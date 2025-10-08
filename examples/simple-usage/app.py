#!/usr/bin/env python3
"""
Basic example of using cdk-aws-s3-transfer

This example demonstrates the simplest way to use the S3TransferStack
with default settings and clear educational outputs.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import aws_cdk as cdk
from cdk_aws_s3_transfer import S3TransferStack

app = cdk.App()

# Create a basic S3 bucket with transfer acceleration enabled
stack = S3TransferStack(
    app,
    "BasicS3TransferStack",
    description="Basic S3 Transfer Acceleration Stack - Simple usage example",
    tags={
        "Environment": "development",
        "Project": "s3-transfer-example"
    },
    env=cdk.Environment(
        account=app.node.try_get_context("account") or None,
        region=app.node.try_get_context("region") or "ap-southeast-2",
    ),
)

# Add educational outputs
from aws_cdk import CfnOutput

CfnOutput(
    stack,
    "TestInstructions",
    value="Run: ./test-acceleration.sh $(aws cloudformation describe-stacks --stack-name BasicS3TransferStack --query 'Stacks[0].Outputs[?OutputKey==`BucketName`].OutputValue' --output text)",
    description="Command to test transfer acceleration",
)

CfnOutput(
    stack,
    "RegularEndpoint",
    value=f"https://{stack.bucket_name_output}.s3.{stack.region}.amazonaws.com/",
    description="Regular S3 endpoint (direct to region)",
)

CfnOutput(
    stack,
    "AcceleratedEndpointInfo", 
    value=stack.accelerated_endpoint,
    description="Accelerated S3 endpoint (via CloudFront edge)",
)

app.synth()
