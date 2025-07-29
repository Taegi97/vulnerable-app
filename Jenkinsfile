pipeline {
    agent any

    tools {
        jdk 'jdk17'
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
                        // SONAR_TOKEN 환경 변수가 자동으로 주입되므로 -Dsonar.login 부분은 제거합니다.
                        sh "'${scannerHome}/bin/sonar-scanner' \
                            -Dsonar.projectKey=vulnerable-app \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=http://localhost:9000"
                    }
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
