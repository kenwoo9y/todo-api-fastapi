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

---
このドキュメントでは、FastAPIアプリケーションをMicrosoft Azureにデプロイする方法と、データベースマイグレーションを実行する方法について説明する。

## 目次

1. [GitHub Secrets設定](#github-secrets設定)
2. [デプロイメント手順](#デプロイメント手順)
3. [データベースマイグレーション手順](#データベースマイグレーション手順)

## GitHub Secrets設定

GitHub ActionsからMicrosoft Azureにデプロイするには、以下のシークレットを設定する必要がある。

### 必要なシークレット

各環境（dev、stg、prod）に対して以下のシークレットを設定する：

1. **`AZURE_CONTAINER_REGISTRY`**: Azure Container Registry名
   - Azure Portal → 「Container registries」から取得
   - 例: `myregistry`

2. **`AZURE_RESOURCE_GROUP`**: Azureリソースグループ名
   - Azure Portal → 「Resource groups」から取得
   - 例: `my-resource-group`

3. **`AZURE_CLIENT_ID`**: AzureサービスプリンシパルのクライアントID（OIDC認証用）
   - Azure Portal → 「Azure Active Directory」 → 「App registrations」 → アプリを選択 → 「Overview」から取得
   - 例: `12345678-1234-1234-1234-123456789abc`

4. **`AZURE_TENANT_ID`**: AzureテナントID（OIDC認証用）
   - Azure Portal → 「Azure Active Directory」 → 「Overview」から取得
   - 例: `87654321-4321-4321-4321-cba987654321`

5. **`AZURE_SUBSCRIPTION_ID`**: AzureサブスクリプションID
   - Azure Portal → 「Subscriptions」から取得
   - 例: `11111111-2222-3333-4444-555555555555`

6. **`CONTAINER_APP_NAME`**: Container Appsサービス名（データベースマイグレーション用）
   - 例: `todo-api-dev`, `todo-api-stg`, `todo-api-prod`

7. **`KEY_VAULT_NAME`**: Azure Key Vault名（データベースマイグレーション用）
   - Azure Portal → 「Key vaults」から取得
   - 例: `my-key-vault`

8. **`AZURE_MYSQL_SERVER_NAME`**: Azure Database for MySQLサーバー名（データベースマイグレーション用）
   - Azure Portal → 「Azure Database for MySQL servers」から取得
   - 例: `my-mysql-server`

9. **`AZURE_POSTGRESQL_SERVER_NAME`**: Azure Database for PostgreSQLサーバー名（データベースマイグレーション用）
   - Azure Portal → 「Azure Database for PostgreSQL servers」から取得
   - 例: `my-postgresql-server`

### シークレットの設定方法

1. GitHubリポジトリ → 「Settings」 → 「Secrets and variables」 → 「Actions」に移動
2. 「New repository secret」をクリック
3. 各環境に対して以下のシークレットを作成：
   - `dev`環境用: `AZURE_CONTAINER_REGISTRY`, `AZURE_RESOURCE_GROUP`, `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID`, `CONTAINER_APP_NAME`, `KEY_VAULT_NAME`, `AZURE_MYSQL_SERVER_NAME`, `AZURE_POSTGRESQL_SERVER_NAME`
   - `stg`環境用: devと同じシークレット（ステージング環境用の適切な値）
   - `prod`環境用: devと同じシークレット（本番環境用の適切な値）

**注意**: `AZURE_SUBSCRIPTION_ID`や`AZURE_TENANT_ID`などの一部のシークレットは環境間で共有される場合があるが、`CONTAINER_APP_NAME`などの他のシークレットは環境固有である必要がある。

## デプロイメント手順

**ワークフローファイル**: `.github/workflows/deploy-azure.yml`

### ブランチプッシュによる自動デプロイメント

以下のブランチにプッシュすると、自動的にデプロイメントがトリガーされる：

- `dev`ブランチ → dev環境にデプロイ
- `stg`ブランチ → stg環境にデプロイ
- `main`ブランチ → prod環境にデプロイ

これらのブランチでの`push`イベントによってワークフローがトリガーされる。

### 手動デプロイメント（GitHub Actions）

1. GitHubリポジトリ → 「Actions」タブに移動
2. 「Deploy to Microsoft Azure」ワークフローを選択
3. 「Run workflow」をクリック
4. デプロイする環境を選択（dev、stg、prod）
5. 「Run workflow」ボタンをクリック

**注意**: DockerイメージをAzure Container Registryにプッシュした後、Container Appsでこのイメージを使用するように設定する必要がある。ワークフローはイメージのビルドとプッシュのみを処理する。

## データベースマイグレーション手順

**ワークフローファイル**: `.github/workflows/migrate-db-azure.yml`

データベースマイグレーションは、GitHub Actionsワークフローを使用して手動で実行される。

### マイグレーションの実行

1. GitHubリポジトリ → 「Actions」タブに移動
2. 「Migrate Database on Microsoft Azure」ワークフローを選択
3. 「Run workflow」をクリック
4. マイグレーションを実行する環境を選択（dev、stg、prod）
5. 「Run workflow」ボタンをクリック

### マイグレーションの詳細

マイグレーションスクリプト（`api/migrate_db.py`）は以下の操作を実行する：

- 既存のテーブルを削除
- テーブルを再作成

**警告**: このマイグレーションはデータを削除する。
