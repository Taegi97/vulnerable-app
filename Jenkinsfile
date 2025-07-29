pipeline {
    agent any

    tools {
        // 파이프라인이 사용할 도구 목록을 준비합니다.
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
                // withSonarQubeEnv: 소나큐브 서버 주소와 토큰을 환경 변수로 설정해줍니다.
                withSonarQubeEnv('sonarqube') {
                    script {
                        // def jdk: 'jdk17' 도구의 실제 설치 경로를 jdk 변수에 저장합니다.
                        def jdk = tool 'jdk17'
                        // def scannerHome: SonarQubeScanner 도구의 실제 설치 경로를 저장합니다.
                        def scannerHome = tool 'SonarQubeScanner'

                        // withEnv: sh 명령어를 실행할 때만 환경 변수를 일시적으로 변경합니다.
                        // PATH를 우리가 지정한 jdk17의 bin 폴더가 가장 앞에 오도록 설정하여,
                        // 무조건 jdk17의 java를 사용하도록 강제합니다.
                        withEnv(["PATH+JDK=${jdk}/bin"]) {
                            sh "'${scannerHome}/bin/sonar-scanner' \
                                -Dsonar.projectKey=vulnerable-app \
                                -Dsonar.sources=."
                        }
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
                sh 'trivy image --exit-code 1 --severity HIGH,CRITICAL vulnerable-app:latest'
            }
        }
    }
}
