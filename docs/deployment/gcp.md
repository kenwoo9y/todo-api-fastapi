# Google Cloud Deployment Guide

This document explains how to deploy a FastAPI application to Google Cloud Platform (GCP) and how to run database migrations.

## Table of Contents

1. [GitHub Secrets Configuration](#github-secrets-configuration)
2. [Deployment Steps](#deployment-steps)
3. [Database Migration Steps](#database-migration-steps)

## GitHub Secrets Configuration

To deploy to Google Cloud Platform from GitHub Actions, you need to configure the following secrets.

### Required Secrets

Configure the following secrets for each environment (dev, stg, prod):

1. **`GCP_PROJECT_ID`**: Google Cloud Project ID
   - Obtain from Google Cloud Console → "IAM & Admin" → "Settings"
   - Example: `my-project-id`

2. **`GCP_REGION`**: Google Cloud Region
   - Example: `asia-northeast1`

3. **`ARTIFACT_REGISTRY_REPOSITORY`**: Artifact Registry repository name
   - Example: `my-repository`

4. **`WIF_PROVIDER`**: Workload Identity Federation Provider
   - Format: `projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/POOL_NAME/providers/PROVIDER_NAME`
   - Obtain from Google Cloud Console → "IAM & Admin" → "Workload Identity Federation"

5. **`WIF_SERVICE_ACCOUNT`**: Workload Identity Federation Service Account
   - Format: `SERVICE_ACCOUNT_EMAIL@PROJECT_ID.iam.gserviceaccount.com`
   - Obtain from Google Cloud Console → "IAM & Admin" → "Service Accounts"

6. **`CLOUD_RUN_SERVICE_NAME`**: Cloud Run service name (for database migrations)
   - Example: `todo-api-dev`, `todo-api-stg`, `todo-api-prod`

7. **`SQL_INSTANCE_MYSQL`**: Cloud SQL MySQL instance connection name (for database migrations)
   - Format: `PROJECT_ID:REGION:INSTANCE_NAME`
   - Example: `my-project:asia-northeast1:my-mysql-instance`

8. **`SQL_INSTANCE_POSTGRESQL`**: Cloud SQL PostgreSQL instance connection name (for database migrations)
   - Format: `PROJECT_ID:REGION:INSTANCE_NAME`
   - Example: `my-project:asia-northeast1:my-postgresql-instance`

### How to Configure Secrets

1. Navigate to GitHub repository → "Settings" → "Secrets and variables" → "Actions"
2. Click "New repository secret"
3. Create the following secrets for each environment:
   - For `dev` environment: `GCP_PROJECT_ID`, `GCP_REGION`, `ARTIFACT_REGISTRY_REPOSITORY`, `WIF_PROVIDER`, `WIF_SERVICE_ACCOUNT`, `CLOUD_RUN_SERVICE_NAME`, `SQL_INSTANCE_MYSQL`, `SQL_INSTANCE_POSTGRESQL`
   - For `stg` environment: Same secrets as dev (with appropriate values for staging)
   - For `prod` environment: Same secrets as dev (with appropriate values for production)

**Note**: Some secrets like `GCP_PROJECT_ID` and `GCP_REGION` may be shared across environments, while others like `CLOUD_RUN_SERVICE_NAME` should be environment-specific.

## Deployment Steps

**Workflow File**: `.github/workflows/deploy-gcp.yml`

### Automatic Deployment via Branch Push

Pushing to the following branches will automatically trigger deployments:

- `dev` branch → deploys to dev environment
- `stg` branch → deploys to stg environment
- `main` branch → deploys to prod environment

The workflow is triggered by the `push` event on these branches.

### Manual Deployment (GitHub Actions)

1. Navigate to GitHub repository → "Actions" tab
2. Select the "Deploy to Google Cloud" workflow
3. Click "Run workflow"
4. Select the environment to deploy (dev, stg, prod)
5. Click "Run workflow" button

**Note**: After pushing the Docker image to Artifact Registry, you need to configure Cloud Run to use this image. The workflow only handles building and pushing the image.

## Database Migration Steps

**Workflow File**: `.github/workflows/migrate-db-gcp.yml`

Database migrations are executed manually using GitHub Actions workflows.

### Running Migrations

1. Navigate to GitHub repository → "Actions" tab
2. Select the "Migrate Database on Google Cloud" workflow
3. Click "Run workflow"
4. Select the environment to run migration (dev, stg, prod)
5. Click "Run workflow" button

### Migration Details

The migration script (`api/migrate_db.py`) performs the following operations:

- Drop existing tables
- Recreate tables

**Warning**: This migration deletes data.