---
sidebar_position: 1
title: GitHub + Docusaurus Setup Guide
---

# Personal Notes Site — GitHub + Docusaurus Setup Guide

## Overview

**What you'll get:**
- A docs site with a sidebar and Markdown content
- Every push of a `.md` file to GitHub automatically publishes live
- Free hosting on GitHub Pages at: `https://YOUR-USERNAME.github.io/YOUR-REPO/`

---

## Step 1 — Prerequisites

### 1.1 Install Node.js
Download from: https://nodejs.org (choose the LTS version)

```bash
node -v    # should show v18 or higher
npm -v     # should show 9 or higher
```

### 1.2 Install Git
Download from: https://git-scm.com

```bash
git --version
```

### 1.3 Create a GitHub Account
Sign up at: https://github.com

---

## Step 2 — Create a GitHub Repository

1. Go to https://github.com/new
2. Fill in:
   - **Repository name:** `my-notes`
   - **Visibility:** Public ✅
   - **Initialize with README:** ✅ Yes
3. Click **Create repository**

---

## Step 3 — Create a Docusaurus Project Locally

```bash
npx create-docusaurus@latest my-notes classic --typescript
cd my-notes
npm run start
```

Visit `http://localhost:3000` to preview. Press `Ctrl+C` to stop.

---

## Step 4 — Configure Docusaurus for GitHub Pages

Edit `docusaurus.config.ts`:

```ts
url: 'https://deeptiyadavsd1111.github.io',
baseUrl: '/my-notes/',
organizationName: 'deeptiyadavsd1111',
projectName: 'my-notes',
```

---

## Step 5 — Set Up GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm run build
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./build
```

---

## Step 6 — Connect to GitHub and Push

```bash
git remote add origin https://github.com/YOUR-USERNAME/my-notes.git
git add .
git commit -m "Initial Docusaurus setup"
git branch -M main
git push -u origin main
```

> Skip `git init` if Docusaurus already created a `.git` folder.

---

## Step 7 — Enable GitHub Pages

1. Go to your repo → **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: `gh-pages` / folder: `/ (root)`
4. Click **Save**

Wait 2–3 minutes, then visit: `https://YOUR-USERNAME.github.io/my-notes/` 🎉

---

## Step 8 — Daily Workflow

```bash
# Create a new note
touch docs/aws-notes.md

# Publish
git add .
git commit -m "Add AWS notes"
git push
```

**Note frontmatter format:**

```markdown
---
sidebar_position: 1
title: AWS Notes
---
```

---

## Step 9 — Organize with Folders

```
docs/
├── aws/
│   ├── _category_.json
│   ├── ec2.md
│   └── s3.md
└── general/
    └── intro.md
```

**`_category_.json` format:**

```json
{
  "label": "AWS",
  "position": 1,
  "collapsible": true,
  "collapsed": false
}
```