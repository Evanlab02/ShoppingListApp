# Actions - Build

This file (`./github/workflows/build.yml`) defines the CI/CD workflow for building and testing various components of the application.

## Reference (Asof 2024/12/11)

```yaml
name: Build

on:
  pull_request:
    branches: [trunk]
  push:
    branches: [trunk]

permissions:
  contents: read

env:
  UV_SYSTEM_PYTHON: 1

jobs:
  static-files-build:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: backend
    steps:
      - uses: actions/checkout@v4

      - name: Load .env file
        uses: aarcangeli/load-dotenv@v1.0.0
        with:
          path: ""
          filenames: |
            .env.template
          quiet: false
          if-file-not-found: error

      - name: Set up Python 3.12
        uses: actions/setup-python@v4
        with:
          python-version: "3.12"

      - name: Set up uv
        uses: astral-sh/setup-uv@v4
        with:
          enable-cache: true
          cache-dependency-glob: "backend/requirements.txt"

      - name: Install dependencies
        run: |
          uv pip install -r requirements.txt

      - name: Create/Build Static Files
        run: |
          python manage.py collectstatic --no-input

  assets-files-build:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: frontend
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: "20.17.0"
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Setup
        run: |
          npm ci

      - name: Create/Build FE assets
        run: |
          npm run build

  docker-images-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker Images
        run: |
          docker build -f docker/admin/Dockerfile -t shopping-app .
          docker build -f docker/server/Dockerfile -t shopping-app-admin .
          docker build -f docker/site/Dockerfile -t shopping-app-site .
```

## Purpose

* **Verify Build Integrity:** Ensure all builds (Django backend static files, React dashboard, Docker images) complete successfully without errors.

## Trigger Conditions

This workflow is triggered by:

* **Pull Requests:** On any pull request targeting the `trunk` branch.
* **Pushes:** On any push or merge to the `trunk` branch.

**NOTE:** Successful execution of this workflow is mandatory for all pull requests.

## Jobs

### 1. Django Static Files Build

* **Platform:** Ubuntu Latest
* **Steps:**
    1. **Checkout Code:** Check out the repository.
    2. **Load Environment:** Load environment variables from `.env.template`.
    3. **Set up Python:** Install Python 3.12.
    4. **Install Dependencies:** Install project dependencies using `uv pip` (for compatibility with the backend's `uv` environment).
    5. **Build Static Files:** Generate and collect static files using `python manage.py collectstatic`.

**Purpose:** Verify that the Django application can successfully generate and collect static files.

### 2. React Dashboard Assets Build

* **Platform:** Ubuntu Latest
* **Steps:**
    1. **Checkout Code:** Check out the repository.
    2. **Set up Node.js:** Install Node.js version 20.17.0 with npm cache for improved performance.
    3. **Install Dependencies:** Install project dependencies using `npm ci`.
    4. **Build Assets:** Build the React dashboard assets using `npm run build`.

**Purpose:** Ensure that the React dashboard can be built successfully without errors.

### 3. Docker Images Build

* **Platform:** Ubuntu Latest
* **Steps:**
    1. **Checkout Code:** Check out the repository.
    2. **Build Docker Images:** 
        * Build the Admin container image.
        * Build the Backend/API container image.
        * Build the Reverse Proxy/File Server container image.

**Purpose:** Verify that all Docker images can be built successfully from their respective Dockerfiles.
