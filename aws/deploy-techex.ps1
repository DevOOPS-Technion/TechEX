# TechEX AWS Deployment Script for PowerShell
# This script deploys the TechEX application using CloudFormation

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

# Check if AWS CLI is installed
try {
    $awsVersion = aws --version 2>$null
    if ($awsVersion) {
        Write-Host "[OK] AWS CLI found: $awsVersion" -ForegroundColor Green
    } else {
        throw "AWS CLI not found"
    }
} catch {
    Write-Host "[ERROR] AWS CLI not found. Please install AWS CLI first." -ForegroundColor Red
    Write-Host "Download from: https://aws.amazon.com/cli/" -ForegroundColor Yellow
    exit 1
}

# Check if required environment variables are set
$requiredVars = @("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN")
$missingVars = @()

foreach ($var in $requiredVars) {
    if (-not (Get-Item "env:$var" -ErrorAction SilentlyContinue)) {
        $missingVars += $var
    }
}

if ($missingVars.Count -gt 0) {
    Write-Host "[ERROR] Missing required environment variables:" -ForegroundColor Red
    foreach ($var in $missingVars) {
        Write-Host "   - $var" -ForegroundColor Red
    }
    Write-Host "Please set these variables in PowerShell:" -ForegroundColor Yellow
    Write-Host "$env:AWS_ACCESS_KEY_ID=\"your_access_key\"" -ForegroundColor Cyan
    Write-Host "$env:AWS_SECRET_ACCESS_KEY=\"your_secret_key\"" -ForegroundColor Cyan
    Write-Host "$env:AWS_SESSION_TOKEN=\"your_session_token\"" -ForegroundColor Cyan
    exit 1
}

Write-Host "[OK] AWS credentials configured" -ForegroundColor Green

# Set AWS region
$region = "us-east-1"
Write-Host "Using AWS region: $region" -ForegroundColor Cyan

# Get AWS Account ID
Write-Host "=== Getting AWS Account ID ===" -ForegroundColor Green
try {
    $accountJson = aws sts get-caller-identity --output json --region $region | ConvertFrom-Json
    $accountId = $accountJson.Account
    if ($accountId) {
        Write-Host "[OK] Account ID: $accountId" -ForegroundColor Green
    } else {
        throw "Failed to get account ID"
    }
} catch {
    Write-Host "[ERROR] Failed to get AWS Account ID. Check your credentials." -ForegroundColor Red
    exit 1
}

# Paths and names
$stackName = "techex-stack"
$templateFile = "cf-techex.yaml"

# Check if template file exists
if (-not (Test-Path $templateFile)) {
    Write-Host "[ERROR] CloudFormation template not found: $templateFile" -ForegroundColor Red
    Write-Host "Make sure you're running this script from the aws/ directory" -ForegroundColor Yellow
    exit 1
}

Write-Host "Template file: $templateFile" -ForegroundColor Cyan
Write-Host "Stack name: $stackName" -ForegroundColor Cyan

# Validate template before deploying
Write-Host "Validating CloudFormation template..." -ForegroundColor Yellow
try {
    $validation = aws cloudformation validate-template --template-body file://$templateFile --region $region --output json | ConvertFrom-Json
    if ($validation) { Write-Host "[OK] Template validation passed" -ForegroundColor Green }
} catch {
    Write-Host "[ERROR] Template validation failed" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
}

# Handle existing stack in non-updatable states
$currentStatus = Get-StackStatus -StackName $stackName -Region $region
if ($currentStatus) {
    Write-Host "Current stack status: $currentStatus" -ForegroundColor Cyan
    if ($currentStatus -match "ROLLBACK" -or $currentStatus -eq "CREATE_FAILED" -or $currentStatus -eq "DELETE_FAILED") {
        Write-Host "Stack is in a non-updatable state. Deleting stack before redeploy..." -ForegroundColor Yellow
        try {
            aws cloudformation delete-stack --stack-name $stackName --region $region | Out-Null
            Wait-For-StackDeletion -StackName $stackName -Region $region
        } catch {
            Write-Host "[ERROR] Failed to delete existing stack: $_" -ForegroundColor Red
            Show-StackEvents -StackName $stackName -Region $region
            exit 1
        }
    }
}

