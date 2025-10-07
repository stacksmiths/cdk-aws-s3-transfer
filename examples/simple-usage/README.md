# Simple Usage Pattern

This usage pattern demonstrates the simplest way to use the `cdk-aws-s3-transfer` package with **clear examples** of transfer acceleration benefits.

## What it creates

- An S3 bucket with transfer acceleration enabled
- Auto-generated bucket name
- CloudFormation outputs for bucket name and accelerated endpoint
- **Performance comparison tools** to demonstrate acceleration benefits

## Usage

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Deploy the stack:

   ```bash
   cdk deploy
   ```

3. **Test Transfer Acceleration**:

   **Option A: Use the automated test script (recommended):**

   ```bash
   # Get your bucket name from the CDK outputs
   BUCKET_NAME=$(aws cloudformation describe-stacks --stack-name BasicS3TransferStack --query 'Stacks[0].Outputs[?OutputKey==`BucketName`].OutputValue' --output text)

   # Run the automated test
   ./test-acceleration.sh $BUCKET_NAME
   ```

   **Option B: Manual testing:**

   ```bash
   # Create a test file
   echo "Testing S3 Transfer Acceleration" > test-file.txt

   # Upload via regular S3 endpoint
   aws s3 cp test-file.txt s3://YOUR_BUCKET_NAME/regular-upload.txt

   # Upload via accelerated endpoint (notice the --endpoint-url flag!)
   aws s3 cp test-file.txt s3://YOUR_BUCKET_NAME/accelerated-upload.txt --endpoint-url https://s3-accelerate.amazonaws.com

   # Both files will be in the same bucket, but uploaded via different paths!
   aws s3 ls s3://YOUR_BUCKET_NAME/
   ```

4. **Performance Comparison** (optional):

   ```bash
   # Create a larger file to see more dramatic differences
   dd if=/dev/zero of=large-test-file.bin bs=1M count=10

   # Time regular upload
   time aws s3 cp large-test-file.bin s3://YOUR_BUCKET_NAME/regular-large.bin

   # Time accelerated upload
   time aws s3 cp large-test-file.bin s3://YOUR_BUCKET_NAME/accelerated-large.bin --endpoint-url https://s3-accelerate.amazonaws.com
   ```

5. Clean up:

   ```bash
   cdk destroy
   ```

## Key Learning Points

### 🚀 **Transfer Acceleration Benefits**

- **Regular S3**: Direct path to AWS region
- **Accelerated S3**: Routes through CloudFront edge locations + AWS backbone
- **Result**: Faster uploads, especially for large files or distant locations

### 🔧 **How to Use Both Endpoints**

```bash
# Regular S3 (default)
aws s3 cp file.txt s3://bucket-name/

# Accelerated S3 (requires --endpoint-url flag)
aws s3 cp file.txt s3://bucket-name/ --endpoint-url https://s3-accelerate.amazonaws.com
```

### 📊 **When to Use Each**

- **Regular S3**: Small files, same region, cost-sensitive
- **Accelerated S3**: Large files, cross-region, performance-critical

## Configuration

You can override the default region using CDK context:

```bash
cdk deploy --context region=ap-southeast-2
```
