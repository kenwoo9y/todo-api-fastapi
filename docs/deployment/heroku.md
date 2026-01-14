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

**Workflow File**: `.github/workflows/deploy-heroku.yml`

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

**Workflow File**: `.github/workflows/migrate-db-heroku.yml`

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

---
このドキュメントでは、FastAPIアプリケーションをHerokuにデプロイする方法と、データベースマイグレーションを実行する方法について説明する。

## 目次

1. [GitHub Secrets設定](#github-secrets設定)
2. [デプロイメント手順](#デプロイメント手順)
3. [データベースマイグレーション手順](#データベースマイグレーション手順)

## GitHub Secrets設定

GitHub ActionsからHerokuにデプロイするには、以下のシークレットを設定する必要がある。

### 必要なシークレット

各環境（dev、stg、prod）に対して以下のシークレットを設定する：

1. **`HEROKU_API_KEY`**: Heroku APIキー
   - Herokuダッシュボード → 「アカウント設定」 → 「APIキー」から取得
   - または `heroku auth:token` コマンドを使用

2. **`HEROKU_APP_NAME`**: Herokuアプリ名
   - 例: `my-app-name-dev`, `my-app-name-stg`, `my-app-name-prod`

### シークレットの設定方法

1. GitHubリポジトリ → 「Settings」 → 「Secrets and variables」 → 「Actions」に移動
2. 「New repository secret」をクリック
3. 各環境に対して以下のシークレットを作成：
   - `dev`環境用: `HEROKU_API_KEY` (dev用), `HEROKU_APP_NAME` (dev用)
   - `stg`環境用: `HEROKU_API_KEY` (stg用), `HEROKU_APP_NAME` (stg用)
   - `prod`環境用: `HEROKU_API_KEY` (prod用), `HEROKU_APP_NAME` (prod用)

## デプロイメント手順

**ワークフローファイル**: `.github/workflows/deploy-heroku.yml`

### ブランチプッシュによる自動デプロイメント

以下のブランチにプッシュすると、自動的にデプロイメントがトリガーされる：

- `dev`ブランチ → dev環境にデプロイ
- `stg`ブランチ → stg環境にデプロイ
- `main`ブランチ → prod環境にデプロイ

これらのブランチでの`push`イベントによってワークフローがトリガーされる。

### 手動デプロイメント（GitHub Actions）

1. GitHubリポジトリ → 「Actions」タブに移動
2. 「Deploy to Heroku」ワークフローを選択
3. 「Run workflow」をクリック
4. デプロイする環境を選択（dev、stg、prod）
5. 「Run workflow」ボタンをクリック

## データベースマイグレーション手順

**ワークフローファイル**: `.github/workflows/migrate-db-heroku.yml`

データベースマイグレーションは、GitHub Actionsワークフローを使用して手動で実行される。

### マイグレーションの実行

1. GitHubリポジトリ → 「Actions」タブに移動
2. 「Migrate Database on Heroku」ワークフローを選択
3. 「Run workflow」をクリック
4. マイグレーションを実行する環境を選択（dev、stg、prod）
5. 「Run workflow」ボタンをクリック

### マイグレーションの詳細

マイグレーションスクリプト（`api/migrate_db.py`）は以下の操作を実行する：

- 既存のテーブルを削除
- テーブルを再作成

**注意**: このマイグレーションはデータを削除する。
