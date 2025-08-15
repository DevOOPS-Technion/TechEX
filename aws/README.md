# TechEX AWS Deployment Guide

This guide will help you deploy the TechEX application to AWS using CloudFormation.

## Prerequisites

1. **AWS CLI** - Install from [https://aws.amazon.com/cli/](https://aws.amazon.com/cli/)
2. **PowerShell** - Windows PowerShell 5.1 or later
3. **AWS Credentials** - Temporary credentials with appropriate permissions

## Quick Start

### 1. Set AWS Credentials in PowerShell

Open PowerShell and set your AWS credentials:

```powershell
$env:AWS_ACCESS_KEY_ID="your_access_key"
$env:AWS_SECRET_ACCESS_KEY="your_secret_key"
$env:AWS_SESSION_TOKEN="your_session_token"
```

### 2. Run Deployment

#### Option A: Using the Batch File (Recommended)
Double-click `deploy-techex.bat` in the `aws/` directory.

#### Option B: Using PowerShell Directly
```powershell
cd aws
.\deploy-techex.ps1
```

## What Gets Deployed

The CloudFormation template (`cf-techex.yaml`) creates:

- **VPC** with CIDR `10.10.0.0/16`
- **2 Subnets** in `us-east-1a` and `us-east-1b`
- **Internet Gateway** for external access
- **Security Groups** for load balancer and EC2 instances
- **Application Load Balancer** distributing traffic
- **Auto Scaling Group** with 2-4 instances
- **Launch Template** that builds TechEX from GitHub

## Architecture

```
Internet → Load Balancer → EC2 Instances (2+)
                    ↓
            Auto Scaling Group
                    ↓
        [us-east-1a] [us-east-1b]
```

## Deployment Process

1. **Validation** - Checks AWS CLI and credentials
2. **Account Verification** - Gets AWS Account ID
3. **Stack Deployment** - Creates CloudFormation stack
4. **Monitoring** - Waits for stack completion
5. **Output** - Provides application URL

## Expected Timeline

- **Stack Creation**: 10-15 minutes
- **Instance Health**: 5-10 minutes after stack completion
- **Total Time**: 15-25 minutes

## Monitoring

During deployment, the script will show:
- ✅ Success indicators
- ⏳ Progress updates
- ❌ Error messages
- 🌐 Final application URL

## Troubleshooting

### Common Issues

1. **AWS CLI Not Found**
   - Install AWS CLI from official website
   - Restart PowerShell after installation

2. **Missing Credentials**
   - Set all three environment variables
   - Check if credentials are expired

3. **Template Errors**
   - Verify `cf-techex.yaml` exists
   - Check CloudFormation console for detailed errors

4. **Stack Creation Fails**
   - Check AWS Console for error details
   - Verify account has necessary permissions

### Useful Commands

```powershell
# Check stack status
aws cloudformation describe-stacks --stack-name techex-stack --region us-east-1

# Delete stack if needed
aws cloudformation delete-stack --stack-name techex-stack --region us-east-1

# List all stacks
aws cloudformation list-stacks --region us-east-1
```

## Security Notes

- EC2 instances are in private subnets
- Load balancer is internet-facing
- SSH access (port 22) is open for debugging
- Application runs on port 5000 internally

## Cost Optimization

- Uses `t3.medium` instances (cost-effective)
- Auto-scaling between 2-4 instances
- Consider stopping instances when not in use

## Support

If you encounter issues:
1. Check the AWS CloudFormation console
2. Review CloudWatch logs
3. Verify all prerequisites are met
4. Check AWS service limits in your account

---

**Note**: This deployment creates production-ready infrastructure. Monitor costs and usage in your AWS account.
