#!/usr/bin/env python3
"""
AWS CDK App for S3 Transfer Acceleration Stack
"""

import aws_cdk as cdk

from cdk_aws_s3_transfer.s3_transfer_stack import S3TransferStack

app = cdk.App()

# Create the S3 Transfer stack
S3TransferStack(
    app,
    "S3TransferStack",
    bucket_name="my-accelerated-s3-bucket",
    enable_acceleration=True,
    env=cdk.Environment(
        account=app.node.try_get_context("account") or None,
        region=app.node.try_get_context("region") or "ap-southeast-2",
    ),
)

app.synth()
