#!/bin/bash
# Test script to demonstrate S3 Transfer Acceleration benefits

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 S3 Transfer Acceleration Demo${NC}"
echo "=================================="

# Check if bucket name is provided
if [ -z "$1" ]; then
    echo -e "${RED}❌ Error: Please provide the S3 bucket name${NC}"
    echo "Usage: $0 <bucket-name>"
    echo "Example: $0 my-accelerated-bucket"
    exit 1
fi

BUCKET_NAME="$1"
echo -e "${YELLOW}📦 Testing with bucket: ${BUCKET_NAME}${NC}"
echo ""

# Create test files
echo -e "${BLUE}📁 Creating test files...${NC}"
echo "Small file test..." > small-test.txt
dd if=/dev/zero of=large-test.bin bs=1M count=5 2>/dev/null
echo -e "${GREEN}✅ Test files created${NC}"
echo ""

# Test 1: Small file comparison
echo -e "${BLUE}🧪 Test 1: Small file upload (5KB)${NC}"
echo "----------------------------------------"

echo -e "${YELLOW}📤 Uploading via regular S3 endpoint...${NC}"
time aws-vault exec dev -- aws s3 cp small-test.txt s3://${BUCKET_NAME}/regular-small.txt

echo -e "${YELLOW}📤 Uploading via accelerated S3 endpoint...${NC}"
time aws-vault exec dev -- aws s3 cp small-test.txt s3://${BUCKET_NAME}/accelerated-small.txt --endpoint-url https://s3-accelerate.amazonaws.com

echo ""

# Test 2: Large file comparison
echo -e "${BLUE}🧪 Test 2: Large file upload (5MB)${NC}"
echo "----------------------------------------"

echo -e "${YELLOW}📤 Uploading via regular S3 endpoint...${NC}"
time aws-vault exec dev -- aws s3 cp large-test.bin s3://${BUCKET_NAME}/regular-large.bin

echo -e "${YELLOW}📤 Uploading via accelerated S3 endpoint...${NC}"
time aws-vault exec dev -- aws s3 cp large-test.bin s3://${BUCKET_NAME}/accelerated-large.bin --endpoint-url https://s3-accelerate.amazonaws.com

echo ""

# Show results
echo -e "${BLUE}📋 Results Summary${NC}"
echo "=================="
aws-vault exec dev -- aws s3 ls s3://${BUCKET_NAME}/ --human-readable

echo ""
echo -e "${GREEN}✅ Demo completed!${NC}"
echo -e "${YELLOW}💡 Key takeaway: Both files are in the same bucket, but uploaded via different network paths${NC}"
echo -e "${YELLOW}   - Regular S3: Direct to AWS region${NC}"
echo -e "${YELLOW}   - Accelerated S3: Through CloudFront edge + AWS backbone${NC}"

# Cleanup local files
rm -f small-test.txt large-test.bin
echo -e "${GREEN}🧹 Local test files cleaned up${NC}"
