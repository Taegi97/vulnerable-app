pipeline {
    // [수정!] 파이프라인 전체가 jdk17 도구를 사용하는 환경에서 실행되도록 설정합니다.
    agent {
        any {
            tools {
                jdk 'jdk17'
            }
        }
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
                        sh "'${scannerHome}/bin/sonar-scanner' -Dsonar.projectKey=vulnerable-app -Dsonar.sources=."
                    }
                }
            }
        }

        stage('Build and Scan Image') {
            steps {
                sh 'docker build -t vulnerable-app:latest .'
                sh 'trivy image --exit-code 1 --severity HIGH,CRITICAL vulnerable-app:latest'
            }
        }
    }
}
