#!/usr/bin/env python3
"""
Advanced example of using cdk-aws-s3-transfer

This example demonstrates custom configuration options including:
- Custom bucket name
- Configurable acceleration settings
- Context-based configuration
- Multiple environments
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import aws_cdk as cdk
from cdk_aws_s3_transfer import S3TransferStack

app = cdk.App()

# Get configuration from context or use defaults
bucket_name = app.node.try_get_context("bucket_name") or "my-advanced-s3-bucket"
enable_acceleration = app.node.try_get_context("enable_acceleration") != "false"
environment = app.node.try_get_context("environment") or "dev"

# Create the stack with custom configuration
S3TransferStack(
    app,
    f"AdvancedS3TransferStack-{environment.title()}",
    bucket_name=f"{bucket_name}-{environment}",
    enable_acceleration=enable_acceleration,
    env=cdk.Environment(
        account=app.node.try_get_context("account") or None,
        region=app.node.try_get_context("region") or "ap-southeast-2",
    ),
    tags={
        "Environment": environment,
        "Project": "AdvancedS3Transfer",
        "ManagedBy": "CDK",
    }
)

app.synth()
