# TechEX AWS Deployment Script for PowerShell
# This script builds the TechEX Docker image, pushes it to ECR, and deploys the stack

Write-Host "=== TechEX AWS Deployment Script ===" -ForegroundColor Green
Write-Host "Starting deployment process..." -ForegroundColor Yellow

function Show-StackEvents {
    param(
        [string]$StackName,
        [string]$Region
    )
    try {
        Write-Host "=== Recent CloudFormation Events ===" -ForegroundColor Green
        $eventsJson = aws cloudformation describe-stack-events --stack-name $StackName --region $Region --output json | ConvertFrom-Json
        $events = $eventsJson.StackEvents | Select-Object -First 50 | Select-Object Timestamp, LogicalResourceId, ResourceStatus, ResourceStatusReason
        if ($events) {
            $events | Format-Table -AutoSize | Out-String | Write-Host
        } else {
            Write-Host "[INFO] No events returned yet" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "[ERROR] Unable to fetch stack events: $_" -ForegroundColor Red
    }
}

function Get-StackStatus {
    param(
        [string]$StackName,
        [string]$Region
    )
    try {
        $stackJson = aws cloudformation describe-stacks --stack-name $StackName --region $Region --output json | ConvertFrom-Json
        return $stackJson.Stacks[0].StackStatus
    } catch {
        return $null
    }
}

function Wait-For-StackDeletion {
    param(
        [string]$StackName,
        [string]$Region
    )
    Write-Host "Waiting for stack deletion to complete..." -ForegroundColor Yellow
    try {
        aws cloudformation wait stack-delete-complete --stack-name $StackName --region $Region | Out-Null
        Write-Host "[OK] Stack deletion complete" -ForegroundColor Green
    } catch {
        Write-Host "[WARN] Waiter returned before deletion confirmed. Verifying..." -ForegroundColor Yellow
        $status = Get-StackStatus -StackName $StackName -Region $Region
        if (-not $status) {
            Write-Host "[OK] Stack no longer exists" -ForegroundColor Green
        } else {
            Write-Host "[ERROR] Stack still present with status: $status" -ForegroundColor Red
            throw "Deletion did not complete"
        }
    }
}

function Show-TargetHealth {
    param(
        [string]$StackName,
        [string]$Region
    )
    try {
        $resources = aws cloudformation list-stack-resources --stack-name $StackName --region $Region --output json | ConvertFrom-Json
        $tg = $resources.StackResourceSummaries | Where-Object { $_.ResourceType -eq 'AWS::ElasticLoadBalancingV2::TargetGroup' } | Select-Object -First 1
        if (-not $tg) {
            Write-Host "[WARN] Could not locate Target Group from stack resources" -ForegroundColor Yellow
            return
        }
        $tgPhysicalId = $tg.PhysicalResourceId
        Write-Host "Target Group: $tgPhysicalId" -ForegroundColor Cyan
        $health = aws elbv2 describe-target-health --target-group-arn $tgPhysicalId --region $Region --output json | ConvertFrom-Json
        $states = $health.TargetHealthDescriptions | ForEach-Object {
            [PSCustomObject]@{
                TargetId = (if ($_.Target.Id) { $_.Target.Id } else { $_.Target })
                Port = $_.Target.Port
                State = $_.TargetHealth.State
                Reason = $_.TargetHealth.Reason
                Description = $_.TargetHealth.Description
            }
        }
        if ($states) {
            $states | Format-Table -AutoSize | Out-String | Write-Host
        } else {
            Write-Host "[WARN] No target health descriptions found" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "[ERROR] Unable to fetch target health: $_" -ForegroundColor Red
    }
}

# Check if AWS CLI and Docker are installed
try {
    $awsVersion = aws --version 2>$null
    if ($awsVersion) { Write-Host "[OK] AWS CLI found: $awsVersion" -ForegroundColor Green } else { throw "AWS CLI not found" }
} catch { Write-Host "[ERROR] AWS CLI not found." -ForegroundColor Red; exit 1 }

try {
    $dockerVersion = docker --version 2>$null
    if ($dockerVersion) { Write-Host "[OK] Docker found: $dockerVersion" -ForegroundColor Green } else { throw "Docker not found" }
} catch { Write-Host "[ERROR] Docker not found." -ForegroundColor Red; exit 1 }

# Check env credentials
$requiredVars = @("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN")
$missingVars = @()
foreach ($var in $requiredVars) { if (-not (Get-Item "env:$var" -ErrorAction SilentlyContinue)) { $missingVars += $var } }
if ($missingVars.Count -gt 0) { Write-Host "[ERROR] Missing env vars: $($missingVars -join ', ')" -ForegroundColor Red; exit 1 }
Write-Host "[OK] AWS credentials configured" -ForegroundColor Green

# Region and names
$region = "us-east-1"
$repositoryName = "techex-web"
$stackName = "techex-stack"
$templateFile = "cf-techex.yaml"

# Get Account ID
$accountId = (aws sts get-caller-identity --output json --region $region | ConvertFrom-Json).Account

# Ensure ECR repository exists
Write-Host "Ensuring ECR repository exists: $repositoryName" -ForegroundColor Yellow
$repoDescribe = aws ecr describe-repositories --repository-names $repositoryName --region $region 2>$null
if (-not $?) {
    Write-Host "Creating ECR repository: $repositoryName" -ForegroundColor Yellow
    aws ecr create-repository --repository-name $repositoryName --region $region | Out-Null
}

# Login to ECR
Write-Host "Logging into ECR..." -ForegroundColor Yellow
aws ecr get-login-password --region $region | docker login --username AWS --password-stdin "${accountId}.dkr.ecr.${region}.amazonaws.com"

# Build, tag, and push docker image
$imageTag = "latest"
$imageLocal = "${repositoryName}:${imageTag}"
$imageUri = "${accountId}.dkr.ecr.${region}.amazonaws.com/${repositoryName}:${imageTag}"

Write-Host "Building Docker image: $imageLocal" -ForegroundColor Yellow
# Build from repo root path assumptions: docker/Dockerfile builds web app
$repoRoot = Split-Path -Path (Get-Location) -Parent
$dockerfile = Join-Path $repoRoot "docker/Dockerfile"
$context = $repoRoot

docker build -f $dockerfile -t $imageLocal $context
if ($LASTEXITCODE -ne 0) { Write-Host "[ERROR] Docker build failed" -ForegroundColor Red; exit 1 }

Write-Host "Tagging: $imageLocal -> $imageUri" -ForegroundColor Yellow
docker tag $imageLocal $imageUri

Write-Host "Pushing image: $imageUri" -ForegroundColor Yellow
docker push $imageUri
if ($LASTEXITCODE -ne 0) { Write-Host "[ERROR] Docker push failed" -ForegroundColor Red; exit 1 }

# Validate template
if (-not (Test-Path $templateFile)) { Write-Host "[ERROR] Missing template $templateFile" -ForegroundColor Red; exit 1 }
Write-Host "Validating CloudFormation template..." -ForegroundColor Yellow
aws cloudformation validate-template --template-body file://$templateFile --region $region | Out-Null

# Handle existing stack in bad states
$currentStatus = Get-StackStatus -StackName $stackName -Region $region
if ($currentStatus -and ($currentStatus -match "ROLLBACK|FAILED")) {
    Write-Host "Deleting existing stack in state $currentStatus..." -ForegroundColor Yellow
    aws cloudformation delete-stack --stack-name $stackName --region $region | Out-Null
    Wait-For-StackDeletion -StackName $stackName -Region $region
}

# Deploy with ImageURI parameter
Write-Host "Deploying CloudFormation stack with ImageURI=$imageUri" -ForegroundColor Yellow
$deployCommand = "aws cloudformation deploy --template-file $templateFile --stack-name $stackName --capabilities CAPABILITY_IAM --region $region --parameter-overrides ImageURI=$imageUri"
Write-Host "Running: $deployCommand" -ForegroundColor Gray
Invoke-Expression $deployCommand
if ($LASTEXITCODE -ne 0) { Write-Host "[ERROR] Deployment failed" -ForegroundColor Red; Show-StackEvents -StackName $stackName -Region $region; exit 1 }

# Wait for stack and show health
Write-Host "Waiting for stack to complete..." -ForegroundColor Yellow
aws cloudformation wait stack-create-complete --stack-name $stackName --region $region
Show-TargetHealth -StackName $stackName -Region $region

# Get LB URL
$stackJson = aws cloudformation describe-stacks --stack-name $stackName --region $region --output json | ConvertFrom-Json
$lbUrl = ($stackJson.Stacks[0].Outputs | Where-Object { $_.OutputKey -eq 'TechEXLBURL' }).OutputValue
if ($lbUrl) { Write-Host "[OK] Load Balancer URL: $lbUrl" -ForegroundColor Green } else { Write-Host "[WARN] LB URL not found in outputs" -ForegroundColor Yellow }