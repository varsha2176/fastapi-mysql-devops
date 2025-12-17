pipeline {
    agent any

    environment {
        PROJECT_NAME = "fastapi-mysql-devops"
        DOCKER_COMPOSE_FILE = "docker-compose.yml"
        GIT_REPO = "https://github.com/varsha2176/fastapi-mysql-devops.git"
    }

    stages {

        stage('Checkout') {
            steps {
                echo '🔄 Checking out code from repository...'
                git branch: 'main', url: "${GIT_REPO}"
            }
        }

        stage('Environment Check') {
            steps {
                echo '🔍 Checking environment...'
                bat '''
                echo Docker version:
                docker --version

                echo Docker Compose version:
                docker-compose --version

                echo Current directory:
                cd

                echo Files in directory:
                dir
                '''
            }
        }

        stage('Cleanup Old Containers') {
            steps {
                echo '🧹 Cleaning up old containers...'
                bat '''
                docker-compose down
                docker system prune -f
                '''
            }
        }

        stage('Build Docker Images') {
            steps {
                echo '🏗️ Building Docker images...'
                bat 'docker-compose build --no-cache'
            }
        }

        stage('Run Tests') {
            steps {
                echo '🧪 Running tests...'
                bat '''
                docker-compose up -d

                echo Waiting for services to be ready...
                timeout /t 30 /nobreak

                curl http://localhost:8000/ || exit /b 1
                curl http://localhost:8000/health || exit /b 1

                echo Tests passed!
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo '🚀 Deploying application...'
                bat '''
                docker-compose down
                docker-compose up -d
                echo Deployment complete!
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                echo '✅ Verifying deployment...'
                bat '''
                timeout /t 20 /nobreak
                docker-compose ps
                curl http://localhost:8000/health || exit /b 1
                echo Application is running successfully!
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }

        failure {
            echo '❌ Pipeline failed!'
            bat 'docker-compose logs'
        }

        always {
            echo '🔍 Showing running containers...'
            bat 'docker ps'
        }
    }
}
