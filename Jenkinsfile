pipeline {
    agent any

    tools {
        // Jenkins > Global Tool Configuration에 설정된 SonarQube Scanner 이름을 사용
        maven 'M3'
        jdk 'jdk17'
    }

    environment {
        SCANNER_HOME = tool 'SonarQubeScanner'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Taegi97/vulnerable-app.git'
            }
        }
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonarqube') {
                    sh ''' $SCANNER_HOME/bin/sonar-scanner \
                        -Dsonar.projectKey=vulnerable-app \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=http://localhost:9000 \
                        -Dsonar.login=squ_2a27b872365d56419798e98218d8e5792949704e '''
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t vulnerable-app:latest .'
                }
            }
        }
        stage('Trivy Scan') {
            steps {
                // Trivy가 HIGH, CRITICAL 취약점을 발견하면 빌드를 실패시킴
                sh 'trivy image --exit-code 1 --severity HIGH,CRITICAL vulnerable-app:latest'
            }
        }
    }
}
