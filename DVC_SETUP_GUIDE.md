# DVC Setup Guide for CI/CD

This guide explains how to set up DVC (Data Version Control) with remote storage for the CI/CD pipeline.

## Problem

The CI/CD pipeline fails with:
```
ERROR: failed to reproduce 'data/Crop_recommendation.csv.dvc': missing data 'source': data/Crop_recommendation.csv
```

This happens because:
1. Large data files are tracked by DVC, not Git
2. Only the `.dvc` metadata file is committed to Git
3. The actual data must be pulled from DVC remote storage (S3)

## Solution

### Step 1: Set Up AWS S3 Bucket

1. **Create an S3 bucket** for DVC storage:
   ```bash
   aws s3 mb s3://your-bucket-name/dvc-storage
   ```

2. **Configure bucket permissions** to allow CI/CD access

### Step 2: Configure GitHub Secrets

Add these secrets to your GitHub repository:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `AWS_ROLE_TO_ASSUME` | AWS IAM Role ARN for OIDC | `arn:aws:iam::123456789:role/github-actions-role` |
| `AWS_REGION` | AWS Region | `us-east-1` |
| `DVC_S3_URL` | S3 URL for DVC storage | `s3://your-bucket-name/dvc-storage` |

**To add secrets:**
1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add each secret

### Step 3: Push Data to DVC Remote

**Option A: Using the initialization script**

```bash
# Linux/Mac/WSL
bash scripts/init_dvc_data.sh

# Windows PowerShell
.\scripts\init_dvc_data.ps1
```

**Option B: Manual steps**

```bash
# 1. Ensure data is tracked by DVC
dvc add data/Crop_recommendation.csv
git add data/Crop_recommendation.csv.dvc data/.gitignore
git commit -m "Track data with DVC"

# 2. Configure DVC remote
dvc remote add -d myremote s3://your-bucket-name/dvc-storage
git add .dvc/config
git commit -m "Configure DVC remote"

# 3. Push data to S3
dvc push

# 4. Push to GitHub
git push
```

### Step 4: Verify Setup

1. **Check DVC configuration:**
   ```bash
   dvc remote list
   dvc status
   ```

2. **Test data pull:**
   ```bash
   # Remove local data
   rm data/Crop_recommendation.csv
   
   # Pull from remote
   dvc pull data/Crop_recommendation.csv.dvc
   
   # Verify
   ls -lh data/Crop_recommendation.csv
   ```

3. **Trigger CI/CD:**
   ```bash
   git commit --allow-empty -m "Test CI/CD with DVC"
   git push
   ```

## CI/CD Workflow

The updated workflow now:

1. ✅ Configures AWS credentials
2. ✅ Sets up DVC remote
3. ✅ **Pulls data from S3**
4. ✅ Verifies data exists
5. ✅ Runs DVC pipeline
6. ✅ Pushes artifacts back to S3

## Troubleshooting

### Data Not Found in S3

**Error:** `Could not pull data from remote`

**Solution:**
```bash
# Check if data was pushed
dvc status -c

# Push data to remote
dvc push
```

### AWS Credentials Issue

**Error:** `Failed to authenticate to AWS`

**Solution:**
- Verify GitHub secrets are set correctly
- Check IAM role has S3 access permissions
- Ensure trust policy allows GitHub OIDC

### Wrong S3 Path

**Error:** `No such bucket`

**Solution:**
```bash
# Check current remote
dvc remote list

# Update remote URL
dvc remote modify myremote url s3://correct-bucket-name/dvc-storage
git add .dvc/config
git commit -m "Fix DVC remote URL"
git push
```

## DVC Commands Reference

```bash
# Check DVC status
dvc status

# Check remote status
dvc status -c

# Pull specific file
dvc pull data/Crop_recommendation.csv.dvc

# Pull all DVC-tracked files
dvc pull

# Push to remote
dvc push

# List remotes
dvc remote list

# Add remote
dvc remote add -d myremote s3://bucket/path

# Modify remote
dvc remote modify myremote url s3://new-bucket/path

# Remove remote
dvc remote remove myremote
```

## Best Practices

1. **Always push data before pushing code:**
   ```bash
   dvc push
   git push
   ```

2. **Commit .dvc files to Git:**
   - `data/Crop_recommendation.csv.dvc` ✅
   - `data/Crop_recommendation.csv` ❌

3. **Keep .dvc/config in Git:**
   ```bash
   git add .dvc/config
   git commit -m "Update DVC configuration"
   ```

4. **Use consistent remote names:**
   - Production: `myremote` or `aws`
   - Development: `dev-remote`

5. **Document S3 bucket structure:**
   ```
   s3://your-bucket/
   └── dvc-storage/
       └── files/
           └── md5/
               └── <hash>
   ```

## Alternative: Local Testing Without S3

For local testing without S3:

```bash
# Use local remote
dvc remote add -d local /tmp/dvc-storage

# Push/pull locally
dvc push
dvc pull
```

## Security Notes

⚠️ **Never commit:**
- AWS credentials
- S3 bucket credentials
- `.dvc/config` with hardcoded credentials

✅ **Always use:**
- GitHub Secrets for credentials
- IAM roles with minimum permissions
- Encrypted S3 buckets

## Additional Resources

- [DVC Documentation](https://dvc.org/doc)
- [DVC with S3](https://dvc.org/doc/user-guide/data-management/remote-storage/amazon-s3)
- [GitHub Actions with AWS](https://github.com/aws-actions/configure-aws-credentials)
- [OIDC for GitHub Actions](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)
