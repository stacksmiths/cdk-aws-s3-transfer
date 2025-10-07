# Custom Configuration Pattern

This usage pattern demonstrates advanced configuration options for the `cdk-aws-s3-transfer` package.

## What it creates

- An S3 bucket with configurable transfer acceleration
- Custom bucket name with environment suffix
- CloudFormation tags for resource management
- Context-based configuration

## Usage

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Deploy with default settings:

   ```bash
   cdk deploy
   ```

3. Deploy with custom configuration:

   ```bash
   cdk deploy \
     --context bucket_name=my-custom-bucket \
     --context environment=prod \
     --context enable_acceleration=true \
     --context region=ap-southeast-2
   ```

4. Deploy without acceleration:

   ```bash
   cdk deploy --context enable_acceleration=false
   ```

5. Clean up:

   ```bash
   cdk destroy
   ```

## Configuration Options

| Context Variable | Default | Description |
|------------------|---------|-------------|
| `bucket_name` | `my-advanced-s3-bucket` | Base name for the S3 bucket |
| `environment` | `dev` | Environment suffix for bucket name |
| `enable_acceleration` | `true` | Whether to enable transfer acceleration |
| `region` | `ap-southeast-2` | AWS region for deployment |
| `account` | `None` | AWS account ID (uses default profile) |

## Example Deployments

### Development Environment

```bash
cdk deploy --context environment=dev --context enable_acceleration=false
```

### Production Environment

```bash
cdk deploy --context environment=prod --context enable_acceleration=true --context region=ap-southeast-2
```

### Custom Bucket Name

```bash
cdk deploy --context bucket_name=my-company-data --context environment=prod
```
