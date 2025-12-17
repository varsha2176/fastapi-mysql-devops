# 🚀 FastAPI + MySQL CI/CD DevOps Project

A complete production-ready DevOps project demonstrating a two-tier application using **FastAPI** and **MySQL**, containerized with **Docker**, orchestrated with **Docker Compose**, and deployed via **Jenkins CI/CD pipeline** to **AWS EC2**.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Jenkins Setup](#jenkins-setup)
- [AWS EC2 Deployment](#aws-ec2-deployment)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)

## ✨ Features

- ✅ RESTful API with FastAPI
- ✅ MySQL database with initialization scripts
- ✅ Docker containerization
- ✅ Docker Compose orchestration
- ✅ Jenkins CI/CD pipeline
- ✅ Health check endpoints
- ✅ Database connection retry logic
- ✅ CORS enabled
- ✅ Production-ready error handling

## 🛠 Tech Stack

- **Backend:** Python 3.11, FastAPI
- **Database:** MySQL 8.0
- **Containerization:** Docker, Docker Compose
- **CI/CD:** Jenkins
- **Cloud:** AWS EC2
- **Version Control:** Git, GitHub

## 🏗 Architecture
```
┌─────────────┐      ┌─────────────┐
│   FastAPI   │◄────►│    MySQL    │
│  (Port 8000)│      │  (Port 3306)│
└─────────────┘      └─────────────┘
       │                    │
       └────────┬───────────┘
                │
         Docker Network
                │
         ┌──────▼──────┐
         │   Jenkins   │
         │   CI/CD     │
         └─────────────┘
```

## 📦 Prerequisites

- Docker (v20.10+)
- Docker Compose (v2.0+)
- Git
- Python 3.11+ (for local development)
- Jenkins (optional, for CI/CD)
- AWS EC2 instance (for deployment)

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/fastapi-mysql-devops.git
cd fastapi-mysql-devops
```

### 2. Start Services
```bash
# Build and start all services
docker-compose up --build -d

# Check running containers
docker-compose ps

# View logs
docker-compose logs -f
```

### 3. Test Application
```bash
# Health check
curl http://localhost:8000/

# Database health
curl http://localhost:8000/health

# Get all users
curl http://localhost:8000/db/users

# Get database tables
curl http://localhost:8000/db/tables
```

### 4. Stop Services
```bash
docker-compose down

# Stop and remove volumes (⚠️ deletes database data)
docker-compose down -v
```

## 🔧 Jenkins Setup

### 1. Install Jenkins on EC2
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Java
sudo apt install -y openjdk-11-jdk

# Install Jenkins
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt update
sudo apt install -y jenkins

# Start Jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins
```

### 2. Install Docker
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add Jenkins user to Docker group
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### 3. Install Docker Compose
```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 4. Configure Jenkins Pipeline

1. Open Jenkins: `http://YOUR_EC2_IP:8080`
2. Create New Item → Pipeline
3. Configure:
   - **Pipeline Definition:** Pipeline script from SCM
   - **SCM:** Git
   - **Repository URL:** Your GitHub repo URL
   - **Branch:** main
   - **Script Path:** Jenkinsfile
4. Save and Build

## ☁️ AWS EC2 Deployment

### 1. Launch EC2 Instance

- **AMI:** Ubuntu 22.04 LTS
- **Instance Type:** t2.medium (minimum)
- **Security Group:**
  - Port 22 (SSH)
  - Port 8000 (FastAPI)
  - Port 8080 (Jenkins)
  - Port 3306 (MySQL - optional, for remote access)

### 2. Connect and Setup
```bash
# SSH into EC2
ssh -i your-key.pem ubuntu@YOUR_EC2_IP

# Install prerequisites
sudo apt update
sudo apt install -y git docker.io docker-compose

# Clone and deploy
git clone https://github.com/YOUR_USERNAME/fastapi-mysql-devops.git
cd fastapi-mysql-devops
docker-compose up -d
```

### 3. Access Application

- **API:** `http://YOUR_EC2_IP:8000`
- **Jenkins:** `http://YOUR_EC2_IP:8080`

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint / health check |
| GET | `/health` | Detailed health check with DB status |
| GET | `/db/tables` | List all database tables |
| GET | `/db/users` | Get all users |
| POST | `/db/users?name=NAME&email=EMAIL` | Create new user |

### Example API Calls
```bash
# Create user
curl -X POST "http://localhost:8000/db/users?name=Alice&email=alice@example.com"

# Get users
curl http://localhost:8000/db/users
```

## 📁 Project Structure
```
fastapi-mysql-devops/
│
├── app/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile           # Docker image for FastAPI
│   └── __init__.py          # Python package marker
│
├── db/
│   └── init.sql             # Database initialization
│
├── docker-compose.yml       # Multi-service orchestration
├── Jenkinsfile              # CI/CD pipeline definition
├── .gitignore               # Git ignore rules
└── README.md                # Project documentation
```

## 🔍 Troubleshooting

### Container Issues
```bash
# View logs
docker-compose logs app
docker-compose logs db

# Restart services
docker-compose restart

# Rebuild from scratch
docker-compose down -v
docker-compose up --build
```

### Database Connection Issues
```bash
# Check MySQL is running
docker-compose exec db mysql -u root -prootpassword -e "SHOW DATABASES;"

# Check network
docker network ls
docker network inspect fastapi-mysql-devops_app-network
```

## 📝 License

MIT License

## 👤 Author

Your Name - [GitHub](https://github.com/YOUR_USERNAME)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

---

**⭐ If you like this project, please give it a star on GitHub!**