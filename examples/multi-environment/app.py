#!/usr/bin/env python3
"""
Multi-stack example of using cdk-aws-s3-transfer

This example demonstrates creating multiple S3 buckets for different purposes:
- Production bucket with acceleration
- Development bucket without acceleration
- Staging bucket with custom configuration
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import aws_cdk as cdk
from cdk_aws_s3_transfer import S3TransferStack

app = cdk.App()

# Get base configuration from context
base_name = app.node.try_get_context("base_name") or "my-company"
region = app.node.try_get_context("region") or "ap-southeast-2"
account = app.node.try_get_context("account") or None

# Production bucket with acceleration
S3TransferStack(
    app,
    "ProductionS3Stack",
    bucket_name=f"{base_name}-prod-data",
    enable_acceleration=True,
    env=cdk.Environment(account=account, region=region),
    tags={
        "Environment": "production",
        "Purpose": "production-data",
        "ManagedBy": "CDK",
    }
)

# Development bucket without acceleration (cost optimization)
S3TransferStack(
    app,
    "DevelopmentS3Stack",
    bucket_name=f"{base_name}-dev-data",
    enable_acceleration=False,
    env=cdk.Environment(account=account, region=region),
    tags={
        "Environment": "development",
        "Purpose": "development-data",
        "ManagedBy": "CDK",
    }
)

# Staging bucket with acceleration
S3TransferStack(
    app,
    "StagingS3Stack",
    bucket_name=f"{base_name}-staging-data",
    enable_acceleration=True,
    env=cdk.Environment(account=account, region=region),
    tags={
        "Environment": "staging",
        "Purpose": "staging-data",
        "ManagedBy": "CDK",
    }
)

# Optional: Analytics bucket (can be deployed separately)
if app.node.try_get_context("include_analytics") == "true":
    S3TransferStack(
        app,
        "AnalyticsS3Stack",
        bucket_name=f"{base_name}-analytics-data",
        enable_acceleration=True,
        env=cdk.Environment(account=account, region=region),
        tags={
            "Environment": "analytics",
            "Purpose": "analytics-data",
            "ManagedBy": "CDK",
        }
    )

app.synth()
