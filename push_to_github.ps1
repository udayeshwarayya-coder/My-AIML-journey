# ============================================================
# push_to_github.ps1
# Run this script ONCE to initialize your repo and push everything.
# Usage: .\push_to_github.ps1 -RepoUrl "https://github.com/YOUR_USERNAME/300-days-ai-ml.git"
# ============================================================

param(
    [Parameter(Mandatory=$true)]
    [string]$RepoUrl
)

Write-Host "`n?? 300 Days AI/ML — GitHub Push Script" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Step 1: Init git if not already
if (-not (Test-Path ".git")) {
    Write-Host "`n?? Initializing git repository..." -ForegroundColor Yellow
    git init
    git branch -M main
} else {
    Write-Host "`n? Git already initialized." -ForegroundColor Green
}

# Step 2: Add remote
$remotes = git remote
if ($remotes -notcontains "origin") {
    Write-Host "`n?? Adding remote origin..." -ForegroundColor Yellow
    git remote add origin $RepoUrl
} else {
    Write-Host "`n? Remote origin already exists." -ForegroundColor Green
    git remote set-url origin $RepoUrl
}

# Step 3: Stage and commit everything
Write-Host "`n?? Staging all files..." -ForegroundColor Yellow
git add .

Write-Host "`n??  Committing..." -ForegroundColor Yellow
git commit -m "?? Initial commit: 300 Days AI/ML — Phase 1 (Days 1-11)"

# Step 4: Push
Write-Host "`n??  Pushing to GitHub..." -ForegroundColor Yellow
git push -u origin main

Write-Host "`n? Done! Your 300-day journey is now live on GitHub." -ForegroundColor Green
Write-Host "?? Visit: $RepoUrl" -ForegroundColor Cyan
