# TechEX AWS Deployment Guide

This guide deploys TechEX to AWS using CloudFormation and an Application Load Balancer. The script builds a Docker image locally, pushes it to ECR, and then deploys a stack that pulls and runs the image on EC2 instances.

## Prerequisites
- AWS CLI v2
- Docker (running locally)
- PowerShell 5.1+ or PowerShell 7
- Temporary AWS credentials (sandbox) in `us-east-1` or `us-west-2`

## Credentials (PowerShell)
```powershell
$env:AWS_ACCESS_KEY_ID="<key>"
$env:AWS_SECRET_ACCESS_KEY="<secret>"
$env:AWS_SESSION_TOKEN="<session>"
```

## One-command deploy (WIN)
```powershell
cd aws
.\deploy-techex.ps1
```
The script will:
- Build `techex-web:latest` from `docker/Dockerfile`
- Ensure ECR repository `techex-web` exists and push the image
- Deploy CloudFormation stack `techex-stack` with `ImageURI=<your ECR image>`
- Wait for completion and print the ALB URL
- Print Target Group health for quick diagnosis

## What the stack creates (`cf-techex.yaml`)
- VPC (10.10.0.0/16) with 2 public subnets in different AZs
- Internet Gateway + routing
- Security groups for ALB (80) and EC2 (5000, 22)
- Application Load Balancer → Target Group (port 5000)
- Target Group health check: `GET /health`, success codes `200-399`
- Launch Template with UserData that logs into ECR and runs your image
- Auto Scaling Group (2-4 instances)
- Uses sandbox’s pre-created `LabInstanceProfile` (no custom IAM creation)

## Region
- Default is `us-east-1`. You can change `$region` in `deploy-techex.ps1` to `us-west-2` if needed.

## Troubleshooting
- 502 at ALB URL? Give it a minute. Check printed target health.
- Stuck stack (ROLLBACK_COMPLETE)? The script will delete and redeploy automatically.
- Verify the image exists in ECR and the `ImageURI` matches the pushed tag (`latest`).

## Useful commands
```powershell
# Show stack events
aws cloudformation describe-stack-events --stack-name techex-stack --region us-east-1 | cat

# Delete stack
aws cloudformation delete-stack --stack-name techex-stack --region us-east-1 | cat

# Describe target health (when you have the TG ARN)
aws elbv2 describe-target-health --target-group-arn <tg-arn> --region us-east-1 | cat
```

Tip: This sandbox pre-creates `LabInstanceProfile` and restricts services/regions. The template is compliant.
