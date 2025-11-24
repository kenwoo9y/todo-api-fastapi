# Heroku Deployment Guide

This document explains how to deploy a FastAPI application to Heroku and how to run database migrations.

## Table of Contents

1. [GitHub Secrets Configuration](#github-secrets-configuration)
2. [Deployment Steps](#deployment-steps)
3. [Database Migration Steps](#database-migration-steps)

## GitHub Secrets Configuration

To deploy to Heroku from GitHub Actions, you need to configure the following secrets.

### Required Secrets

Configure the following secrets for each environment (dev, stg, prod):

1. **`HEROKU_API_KEY`**: Heroku API key
   - Obtain from Heroku Dashboard → "Account settings" → "API Key"
   - Or use the `heroku auth:token` command

2. **`HEROKU_APP_NAME`**: Heroku app name
   - Example: `my-app-name-dev`, `my-app-name-stg`, `my-app-name-prod`

### How to Configure Secrets

1. Navigate to GitHub repository → "Settings" → "Secrets and variables" → "Actions"
2. Click "New repository secret"
3. Create the following secrets for each environment:
   - For `dev` environment: `HEROKU_API_KEY` (for dev), `HEROKU_APP_NAME` (for dev)
   - For `stg` environment: `HEROKU_API_KEY` (for stg), `HEROKU_APP_NAME` (for stg)
   - For `prod` environment: `HEROKU_API_KEY` (for prod), `HEROKU_APP_NAME` (for prod)

## Deployment Steps

**Workflow File**: [`.github/workflows/deploy-heroku.yml`](../../.github/workflows/deploy-heroku.yml)

### Automatic Deployment via Branch Push

Pushing to the following branches will automatically trigger deployments:

- `dev` branch → deploys to dev environment
- `stg` branch → deploys to stg environment
- `main` branch → deploys to prod environment

The workflow is triggered by the `push` event on these branches.

### Manual Deployment (GitHub Actions)

1. Navigate to GitHub repository → "Actions" tab
2. Select the "Deploy to Heroku" workflow
3. Click "Run workflow"
4. Select the environment to deploy (dev, stg, prod)
5. Click "Run workflow" button

## Database Migration Steps

**Workflow File**: [`.github/workflows/migrate-db-heroku.yml`](../../.github/workflows/migrate-db-heroku.yml)

Database migrations are executed manually using GitHub Actions workflows.

### Running Migrations

1. Navigate to GitHub repository → "Actions" tab
2. Select the "Migrate Database on Heroku" workflow
3. Click "Run workflow"
4. Select the environment to run migration (dev, stg, prod)
5. Click "Run workflow" button

### Migration Details

The migration script (`api/migrate_db.py`) performs the following operations:

- Drop existing tables
- Recreate tables

**Warning**: This migration deletes data. 

