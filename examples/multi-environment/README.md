# Multi-Environment Pattern

This usage pattern demonstrates creating multiple S3 buckets for different environments and purposes using the `cdk-aws-s3-transfer` package.

## What it creates

- **Production bucket**: With transfer acceleration enabled
- **Development bucket**: Without acceleration (cost optimization)
- **Staging bucket**: With transfer acceleration enabled
- **Analytics bucket**: Optional, with acceleration enabled

Each bucket has appropriate tags for resource management and cost tracking.

## Usage

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Deploy all stacks:

   ```bash
   # Using virtual environment (recommended)
   source ../../venv/bin/activate
   aws-vault exec dev -- cdk deploy --all --context base_name=my-company
   ```

3. **Test the deployment**:

   ```bash
   # Verify buckets were created
   aws-vault exec dev -- aws s3 ls --region ap-southeast-2 | grep my-company

   # Test production bucket (with acceleration)
   echo "Test file" > test-file.txt
   aws-vault exec dev -- aws s3 cp test-file.txt s3://my-company-prod-data/regular-upload.txt --region ap-southeast-2
   aws-vault exec dev -- aws s3 cp test-file.txt s3://my-company-prod-data/accelerated-upload.txt --endpoint-url https://s3-accelerate.amazonaws.com --region ap-southeast-2

   # Test development bucket (no acceleration)
   aws-vault exec dev -- aws s3 cp test-file.txt s3://my-company-dev-data/dev-upload.txt --region ap-southeast-2

   # Test staging bucket (with acceleration)
   aws-vault exec dev -- aws s3 cp test-file.txt s3://my-company-staging-data/staging-upload.txt --endpoint-url https://s3-accelerate.amazonaws.com --region ap-southeast-2

   # Verify all files uploaded successfully
   aws-vault exec dev -- aws s3 ls s3://my-company-prod-data/ --region ap-southeast-2
   aws-vault exec dev -- aws s3 ls s3://my-company-dev-data/ --region ap-southeast-2
   aws-vault exec dev -- aws s3 ls s3://my-company-staging-data/ --region ap-southeast-2
   ```

4. Deploy with custom base name:

   ```bash
   aws-vault exec dev -- cdk deploy --all --context base_name=my-company
   ```

5. Deploy with analytics bucket:

   ```bash
   aws-vault exec dev -- cdk deploy --all --context include_analytics=true
   ```

6. Deploy specific stack only:

   ```bash
   aws-vault exec dev -- cdk deploy ProductionS3Stack
   ```

7. Clean up all stacks:

   ```bash
   aws-vault exec dev -- cdk destroy --all --force
   ```

## Configuration Options

| Context Variable | Default | Description |
|------------------|---------|-------------|
| `base_name` | `my-company` | Base name for all S3 buckets |
| `region` | `ap-southeast-2` | AWS region for deployment |
| `account` | `None` | AWS account ID (uses default profile) |
| `include_analytics` | `false` | Whether to include analytics bucket |

## Stack Details

### ProductionS3Stack

- Bucket name: `{base_name}-prod-data`
- Transfer acceleration: **Enabled**
- Purpose: Production data storage
- Environment: production

### DevelopmentS3Stack

- Bucket name: `{base_name}-dev-data`
- Transfer acceleration: **Disabled** (cost optimization)
- Purpose: Development data storage
- Environment: development

### StagingS3Stack

- Bucket name: `{base_name}-staging-data`
- Transfer acceleration: **Enabled**
- Purpose: Staging data storage
- Environment: staging

### AnalyticsS3Stack (Optional)

- Bucket name: `{base_name}-analytics-data`
- Transfer acceleration: **Enabled**
- Purpose: Analytics data storage
- Environment: analytics

## Example Deployments

### Basic Multi-Environment Setup

```bash
source ../../venv/bin/activate
aws-vault exec dev -- cdk deploy --all --context base_name=myapp
```

### Full Setup with Analytics

```bash
source ../../venv/bin/activate
aws-vault exec dev -- cdk deploy --all \
  --context base_name=myapp \
  --context include_analytics=true \
  --context region=ap-southeast-2
```

### Production Only

```bash
source ../../venv/bin/activate
aws-vault exec dev -- cdk deploy ProductionS3Stack --context base_name=myapp
```

## Cost Optimization

- Development bucket has acceleration disabled to reduce costs
- Production and staging buckets have acceleration enabled for performance
- Each bucket can be managed independently
- Tags help with cost allocation and resource tracking
