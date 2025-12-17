pipeline {
    agent any

    environment {
        GIT_REPO = "https://github.com/varsha2176/fastapi-mysql-devops.git"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main', url: "${GIT_REPO}"
            }
        }

        stage('Environment Check') {
            steps {
                bat '''
                docker --version
                docker-compose --version
                dir
                '''
            }
        }

        stage('Cleanup') {
            steps {
                bat '''
                docker-compose down
                docker system prune -f
                '''
            }
        }

        stage('Build') {
            steps {
                bat 'docker-compose build'
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                docker-compose up -d
                timeout /t 40 /nobreak
                powershell -Command "Invoke-WebRequest http://localhost:8000/health"
                '''
            }
        }

        stage('Deploy') {
            steps {
                bat '''
                docker-compose down
                docker-compose up -d
                '''
            }
        }

        stage('Verify') {
            steps {
                bat '''
                timeout /t 20 /nobreak
                docker-compose ps
                powershell -Command "Invoke-WebRequest http://localhost:8000/health"
                '''
            }
        }
    }

    post {
        failure {
            bat 'docker-compose logs'
        }
        always {
            bat 'docker ps'
        }
    }
}