# Deploy the stack
try {
    Write-Host "Deploying CloudFormation stack (this may take 10-15 minutes)..." -ForegroundColor Yellow
    
    $deployCommand = "aws cloudformation deploy --template-file $templateFile --stack-name $stackName --capabilities CAPABILITY_IAM --region $region"
    Write-Host "Running: $deployCommand" -ForegroundColor Gray
    
    Invoke-Expression $deployCommand
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] CloudFormation deploy command executed" -ForegroundColor Green
    } else {
        throw "CloudFormation deployment failed with exit code $LASTEXITCODE"
    }
} catch {
    Write-Host "[ERROR] Failed to deploy CloudFormation stack" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
    Show-StackEvents -StackName $stackName -Region $region
    exit 1
}

# Wait for stack to complete
Write-Host "=== Waiting for stack to complete ===" -ForegroundColor Green
try {
    $maxWaitTime = 900  # 15 minutes
    $waitTime = 0
    $waitInterval = 30  # Check every 30 seconds
    
    while ($waitTime -lt $maxWaitTime) {
        $stackJson = aws cloudformation describe-stacks --stack-name $stackName --region $region --output json | ConvertFrom-Json
        $stackStatus = $stackJson.Stacks[0].StackStatus
        
        if ($stackStatus -eq "CREATE_COMPLETE" -or $stackStatus -eq "UPDATE_COMPLETE") {
            Write-Host "[OK] Stack completed successfully (Status: $stackStatus)" -ForegroundColor Green
            break
        } elseif ($stackStatus -match "FAILED|ROLLBACK|DELETE_COMPLETE|DELETE_FAILED") {
            Write-Host "[ERROR] Stack failed with status: $stackStatus" -ForegroundColor Red
            Show-StackEvents -StackName $stackName -Region $region
            exit 1
        } else {
            Write-Host "[WAIT] Stack status: $stackStatus" -ForegroundColor Yellow
            Start-Sleep -Seconds $waitInterval
            $waitTime += $waitInterval
        }
    }
    
    if ($waitTime -ge $maxWaitTime) {
        Write-Host "[WARN] Stack creation is taking longer than expected. Check AWS Console for status." -ForegroundColor Yellow
    }
} catch {
    Write-Host "[ERROR] Error checking stack status: $_" -ForegroundColor Red
}

# Get Application URL
Write-Host "=== Getting Application URL ===" -ForegroundColor Green
$loadBalancerUrl = $null
try {
    $stackJson = aws cloudformation describe-stacks --stack-name $stackName --region $region --output json | ConvertFrom-Json
    $outputs = $stackJson.Stacks[0].Outputs
    if ($outputs) {
        foreach ($out in $outputs) {
            if ($out.OutputKey -eq "TechEXLBURL") {
                $loadBalancerUrl = $out.OutputValue
                break
            }
        }
    }
    
    if ($loadBalancerUrl) {
        Write-Host "[OK] Load Balancer URL: $loadBalancerUrl" -ForegroundColor Green
    } else {
        Write-Host "[WARN] Could not retrieve Load Balancer URL from stack outputs" -ForegroundColor Yellow
    }
} catch {
    Write-Host "[ERROR] Failed to get Load Balancer URL: $_" -ForegroundColor Red
}

# Show target health
Show-TargetHealth -StackName $stackName -Region $region

# Final status
Write-Host "=== Deployment Summary ===" -ForegroundColor Green
Write-Host "[OK] CloudFormation stack: $stackName" -ForegroundColor Green
Write-Host "[OK] Region: $region" -ForegroundColor Green
Write-Host "[OK] Account ID: $accountId" -ForegroundColor Green

if ($loadBalancerUrl) {
    Write-Host "[OK] Application URL: $loadBalancerUrl" -ForegroundColor Green
} else {
    Write-Host "[WARN] Application URL not available yet" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Note: It may take 5-10 minutes for instances to become healthy" -ForegroundColor Yellow
Write-Host "Check the AWS Console for detailed status and monitoring" -ForegroundColor Cyan
Write-Host ""
Write-Host "=== Deployment Complete ===" -ForegroundColor Green