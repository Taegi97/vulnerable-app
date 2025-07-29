pipeline {
    agent any

    tools {
        // 젠킨스가 JDK 17을 미리 다운로드하도록 준비시킵니다.
        jdk 'jdk17'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Taegi97/vulnerable-app.git'
            }
        }

        stage('Run Security Scans') {
            steps {
                withSonarQubeEnv('sonarqube') {
                    script {
                        // JDK 17의 실제 설치 경로를 변수에 저장합니다.
                        def jdk17_path = tool 'jdk17'
                        def scannerHome = tool 'SonarQubeScanner'

                        // 셸 스크립트를 실행하기 전에,
                        // JAVA_HOME과 PATH 환경 변수를 JDK 17로 직접 덮어씁니다.
                        // 이것이 가장 확실하게 Java 버전을 지정하는 방법입니다.
                        sh """
                            export JAVA_HOME="${jdk17_path}"
                            export PATH="${jdk17_path}/bin:\$PATH"

                            echo "--- Using Java Version ---"
                            java -version

                            echo "--- Running SonarQube Scanner ---"
                            ${scannerHome}/bin/sonar-scanner \
                                -Dsonar.projectKey=vulnerable-app \
                                -Dsonar.sources=.
                        """
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
