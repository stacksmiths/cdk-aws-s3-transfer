"""
AWS CDK Stack for S3 Transfer Acceleration
"""

import logging
import re
from typing import Optional

from aws_cdk import CfnOutput, Duration, RemovalPolicy, Stack
from aws_cdk import aws_cloudwatch as cloudwatch
from aws_cdk import aws_s3 as s3
from aws_cdk.aws_s3 import CfnBucket
from constructs import Construct

# Configure logging
logger = logging.getLogger(__name__)


class S3TransferStack(Stack):
    """
    A reusable CDK stack that provisions an S3 bucket with Transfer Acceleration.

    This stack creates an S3 bucket with the following features:
    - Configurable bucket name
    - Optional transfer acceleration
    - Automatic object deletion on stack destruction
    - Proper removal policy for easy cleanup
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        bucket_name: Optional[str] = None,
        enable_acceleration: bool = True,
        description: Optional[str] = None,
        **kwargs,
    ) -> None:
        """
        Initialize the S3 Transfer Stack.

        Args:
            scope: The parent construct
            construct_id: The construct ID
            bucket_name: Name for the S3 bucket (optional, auto-generated)
            enable_acceleration: Whether to enable S3 Transfer Acceleration
            description: Description for the CloudFormation stack
            **kwargs: Additional arguments passed to the parent Stack

        Raises:
            ValueError: If bucket_name is provided but invalid
        """
        # Set stack description if provided
        if description:
            kwargs["description"] = description

        super().__init__(scope, construct_id, **kwargs)

        # Log stack creation
        logger.info("Creating S3TransferStack: %s", construct_id)

        # Safety check for production environments
        if self.node.try_get_context("environment") == "prod":
            logger.warning(
                "⚠️  PRODUCTION MODE: Stack configured for production environment"
            )
            logger.warning(
                "⚠️  Ensure you have proper backups before deploying to production"
            )

        # Validate bucket name if provided
        if bucket_name:
            logger.debug("Validating bucket name: %s", bucket_name)
            self._validate_bucket_name(bucket_name)

        # Create the S3 bucket with enhanced security
        self.bucket = s3.Bucket(
            self,
            "TransferBucket",
            bucket_name=bucket_name,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            versioned=False,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            enforce_ssl=True,
            lifecycle_rules=[
                s3.LifecycleRule(
                    id="DeleteIncompleteMultipartUploads",
                    abort_incomplete_multipart_upload_after=Duration.days(7),
                )
            ],
        )

        # Enable transfer acceleration if requested
        if enable_acceleration:
            logger.info("Enabling S3 Transfer Acceleration")
            # Use CfnBucket to enable transfer acceleration
            cfn_bucket = self.bucket.node.default_child
            if cfn_bucket and isinstance(cfn_bucket, CfnBucket):
                cfn_bucket.add_property_override(
                    "AccelerateConfiguration", {"AccelerationStatus": "Enabled"}
                )

        # Create CloudWatch monitoring
        self._create_monitoring()

        # Output the bucket name and accelerated endpoint
        self.bucket_name_output = self.bucket.bucket_name
        self.accelerated_endpoint = (
            f"https://{self.bucket_name_output}.s3-accelerate.amazonaws.com"
        )

        # Create CDK outputs

        CfnOutput(
            self,
            "BucketName",
            value=self.bucket_name_output,
            description="Name of the S3 bucket",
        )

        CfnOutput(
            self,
            "AcceleratedEndpoint",
            value=self.accelerated_endpoint,
            description="Accelerated S3 endpoint URL",
        )

        if enable_acceleration:
            CfnOutput(
                self,
                "TransferAccelerationStatus",
                value="Enabled",
                description="S3 Transfer Acceleration status",
            )
        else:
            CfnOutput(
                self,
                "TransferAccelerationStatus",
                value="Disabled",
                description="S3 Transfer Acceleration status",
            )

    def _validate_bucket_name(self, bucket_name: str) -> None:
        """
        Validate S3 bucket name according to AWS naming rules.

        Args:
            bucket_name: The bucket name to validate

        Raises:
            ValueError: If the bucket name is invalid
        """
        if not bucket_name:
            raise ValueError("Bucket name cannot be empty")

        # Check length (3-63 characters)
        if len(bucket_name) < 3 or len(bucket_name) > 63:
            raise ValueError("Bucket name must be between 3 and 63 characters long")

        # Check for valid characters (lowercase letters, numbers, dots, hyphens)
        if not re.match(r"^[a-z0-9.-]+$", bucket_name):
            raise ValueError(
                "Bucket name can only contain lowercase letters, numbers, "
                "dots, and hyphens"
            )

        # Check that it doesn't start or end with a dot or hyphen
        if bucket_name.startswith(".") or bucket_name.endswith("."):
            raise ValueError("Bucket name cannot start or end with a dot")

        if bucket_name.startswith("-") or bucket_name.endswith("-"):
            raise ValueError("Bucket name cannot start or end with a hyphen")

        # Check for consecutive dots
        if ".." in bucket_name:
            raise ValueError("Bucket name cannot contain consecutive dots")

        # Check for IP address format
        if re.match(r"^\d+\.\d+\.\d+\.\d+$", bucket_name):
            raise ValueError("Bucket name cannot be formatted as an IP address")

    def _create_monitoring(self) -> None:
        """
        Create CloudWatch monitoring for the S3 bucket.
        """
        logger.debug("Creating CloudWatch monitoring")

        # Create CloudWatch dashboard
        dashboard = cloudwatch.Dashboard(
            self,
            "S3TransferDashboard",
            dashboard_name=f"{self.stack_name}-s3-transfer-dashboard",
        )

        # Add S3 metrics to dashboard
        dashboard.add_widgets(
            cloudwatch.GraphWidget(
                title="S3 Bucket Size",
                left=[
                    cloudwatch.Metric(
                        namespace="AWS/S3",
                        metric_name="BucketSizeBytes",
                        dimensions_map={
                            "BucketName": self.bucket.bucket_name,
                            "StorageType": "StandardStorage",
                        },
                        statistic="Average",
                    )
                ],
                width=12,
                height=6,
            ),
            cloudwatch.GraphWidget(
                title="S3 Request Metrics",
                left=[
                    cloudwatch.Metric(
                        namespace="AWS/S3",
                        metric_name="NumberOfObjects",
                        dimensions_map={
                            "BucketName": self.bucket.bucket_name,
                            "StorageType": "AllStorageTypes",
                        },
                        statistic="Average",
                    )
                ],
                width=12,
                height=6,
            ),
        )

        # Create CloudWatch alarms
        self._create_alarms()

    def _create_alarms(self) -> None:
        """
        Create CloudWatch alarms for monitoring.
        """
        logger.debug("Creating CloudWatch alarms")

        # Alarm for high error rate (if applicable)
        cloudwatch.Alarm(
            self,
            "S3ErrorRateAlarm",
            metric=cloudwatch.Metric(
                namespace="AWS/S3",
                metric_name="4xxErrors",
                dimensions_map={"BucketName": self.bucket.bucket_name},
                statistic="Sum",
            ),
            threshold=10,
            evaluation_periods=2,
            alarm_description="S3 4xx errors alarm",
        )

        # Alarm for unusual activity (if applicable)
        cloudwatch.Alarm(
            self,
            "S3ActivityAlarm",
            metric=cloudwatch.Metric(
                namespace="AWS/S3",
                metric_name="AllRequests",
                dimensions_map={"BucketName": self.bucket.bucket_name},
                statistic="Sum",
            ),
            threshold=1000,
            evaluation_periods=1,
            alarm_description="High S3 activity alarm",
        )
