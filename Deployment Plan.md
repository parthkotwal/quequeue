# Project State & Deployment Plan for *QueQueue*

## Current State (Development)

* **Frontend**

  * Built with **Vue.js**
  * Fully functional UI for exporting/importing queues, authentication, and queue management
  * Containerized with Docker

* **Backend**

  * Built with **Django (Python)**
  * Handles Spotify API integration, authentication (OAuth), and queue persistence
  * Running on a local **PostgreSQL** database (also containerized)
  * Containerized backend service

* **Database (Dev)**

  * Local PostgreSQL instance in Docker
  * Stores user accounts and queue metadata

* **Other**

  * ML module stubbed in (recommendations via audio features; embeddings in progress)
  * No production deployment yet — running locally via Docker Compose

---

## Ideal Deployment Plan (Balanced AWS + PaaS Approach)

### 1. **Frontend**

* **Deploy Vue.js build artifacts** to **AWS S3** (static hosting)
* Serve via **AWS CloudFront** for global low-latency distribution

### 2. **Backend**

* Deploy Django backend (containerized) to a **PaaS**:
  * Options: **Railway, Render, Fly.io, or Heroku**
  * Handles scaling, health checks, and networking automatically
* Connect backend securely to AWS services (RDS, S3) via environment variables

### 3. **Database**

* Migrate from local Postgres → **Amazon RDS (PostgreSQL)**
* Benefits: backups, monitoring, managed scaling
* Keep schema migrations in source control (e.g., Django migrations)

### 4. **Storage**

* Store user uploaded data in **Amazon S3**
* Backend handles signed URLs for secure access

### 5. **Authentication**

* Continue using Spotify OAuth flow via backend
* Ensure production Spotify app settings are configured (redirect URIs, scopes, etc.)

---

## Deployment Steps (High-Level)

1. **Frontend**

   * `npm run build` → Upload to S3 bucket
   * Configure CloudFront distribution

2. **Backend**

   * Push Dockerized backend to Railway/Render/Fly.io
   * Add environment variables (Spotify API keys, RDS endpoint, S3 bucket info)

3. **Database**

   * Spin up Postgres instance in RDS
   * Apply Django migrations
   * Update backend DB config

4. **Storage**

   * Create S3 bucket for queue JSONs
   * Configure IAM policy for backend access
   * Update backend code to read/write S3

5. **Domain/SSL**

   * Route domain → CloudFront for frontend
   * Backend served via PaaS-provided HTTPS or custom domain

---

**End Result**:

* Frontend served globally (S3 + CloudFront)
* Backend hosted on PaaS (cheap, simple, reliable)
* RDS (Postgres) + S3 (storage) → AWS infra cred
* Clean story for résumé/interviews: “Used AWS managed services (RDS, S3, CloudFront) and lightweight PaaS hosting to balance production readiness with cost and simplicity.