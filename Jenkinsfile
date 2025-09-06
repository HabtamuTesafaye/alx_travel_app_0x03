pipeline {
    agent any

    environment {
        RENDER_API_KEY = credentials('render-api-key') // Store your Render API key in Jenkins credentials
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/your-repo-url.git'
            }
        }

        stage('Build') {
            steps {
                script {
                    docker.image('python:3.11-slim').inside {
                        sh '''
                            pip install --upgrade pip
                            pip install -r requirements.txt
                        '''
                    }
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    docker.image('python:3.11-slim').inside {
                        sh 'pytest'  // Replace with your test command
                    }
                }
            }
        }

        stage('Deploy to Render') {
            steps {
                script {
                    def response = sh(script: """
                        curl -X POST https://api.render.com/deploy/svc/<SERVICE_ID> \
                        -H "Authorization: Bearer ${env.RENDER_API_KEY}" \
                        -H "Content-Type: application/json" \
                        -d '{"clearCache": true}'
                    """, returnStdout: true)
                    echo "Deployment Response: ${response}"
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}