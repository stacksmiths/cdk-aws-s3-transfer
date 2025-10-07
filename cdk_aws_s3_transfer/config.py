"""
Configuration management for S3TransferStack
"""

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class S3TransferConfig:  # pylint: disable=too-many-instance-attributes
    """Configuration class for S3TransferStack"""

    bucket_name: Optional[str] = None
    enable_acceleration: bool = True
    enable_monitoring: bool = True
    # Security settings
    enable_encryption: bool = True
    enable_ssl: bool = True
    enable_public_access_block: bool = True
    # Lifecycle settings
    enable_lifecycle: bool = True
    lifecycle_days: int = 7
    enable_versioning: bool = False

    @classmethod
    def from_environment(cls) -> "S3TransferConfig":
        """Create configuration from environment variables"""
        return cls(
            bucket_name=os.getenv("S3_BUCKET_NAME"),
            enable_acceleration=os.getenv("S3_ENABLE_ACCELERATION", "true").lower()
            == "true",
            enable_monitoring=os.getenv("S3_ENABLE_MONITORING", "true").lower()
            == "true",
            enable_encryption=os.getenv("S3_ENABLE_ENCRYPTION", "true").lower()
            == "true",
            enable_ssl=os.getenv("S3_ENABLE_SSL", "true").lower() == "true",
            enable_lifecycle=os.getenv("S3_ENABLE_LIFECYCLE", "true").lower() == "true",
            lifecycle_days=int(os.getenv("S3_LIFECYCLE_DAYS", "7")),
            enable_versioning=os.getenv("S3_ENABLE_VERSIONING", "false").lower()
            == "true",
            enable_public_access_block=os.getenv(
                "S3_ENABLE_PUBLIC_ACCESS_BLOCK", "true"
            ).lower()
            == "true",
        )

    @classmethod
    def from_context(cls, context: Dict[str, Any]) -> "S3TransferConfig":
        """Create configuration from CDK context"""
        return cls(
            bucket_name=context.get("bucket_name"),
            enable_acceleration=context.get("enable_acceleration", True),
            enable_monitoring=context.get("enable_monitoring", True),
            enable_encryption=context.get("enable_encryption", True),
            enable_ssl=context.get("enable_ssl", True),
            enable_lifecycle=context.get("enable_lifecycle", True),
            lifecycle_days=context.get("lifecycle_days", 7),
            enable_versioning=context.get("enable_versioning", False),
            enable_public_access_block=context.get("enable_public_access_block", True),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "bucket_name": self.bucket_name,
            "enable_acceleration": self.enable_acceleration,
            "enable_monitoring": self.enable_monitoring,
            "enable_encryption": self.enable_encryption,
            "enable_ssl": self.enable_ssl,
            "enable_lifecycle": self.enable_lifecycle,
            "lifecycle_days": self.lifecycle_days,
            "enable_versioning": self.enable_versioning,
            "enable_public_access_block": self.enable_public_access_block,
        }
