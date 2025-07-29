pipeline {
    agent any

    // 파이프라인에서 사용할 도구들을 정의합니다.
    tools {
        jdk 'jdk17' // Global Tool Configuration에 설정한 JDK 이름
    }

    environment {
        SONARQUBE_URL = 'http://localhost:9000'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Taegi97/vulnerable-app.git'
            }
        }
        stage('SonarQube Analysis') {
            steps {
                // withSonarQubeEnv 블록을 사용하여 소나큐브 서버 설정을 불러옵니다.
                withSonarQubeEnv('sonarqube') {
                    // sh 단계를 'jdk17' 환경 안에서 실행하도록 합니다.
                    script {
                        def scannerHome = tool 'SonarQubeScanner'
                        sh "'${scannerHome}/bin/sonar-scanner' \
                            -Dsonar.projectKey=vulnerable-app \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=${SONARQUBE_URL} \
                            -Dsonar.login=${credentials('sonarqube-token')}"
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
                sh 'trivy image --exit-code 1 --severity HIGH,CRITICAL vulnerable-app:latest'
            }
        }
    }
}
