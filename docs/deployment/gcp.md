# Google Cloud Deployment Guide

This document explains how to deploy a FastAPI application to Google Cloud and how to run database migrations.

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

---
このドキュメントでは、FastAPIアプリケーションをGoogle Cloudにデプロイする方法と、データベースマイグレーションを実行する方法について説明する。

## 目次

1. [GitHub Secrets設定](#github-secrets設定)
2. [デプロイメント手順](#デプロイメント手順)
3. [データベースマイグレーション手順](#データベースマイグレーション手順)

## GitHub Secrets設定

GitHub ActionsからGoogle Cloud Platformにデプロイするには、以下のシークレットを設定する必要がある。

### 必要なシークレット

各環境（dev、stg、prod）に対して以下のシークレットを設定する：

1. **`GCP_PROJECT_ID`**: Google CloudプロジェクトID
   - Google Cloud Console → 「IAM & Admin」 → 「Settings」から取得
   - 例: `my-project-id`

2. **`GCP_REGION`**: Google Cloudリージョン
   - 例: `asia-northeast1`

3. **`ARTIFACT_REGISTRY_REPOSITORY`**: Artifact Registryリポジトリ名
   - 例: `my-repository`

4. **`WIF_PROVIDER`**: Workload Identity Federationプロバイダー
   - 形式: `projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/POOL_NAME/providers/PROVIDER_NAME`
   - Google Cloud Console → 「IAM & Admin」 → 「Workload Identity Federation」から取得

5. **`WIF_SERVICE_ACCOUNT`**: Workload Identity Federationサービスアカウント
   - 形式: `SERVICE_ACCOUNT_EMAIL@PROJECT_ID.iam.gserviceaccount.com`
   - Google Cloud Console → 「IAM & Admin」 → 「Service Accounts」から取得

6. **`CLOUD_RUN_SERVICE_NAME`**: Cloud Runサービス名（データベースマイグレーション用）
   - 例: `todo-api-dev`, `todo-api-stg`, `todo-api-prod`

7. **`SQL_INSTANCE_MYSQL`**: Cloud SQL MySQLインスタンス接続名（データベースマイグレーション用）
   - 形式: `PROJECT_ID:REGION:INSTANCE_NAME`
   - 例: `my-project:asia-northeast1:my-mysql-instance`

8. **`SQL_INSTANCE_POSTGRESQL`**: Cloud SQL PostgreSQLインスタンス接続名（データベースマイグレーション用）
   - 形式: `PROJECT_ID:REGION:INSTANCE_NAME`
   - 例: `my-project:asia-northeast1:my-postgresql-instance`

### シークレットの設定方法

1. GitHubリポジトリ → 「Settings」 → 「Secrets and variables」 → 「Actions」に移動
2. 「New repository secret」をクリック
3. 各環境に対して以下のシークレットを作成：
   - `dev`環境用: `GCP_PROJECT_ID`, `GCP_REGION`, `ARTIFACT_REGISTRY_REPOSITORY`, `WIF_PROVIDER`, `WIF_SERVICE_ACCOUNT`, `CLOUD_RUN_SERVICE_NAME`, `SQL_INSTANCE_MYSQL`, `SQL_INSTANCE_POSTGRESQL`
   - `stg`環境用: devと同じシークレット（ステージング環境用の適切な値）
   - `prod`環境用: devと同じシークレット（本番環境用の適切な値）

**注意**: `GCP_PROJECT_ID`や`GCP_REGION`などの一部のシークレットは環境間で共有される場合があるが、`CLOUD_RUN_SERVICE_NAME`などの他のシークレットは環境固有である必要がある。

## デプロイメント手順

**ワークフローファイル**: `.github/workflows/deploy-gcp.yml`

### ブランチプッシュによる自動デプロイメント

以下のブランチにプッシュすると、自動的にデプロイメントがトリガーされる：

- `dev`ブランチ → dev環境にデプロイ
- `stg`ブランチ → stg環境にデプロイ
- `main`ブランチ → prod環境にデプロイ

これらのブランチでの`push`イベントによってワークフローがトリガーされる。

### 手動デプロイメント（GitHub Actions）

1. GitHubリポジトリ → 「Actions」タブに移動
2. 「Deploy to Google Cloud」ワークフローを選択
3. 「Run workflow」をクリック
4. デプロイする環境を選択（dev、stg、prod）
5. 「Run workflow」ボタンをクリック

**注意**: DockerイメージをArtifact Registryにプッシュした後、Cloud Runでこのイメージを使用するように設定する必要がある。ワークフローはイメージのビルドとプッシュのみを処理する。

## データベースマイグレーション手順

**ワークフローファイル**: `.github/workflows/migrate-db-gcp.yml`

データベースマイグレーションは、GitHub Actionsワークフローを使用して手動で実行される。

### マイグレーションの実行

1. GitHubリポジトリ → 「Actions」タブに移動
2. 「Migrate Database on Google Cloud」ワークフローを選択
3. 「Run workflow」をクリック
4. マイグレーションを実行する環境を選択（dev、stg、prod）
5. 「Run workflow」ボタンをクリック

### マイグレーションの詳細

マイグレーションスクリプト（`api/migrate_db.py`）は以下の操作を実行する：

- 既存のテーブルを削除
- テーブルを再作成

**警告**: このマイグレーションはデータを削除する。
