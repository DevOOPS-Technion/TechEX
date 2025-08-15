# TechEX Docker

This folder contains the production-ready Docker image for the TechEX web app.

## What the image does
- Uses Ubuntu 24.04 base
- Installs Python 3 and Node.js (24)
- Installs Python and Node dependencies
- Builds frontend assets with Vite/Tailwind
- Runs the Flask app on port 5000 using `docker/start.sh`

## Files
- `Dockerfile` — builds the final image
- `start.sh` — startup script used by the container (builds CSS and runs Flask via `web/build.py`)

## Build locally
From the repository root:
```bash
# Build
docker build -f docker/Dockerfile -t techex-web .

# Run
docker run --rm -p 5000:5000 techex-web
# open http://localhost:5000
```

## Environment
The app defaults to port `5000` and binds to `0.0.0.0`. No extra env vars are required for the demo.

## Using with AWS
The AWS deployment flow (see `aws/README.md`) builds this same image locally, pushes it to **ECR**, and deploys EC2 instances behind an **ALB** that pull and run the image.

## Troubleshooting
- Build fails on Node install: ensure your network can fetch from GitHub and nodejs.org.
- CSS not appearing: make sure the Vite build step runs (it does during the Docker build); `web/build.py` also builds once on container start.
- Port already in use: change host port on `docker run -p <host>:5000 techex-web`.

---
If the container starts but the ALB health check is failing, try hitting `/health` locally first to confirm the app is up.
