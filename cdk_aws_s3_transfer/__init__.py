"""
AWS CDK S3 Transfer Acceleration Package

A reusable CDK stack for creating S3 buckets with transfer acceleration enabled.
"""

from .config import S3TransferConfig
from .s3_transfer_stack import S3TransferStack

__version__ = "1.1.0"
__all__ = ["S3TransferStack", "S3TransferConfig"]
