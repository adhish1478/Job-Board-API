# 🧰 Job Board API

A full-featured backend API for a Job Board application built using Django and Django REST Framework.  
It supports user registration with email verification, job postings, job applications, and is production-ready with Docker, CI/CD, and AWS deployment.

![CI](https://github.com/adhish1478/Job-Board-API/actions/workflows/ci.yml/badge.svg)

---

## 🔗 Live Demo

📍 **API Base URL**: `http://56.228.30.131:8000/api/`

---

## 🚀 Features

- 🔐 JWT Authentication (Login/Register/Refresh)
- ✅ Email verification system
- 👤 Role-based user profiles (Recruiter & Job Seeker)
- 📄 Recruiter can create, update, delete jobs
- 📌 Job seeker can apply to jobs and view applications
- ⚙️ Django + PostgreSQL + Redis + Celery stack
- 📦 Dockerized for consistent development
- ☁️ Deployed on AWS EC2
- 🔁 CI/CD with GitHub Actions
- 🧪 Unit tests included

---

## 🛠️ Tech Stack

| Tool | Description |
|------|-------------|
| Django & DRF | Core backend + REST API |
| PostgreSQL | Relational database |
| Redis | Message broker for Celery |
| Celery | Asynchronous task queue |
| Docker | Containerization |
| AWS EC2 | Cloud hosting |
| GitHub Actions | CI/CD Pipeline |
| pytest / TestCase | Unit testing framework |

---

## 📁 Project Structure

```bash
Job-Board-API/
├── accounts/              # User registration, JWT, profiles
├── jobs/                  # Job posting CRUD
├── applications/          # Job applications
├── job_board/             # Project settings and URLs
├── docker-compose.yml     # Multi-container Docker setup
├── Dockerfile             # Web container build config
├── wait-for-db.sh         # Waits for DB before starting app
├── .github/workflows/     # CI/CD pipeline config
└── README.md
```
---

## 🧪 Running Tests
```
# Run test cases inside Docker
docker-compose exec web python manage.py test
```
Test cases included for:
	•	✅ User Registration
	•	🔐 JWT Token generation
 
---

## 🐳 Running Locally with Docker
```
# Build and run containers
docker-compose up --build

# Access API
http://localhost:8000/api/
```
⚠️ Make sure to create a .env file in the root directory with the required variables.

---

## ☁️ Deployment: AWS EC2 + GitHub Actions
	•	CI/CD automatically runs on every push to main
	•	Code gets deployed to AWS EC2 using SSH and Docker Compose
	•	Manual setup required for EC2:
	  •	Expose ports 22 & 8000
	  •	Upload your .env file manually on the server
	  •	Add key.pem for GitHub SSH access

---

## 🔐 Environment Variables
Example .env file:
```
# Email Configuration
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Database Configuration
POSTGRES_DB=Job_Board_CustomUser
POSTGRES_USER=postgres
POSTGRES_PASSWORD=1234
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Django Secret Key
DJANGO_SECRET_KEY=your-django-secret-key
```

---

## 🧩 API Endpoints
### 🔑 Accounts
	•	POST /api/register/ – Register user
	•	POST /api/token/ – Obtain JWT
	•	POST /api/token/refresh/ – Refresh token
	•	GET /api/profile/ – Get user profile
	•	POST /api/verify-email/ – Verify user email
	•	POST /api/resend-verification/ – Resend verification email
### 💼 Jobs
	•	GET/POST /api/recruiter/jobs/ – List or create jobs
	•	GET/PUT/DELETE /api/recruiter/jobs/<id>/ – Update/delete job
	•	GET /api/jobs/ – List public jobs (filtered)
### 📥 Applications
	•	POST /api/apply/<job_id>/ – Apply to a job
	•	GET /api/my-applications/ – View my applications
	•	GET /api/recruiter/jobs/<job_id>/applicants/ – Recruiter sees applicants

 ---

 ## 🧠 Future Enhancements
  - 🧠 ML-based Job Recommendations for users  
  - 📊 ATS Scanner for recruiters to assess resume scores
  - 🛡️ Nginx + Gunicorn for production deployment
  - 📂 AWS S3 integration for media files  
  - 🔁 Password reset via email  
  - 🧭 Admin dashboard with analytics  
   

 ---

 ## 📬 Contact
 Adhish Aravind
📧 adhisharavind01@gmail.com
🌐 GitHub: adhish1478
