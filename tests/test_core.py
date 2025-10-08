"""
Core functionality tests - simple and focused
"""

def test_package_import():
    """Test that the package can be imported"""
    import cdk_aws_s3_transfer
    assert hasattr(cdk_aws_s3_transfer, 'S3TransferStack')
    assert hasattr(cdk_aws_s3_transfer, 'S3TransferConfig')

def test_config_creation():
    """Test that config can be created"""
    from cdk_aws_s3_transfer.config import S3TransferConfig
    
    config = S3TransferConfig()
    assert config.enable_acceleration == True
    assert config.enable_encryption == True
    assert config.bucket_name is None

def test_config_from_dict():
    """Test config creation from dictionary"""
    from cdk_aws_s3_transfer.config import S3TransferConfig
    
    config = S3TransferConfig(
        bucket_name="test-bucket",
        enable_acceleration=False
    )
    assert config.bucket_name == "test-bucket"
    assert config.enable_acceleration == False

def test_validation_function():
    """Test the validation function directly"""
    from cdk_aws_s3_transfer.s3_transfer_stack import S3TransferStack
    
    # Test valid bucket names
    valid_names = ["valid-bucket", "bucket123", "my.bucket.name"]
    for name in valid_names:
        S3TransferStack._validate_bucket_name(None, name)
    
    # Test invalid bucket names
    invalid_names = ["", "ab", "InvalidName", ".bucket", "bucket."]
    for name in invalid_names:
        try:
            S3TransferStack._validate_bucket_name(None, name)
            assert False, f"Invalid name '{name}' should have failed"
        except ValueError:
            pass  # Expected
