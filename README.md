# QueQueue

QueQueue is a Spotify queue manager app - built with a Vue.js frontend and a Django backend.  
It lets users save and restore Spotify queues with the click of a button. 

[https://quequeue.app](https://quequeue.app)  

## Videos

### 1. App Walkthrough
[▶️ Watch the walkthrough](https://quequeue-user-uploads.s3.us-west-2.amazonaws.com/frontend/QueQueue+-+1+October+2025.mp4)

A quick demo showing how the app looks and works from a user’s perspective.

---

### 2. Infrastructure Overview
[▶️ Watch the infra tour](https://quequeue-user-uploads.s3.us-west-2.amazonaws.com/frontend/Infrastructure+Overview+of+quequeue.app.mp4)

An overview of the architecture: CI/CD, S3, CloudFront, Elastic Beanstalk, EC2, RDS, and more.

---

## Tech Stack

**Frontend**
- Vue.js  
- Deployed via S3 + CloudFront  

**Backend**
- Django + Django REST Framework  
- Dockerized and deployed with AWS Elastic Beanstalk  
- Runs on EC2 with Application Load Balancer  

**Storage & Database**
- PostgreSQL (Amazon RDS)  
- S3 buckets for frontend hosting + user uploads  

**CI/CD**
- GitHub Actions → Docker builds → ECR + Beanstalk  

**Integrations**
- Spotify Web API (via SDK)  

---

If you would like to use the app or have feedback, send me an email at parthkotwa07@gmail.com!

