pipeline {
    agent any

    environment {
        PROJECT_NAME = "fastapi-mysql-devops"
        DOCKER_COMPOSE_FILE = "docker-compose.yml"
        GIT_REPO = "https://github.com/YOUR_USERNAME/fastapi-mysql-devops.git"
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
                sh '''
                    echo "Docker version:"
                    docker --version
                    echo "Docker Compose version:"
                    docker-compose --version
                    echo "Current directory:"
                    pwd
                    echo "Files in directory:"
                    ls -la
                '''
            }
        }

        stage('Cleanup Old Containers') {
            steps {
                echo '🧹 Cleaning up old containers...'
                sh '''
                    docker-compose down || true
                    docker system prune -f || true
                '''
            }
        }

        stage('Build Docker Images') {
            steps {
                echo '🏗️ Building Docker images...'
                sh 'docker-compose build --no-cache'
            }
        }

        stage('Run Tests') {
            steps {
                echo '🧪 Running tests...'
                sh '''
                    # Start services
                    docker-compose up -d
                    
                    # Wait for services to be ready
                    sleep 30
                    
                    # Test API endpoint
                    curl -f http://localhost:8000/ || exit 1
                    curl -f http://localhost:8000/health || exit 1
                    
                    echo "✅ Tests passed!"
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo '🚀 Deploying application...'
                sh '''
                    docker-compose down
                    docker-compose up -d
                    echo "✅ Deployment complete!"
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                echo '✅ Verifying deployment...'
                sh '''
                    sleep 20
                    docker-compose ps
                    curl -f http://localhost:8000/health || exit 1
                    echo "✅ Application is running successfully!"
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
            sh 'docker-compose logs'
        }
        always {
            echo '🔍 Showing running containers...'
            sh 'docker ps'
        }
    }
}