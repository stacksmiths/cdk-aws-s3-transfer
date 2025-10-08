#!/usr/bin/env python3
"""
Real-world example of S3 Transfer Acceleration usage
This shows how it's typically implemented in production applications
"""

import boto3
import os
from pathlib import Path

def upload_with_acceleration(file_path, bucket_name, key):
    """
    Real-world function that automatically chooses between
    regular S3 and accelerated S3 based on file size
    """
    file_size = os.path.getsize(file_path)
    
    # Use acceleration for files larger than 100MB
    use_acceleration = file_size > 100 * 1024 * 1024  # 100MB
    
    print(f"File size: {file_size / (1024*1024):.2f} MB")
    print(f"Using acceleration: {use_acceleration}")
    
    # Create S3 client with appropriate configuration
    s3_client = boto3.client('s3', use_accelerate_endpoint=use_acceleration)
    
    try:
        # Upload the file
        s3_client.upload_file(file_path, bucket_name, key)
        print(f"✅ Upload successful to s3://{bucket_name}/{key}")
        
        if use_acceleration:
            print("🚀 Used S3 Transfer Acceleration for optimal performance")
        else:
            print("📁 Used regular S3 (file too small for acceleration)")
            
    except Exception as e:
        print(f"❌ Upload failed: {e}")

def smart_upload(file_path, bucket_name):
    """
    Smart upload function that handles different scenarios
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return
    
    # Determine key based on file type
    if file_path.suffix.lower() in ['.mp4', '.avi', '.mov']:
        key = f"videos/{file_path.name}"
        print("🎥 Video file detected - using acceleration")
    elif file_path.suffix.lower() in ['.zip', '.tar', '.gz']:
        key = f"archives/{file_path.name}"
        print("📦 Archive file detected - using acceleration")
    else:
        key = f"uploads/{file_path.name}"
        print("📄 Regular file - checking size for acceleration")
    
    upload_with_acceleration(str(file_path), bucket_name, key)

if __name__ == "__main__":
    # Example usage
    print("Real-world S3 Transfer Acceleration Example")
    print("=" * 50)
    
    # This would be your actual bucket name
    bucket_name = "your-bucket-name"
    
    # Example files (you would replace these with real files)
    test_files = [
        "small-document.pdf",      # < 100MB - regular S3
        "large-video.mp4",         # > 100MB - accelerated S3
        "backup-archive.zip",      # > 100MB - accelerated S3
    ]
    
    for file_path in test_files:
        print(f"\n📁 Processing: {file_path}")
        smart_upload(file_path, bucket_name)
        print("-" * 30)
