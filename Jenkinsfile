pipeline {
    agent any

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
