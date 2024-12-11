# Actions - Build

This file (`./github/workflows/build.yml`) is responsible for checking all builds work as expected and have no failures.

This will be the builds for:

- The Django backend static files.
- The React dashboard.
- The images for the
    - Admin container 
    - Backend / API
    - Reverse proxy / file server.

## When does it run

```yaml
on:
  pull_request:
    branches: [trunk]
  push:
    branches: [trunk]
```

This action will run on:

- Every PR that is set to be merged into trunk
- Every push/merge into trunk.

**NOTE: The jobs from this file are required on PRs.**

## Jobs

### 