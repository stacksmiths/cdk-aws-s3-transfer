# Examples

This directory contains working examples for the `cdk-aws-s3-transfer` package. Each example is a complete, runnable CDK application that demonstrates different ways to use the reusable S3TransferStack.

## Available Examples

### 1. [Simple Usage](./simple-usage/)

The simplest way to use the S3TransferStack with default settings.

**What it demonstrates:**

- Basic stack creation with minimal configuration
- Default transfer acceleration enabled
- Auto-generated bucket name

**Best for:** Getting started quickly, understanding the basics

### 2. [Custom Configuration](./custom-configuration/)

Custom configuration with context-based parameters and tagging.

**What it demonstrates:**

- Custom bucket naming
- Configurable acceleration settings
- Context-based configuration
- Resource tagging
- Environment-specific deployments

**Best for:** Production deployments, custom configurations

### 3. [Multi-Environment](./multi-environment/)

Multiple S3 buckets for different environments and purposes.

**What it demonstrates:**

- Multiple stacks in one application
- Environment-specific configurations
- Cost optimization strategies
- Optional stack inclusion
- Resource management with tags

**Best for:** Multi-environment setups, complex architectures

## Quick Start

1. **Choose an example** that matches your use case
2. **Navigate to the example directory**:

   ```bash
   cd examples/simple-usage  # or custom-configuration, multi-environment
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Deploy the stack**:

   ```bash
   cdk deploy
   ```

5. **Clean up when done**:

   ```bash
   cdk destroy
   ```

## Prerequisites

- AWS CLI configured with appropriate credentials
- CDK bootstrapped in your target region
- Python 3.8+ (or use the Dev Container)

## Using with Dev Container

All usage patterns work seamlessly with the Dev Container:

1. Open the project in VS Code
2. Reopen in Dev Container
3. Navigate to any pattern directory
4. Run the pattern

## Customization

Each example can be customized by:

- **Modifying the code**: Edit `app.py` to change configuration
- **Using context variables**: Pass parameters via `--context`
- **Environment variables**: Set AWS region, account, etc.
- **CDK context files**: Create `cdk.json` for persistent configuration

## Example: Using Context Variables

```bash
# Deploy with custom settings
cdk deploy \
  --context bucket_name=my-custom-bucket \
  --context enable_acceleration=false \
  --context region=ap-southeast-2
```

## Example: Environment-Specific Deployment

```bash
# Development
cdk deploy --context environment=dev --context enable_acceleration=false

# Production
cdk deploy --context environment=prod --context enable_acceleration=true
```

## Contributing

To add a new example:

1. Create a new directory under `examples/`
2. Include `app.py`, `requirements.txt`, and `README.md`
3. Follow the naming convention: `examples/your-example-name/`
4. Update this README to include your example

## Support

For questions about these examples:

- Check the individual example README files
- Review the main project documentation
- Open an issue on GitHub
