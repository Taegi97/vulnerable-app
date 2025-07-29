pipeline {
    agent any

    tools {
        jdk 'jdk17'
        maven 'M3'
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
                    script {
                        def scannerHome = tool 'SonarQubeScanner'
                        // 셸 스크립트를 """ (Triple double quotes)로 감싸서 문법 오류 가능성을 최소화합니다.
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=vulnerable-app \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=http://localhost:9000
                        """
                    }
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t vulnerable-app:latest .'
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
