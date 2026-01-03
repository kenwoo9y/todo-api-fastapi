# Microsoft Azure Deployment Guide

This document explains how to deploy a FastAPI application to Microsoft Azure and how to run database migrations.

## Table of Contents

1. [GitHub Secrets Configuration](#github-secrets-configuration)
2. [Deployment Steps](#deployment-steps)
3. [Database Migration Steps](#database-migration-steps)

## GitHub Secrets Configuration

To deploy to Microsoft Azure from GitHub Actions, you need to configure the following secrets.

### Required Secrets

Configure the following secrets for each environment (dev, stg, prod):

1. **`AZURE_CONTAINER_REGISTRY`**: Azure Container Registry name
   - Obtain from Azure Portal → "Container registries"
   - Example: `myregistry`

2. **`AZURE_RESOURCE_GROUP`**: Azure Resource Group name
   - Obtain from Azure Portal → "Resource groups"
   - Example: `my-resource-group`

3. **`AZURE_CLIENT_ID`**: Azure Service Principal Client ID (for OIDC authentication)
   - Obtain from Azure Portal → "Azure Active Directory" → "App registrations" → Select your app → "Overview"
   - Example: `12345678-1234-1234-1234-123456789abc`

4. **`AZURE_TENANT_ID`**: Azure Tenant ID (for OIDC authentication)
   - Obtain from Azure Portal → "Azure Active Directory" → "Overview"
   - Example: `87654321-4321-4321-4321-cba987654321`

5. **`AZURE_SUBSCRIPTION_ID`**: Azure Subscription ID
   - Obtain from Azure Portal → "Subscriptions"
   - Example: `11111111-2222-3333-4444-555555555555`

6. **`CONTAINER_APP_NAME`**: Container Apps service name (for database migrations)
   - Example: `todo-api-dev`, `todo-api-stg`, `todo-api-prod`

7. **`KEY_VAULT_NAME`**: Azure Key Vault name (for database migrations)
   - Obtain from Azure Portal → "Key vaults"
   - Example: `my-key-vault`

8. **`AZURE_MYSQL_SERVER_NAME`**: Azure Database for MySQL server name (for database migrations)
   - Obtain from Azure Portal → "Azure Database for MySQL servers"
   - Example: `my-mysql-server`

9. **`AZURE_POSTGRESQL_SERVER_NAME`**: Azure Database for PostgreSQL server name (for database migrations)
   - Obtain from Azure Portal → "Azure Database for PostgreSQL servers"
   - Example: `my-postgresql-server`

### How to Configure Secrets

1. Navigate to GitHub repository → "Settings" → "Secrets and variables" → "Actions"
2. Click "New repository secret"
3. Create the following secrets for each environment:
   - For `dev` environment: `AZURE_CONTAINER_REGISTRY`, `AZURE_RESOURCE_GROUP`, `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`, `CONTAINER_APP_NAME`, `KEY_VAULT_NAME`, `AZURE_MYSQL_SERVER_NAME`, `AZURE_POSTGRESQL_SERVER_NAME`
   - For `stg` environment: Same secrets as dev (with appropriate values for staging)
   - For `prod` environment: Same secrets as dev (with appropriate values for production)

**Note**: Some secrets like `AZURE_SUBSCRIPTION_ID` and `AZURE_TENANT_ID` may be shared across environments, while others like `CONTAINER_APP_NAME` should be environment-specific.

## Deployment Steps

**Workflow File**: `.github/workflows/deploy-azure.yml`

### Automatic Deployment via Branch Push

Pushing to the following branches will automatically trigger deployments:

- `dev` branch → deploys to dev environment
- `stg` branch → deploys to stg environment
- `main` branch → deploys to prod environment

The workflow is triggered by the `push` event on these branches.

### Manual Deployment (GitHub Actions)

1. Navigate to GitHub repository → "Actions" tab
2. Select the "Deploy to Microsoft Azure" workflow
3. Click "Run workflow"
4. Select the environment to deploy (dev, stg, prod)
5. Click "Run workflow" button

**Note**: After pushing the Docker image to Azure Container Registry, you need to configure Container Apps to use this image. The workflow only handles building and pushing the image.

## Database Migration Steps

**Workflow File**: `.github/workflows/migrate-db-azure.yml`

Database migrations are executed manually using GitHub Actions workflows.

### Running Migrations

1. Navigate to GitHub repository → "Actions" tab
2. Select the "Migrate Database on Microsoft Azure" workflow
3. Click "Run workflow"
4. Select the environment to run migration (dev, stg, prod)
5. Click "Run workflow" button

### Migration Details

The migration script (`api/migrate_db.py`) performs the following operations:

- Drop existing tables
- Recreate tables

**Warning**: This migration deletes data.

The workflow automatically detects whether you're using PostgreSQL or MySQL based on the `DB_TYPE` environment variable in your Container App configuration, and supports both Flexible Server and Single Server deployment models.