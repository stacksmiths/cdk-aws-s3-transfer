.PHONY: help install install-dev test lint format clean setup

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup: ## Set up development environment
	python3 -m venv venv
	@echo "Virtual environment created. Activate it with: source venv/bin/activate"

install: ## Install production dependencies
	./venv/bin/pip install -r requirements.txt

install-dev: install ## Install development dependencies
	./venv/bin/pip install -r requirements-dev.txt
	@echo "Installing CDK CLI..."
	@./install-cdk.sh || echo "CDK CLI installation failed. Please run './install-cdk.sh' manually."

test: ## Run tests
	pytest

lint: ## Run linting
	pylint cdk_aws_s3_transfer/
	mypy cdk_aws_s3_transfer/

format: ## Format code
	black cdk_aws_s3_transfer/ app.py
	isort cdk_aws_s3_transfer/ app.py

format-check: ## Check code formatting
	black --check cdk_aws_s3_transfer/ app.py
	isort --check-only cdk_aws_s3_transfer/ app.py

lint-fix: ## Auto-fix linting issues
	./venv/bin/autoflake --remove-all-unused-imports --remove-unused-variables --in-place --recursive cdk_aws_s3_transfer/ app.py
	black cdk_aws_s3_transfer/ app.py
	isort cdk_aws_s3_transfer/ app.py

clean: ## Clean up temporary files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ *.egg-info/

check-cdk: ## Check if CDK CLI is installed
	@which cdk > /dev/null || (echo "CDK CLI not found. Run 'make install-dev' first." && exit 1)

deploy: check-cdk ## Deploy CDK stack
	cdk deploy

diff: check-cdk ## Show CDK diff
	cdk diff

synth: check-cdk ## Synthesize CDK template
	cdk synth

bootstrap: check-cdk ## Bootstrap CDK environment
	cdk bootstrap

destroy: check-cdk ## Destroy the CDK stack (removes all resources)
	@echo "⚠️  WARNING: This will permanently delete all resources in the stack!"
	@echo "This includes:"
	@echo "  - S3 bucket and all objects"
	@echo "  - Lambda functions"
	@echo "  - IAM roles and policies"
	@echo ""
	@read -p "Are you sure you want to continue? (type 'yes' to confirm): " confirm && [ "$$confirm" = "yes" ]
	cdk destroy --force

destroy-all: check-cdk ## Destroy all stacks (if using multiple environments)
	@echo "⚠️  WARNING: This will permanently delete ALL stacks!"
	@read -p "Are you sure you want to continue? (type 'yes' to confirm): " confirm && [ "$$confirm" = "yes" ]
	cdk destroy --all --force

verify-cleanup: check-cdk ## Verify that stack has been properly destroyed
	@echo "Checking if stack exists..."
	@if cdk list 2>/dev/null | grep -q "S3TransferStack"; then \
		echo "❌ Stack still exists! Run 'make destroy' to remove it."; \
		exit 1; \
	else \
		echo "✅ Stack has been properly destroyed."; \
	fi

security: ## Run security checks
	bandit -r cdk_aws_s3_transfer/
	safety check

coverage: ## Run tests with coverage
	./venv/bin/pytest tests/ --cov=cdk_aws_s3_transfer --cov-report=html --cov-report=term

coverage-check: ## Check test coverage
	./venv/bin/pytest tests/ --cov=cdk_aws_s3_transfer --cov-fail-under=80

all: clean install-dev format lint test security coverage-check ## Run all checks
