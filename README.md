# QueQueue

QueQueue is a Spotify queue manager app - Vue.js frontend, Django backend, PostgreSQL database, and deployed on AWS. Lets users save and restore Spotify queues with the click of a button. I created this tool because of how annoyed I'd be when a friends interrupted my queue or if I couldn't relive the most perfect gym session or late night drive.

[https://quequeue.app](https://quequeue.app)  

**NOTE: Spotify login will not work unless I add you to the authorized list of users (blame the Spotify API...) Therefore, please watch the video for a tour of the app's core functionalities or reach out to me at parthkotwa07@gmail.com**

## Videos

### 1. App Walkthrough
[![Watch the walkthrough](https://img.youtube.com/vi/hJ-PSDomcfE/maxresdefault.jpg)](https://youtu.be/hJ-PSDomcfE)

A quick demo showing how the app looks and works from a user’s perspective.

---

### 2. Infrastructure Overview
[![Watch the walkthrough](https://img.youtube.com/vi/vKi6S3hv4t0/maxresdefault.jpg)](https://youtu.be/vKi6S3hv4t0)

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
