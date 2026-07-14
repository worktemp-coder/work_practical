# Flask App - DevSecOps Demo

A simple Flask application with Docker, Trivy scanning, and CI/CD.

## Quick Start

```bash
docker compose up --build
```

## Endpoints

- `GET /health` - Health check
- `GET /version` - Version info
- `POST /login` - Login (placeholder)
- `POST /logout` - Logout (placeholder)
- `GET /profile` - Profile (placeholder)

## Security Notes

- `vuln_app.py` contains **intentionally vulnerable code** for SAST/dependency scanning demos only. Do not deploy.
- Sensitive files (`.env`, `apikey.txt`) are gitignored. Use environment variables for real secrets.
# Test PR
