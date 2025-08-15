<p align="center">
  <img src="web/assets/TechEX_dark.png" alt="TechEX Logo" width="420" />
</p>

## TechEX — Parcel Management System

TechEX is a modern, single-repo app for tracking parcels and visualizing basic stats. It ships with a Flask backend, a Vite/Tailwind UI, and an AWS deploy path that runs behind an Application Load Balancer. It’s intentionally simple so you can read it in one sitting (coffee optional, recommended).

### What’s inside
- **Web app**: Flask + Vite + Tailwind/DaisyUI (served on port 5000)
- **Docker**: Production image that builds assets and runs the app
- **AWS**: CloudFormation stack (VPC, ALB, ASG) + a script that builds/pushes the image to ECR and deploys

### Quick start (local)

- Python deps:
  ```bash
  cd web
  pip install -r requirements.txt
  ```
- Frontend deps and build: 
  ```bash
  npm install
  npm run build
  ```
- Run locally:
  ```bash
  python build.py
  # open http://localhost:5000
  ```

### Quick start Docker: (Recommended)

```bash
# from repo root
docker build -f docker/Dockerfile -t techex-web .
docker run -p 5000:5000 techex-web
```
### Deploy to AWS (ECR + ALB)
Head to `aws/README.md` for the full guide.
- The deployment script builds the image locally, pushes to **ECR**, and deploys a stack that pulls the image in an **Auto Scaling Group** behind an **ALB**.
- Sandbox friendly: uses the pre-created `LabInstanceProfile`. No custom IAM needed (Like I could have even made them...).

### Repository map
- `aws/` — CloudFormation (`cf-techex.yaml`) and deployment script (`deploy-techex.ps1`)
- `docker/` — Dockerfile and startup script
- `python/` — The original app in cli mode
- `web/` — Flask app, templates, static assets, build script

### Health checks
- App health endpoint: `GET /health` → 200 JSON
- ALB Target Group health check path: `/health`

### Notes
- Keep instances small in sandbox (t3.micro/t3.small). The script knows.
- The UI has a dark theme. Because of course it does.

---
Built with care and a few emojis. If something breaks, it probably just the sandbox of the aws (or logs).