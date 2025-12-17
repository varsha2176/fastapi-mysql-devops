pipeline {
    agent any

    environment {
        PROJECT_NAME = "fastapi-mysql-devops"
        GIT_REPO = "https://github.com/varsha2176/fastapi-mysql-devops.git"
    }

    stages {
        stage('Checkout') {
            steps {
                echo '🔄 Checking out code...'
                git branch: 'main', url: "${GIT_REPO}"
            }
        }

        stage('Environment Check') {
            steps {
                echo '🔍 Checking environment...'
                script {
                    bat 'docker --version'
                    bat 'docker-compose --version'
                }
            }
        }

        stage('Cleanup') {
            steps {
                echo '🧹 Cleaning up...'
                script {
                    try {
                        bat 'docker-compose down'
                    } catch (Exception e) {
                        echo "No containers to clean up"
                    }
                    try {
                        bat 'docker system prune -f'
                    } catch (Exception e) {
                        echo "Prune failed, continuing..."
                    }
                }
            }
        }

        stage('Build') {
            steps {
                echo '🏗️ Building Docker images...'
                bat 'docker-compose build'
            }
        }

        stage('Deploy') {
            steps {
                echo '🚀 Starting services...'
                bat 'docker-compose up -d'
                
                echo '⏳ Waiting for services to initialize (60 seconds)...'
                bat 'powershell -Command "Start-Sleep -Seconds 60"'
            }
        }

        stage('Test') {
            steps {
                echo '🧪 Testing endpoints...'
                script {
                    def maxRetries = 3
                    def retryDelay = 10
                    
                    for (int i = 1; i <= maxRetries; i++) {
                        try {
                            bat '''
                                powershell -Command "$response = Invoke-WebRequest -Uri http://localhost:8000/health -UseBasicParsing -ErrorAction Stop; Write-Host 'Health check passed'; Write-Host $response.Content"
                            '''
                            echo "✅ Health check passed on attempt ${i}"
                            break
                        } catch (Exception e) {
                            if (i == maxRetries) {
                                error("Health check failed after ${maxRetries} attempts")
                            }
                            echo "⚠️ Attempt ${i} failed, retrying in ${retryDelay} seconds..."
                            bat "powershell -Command \"Start-Sleep -Seconds ${retryDelay}\""
                        }
                    }
                }
                
                bat '''
                    powershell -Command "$response = Invoke-WebRequest -Uri http://localhost:8000/ -UseBasicParsing; Write-Host $response.Content"
                    powershell -Command "$response = Invoke-WebRequest -Uri http://localhost:8000/db/users -UseBasicParsing; Write-Host $response.Content"
                '''
            }
        }

        stage('Verify') {
            steps {
                echo '✅ Verifying deployment...'
                bat 'docker-compose ps'
                bat 'docker ps'
            }
        }
    }

    post {
        success {
            echo '''
                ========================================
                ✅ DEPLOYMENT SUCCESSFUL
                ========================================
                API: http://localhost:8000
                Health: http://localhost:8000/health
                Users: http://localhost:8000/db/users
                Tables: http://localhost:8000/db/tables
                ========================================
            '''
        }
        failure {
            echo '❌ Pipeline failed! Showing logs...'
            bat '''
                docker-compose logs --tail=50
                docker ps -a
            '''
        }
        always {
            echo '📊 Container Status:'
            bat 'docker ps'
        }
    }
}