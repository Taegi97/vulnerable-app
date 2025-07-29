

# DevSecOps Pipeline & AWS Infrastructure Hardening Project

## 1\. 프로젝트 개요 (Overview)

본 프로젝트는 개발팀으로부터 전달받은 초기 클라우드 인프라 코드(Terraform)에 존재하는 보안 취약점을 분석하고, 이를 개선하여 안전한 인프라를 재구축하는 것을 목표로 합니다. 또한, 코드와 컨테이너 이미지에 취약점이 있을 경우 자동으로 배포를 차단하는 DevSecOps CI/CD 파이프라인을 Jenkins, SonarQube, Trivy를 이용해 구축하여 애플리케이션 배포 수명 주기 전반의 보안을 강화했습니다.

## 2\. 아키텍처 다이어그램 (Architecture Diagram)

프로젝트의 전체 아키텍처는 다음과 같습니다.

![Architecture Diagram](https://github.com/Taegi97/vulnerable-app/blob/506f4a8637f63b3dde6cb2535a534641d68b997c/RLHVRnj547_VJp7a0P98lee_KAYggevTqW1ftPnf7n2Azkx6zkAxtMDtpy52aH1FIFG1X08lVYW2YJxq8MehfPNA5xAFxy3ihS_EoNc8l3VpcvdVp6ycjutbsXPPojwo8ymGCcvH2zvIXKs5HCQii2b2Y76XXPr2MySZOJ6sXKROImlCjP2MCHvRfQ6B4qnLZXguWGGdI_DM9.png?raw=true)


## 3\. 적용된 핵심 보안 기술 (Key Security Features)

  * **Infrastructure as Code (IaC) 보안 강화:** Terraform으로 작성된 초기 인프라 코드의 보안 취약점(Security Group, IAM Role 부재 등)을 분석하고, '최소 권한 원칙'에 따라 개선했습니다.
  * **CI/CD 파이프라인 보안 (DevSecOps):** Jenkins, Docker, SonarQube, Trivy를 연동하여 코드 커밋부터 배포 전까지 모든 단계를 자동화하고 보안 검증을 내재화했습니다.
  * **정적 애플리케이션 보안 테스트 (SAST):** SonarQube를 이용해 소스 코드의 잠재적 취약점(Security Hotspots), 버그, 코드 스멜을 자동으로 탐지하도록 파이프라인을 구성했습니다.
  * **소프트웨어 구성 분석 (SCA):** Trivy를 이용해 컨테이너 이미지의 OS 패키지 및 라이브러리에 존재하는 CVE 취약점을 스캔하고, `HIGH` 또는 `CRITICAL` 등급의 취약점 발견 시 배포를 자동으로 차단하도록 구현했습니다.
  * **Immutable Infrastructure (불변 인프라):** Packer를 사용하여 Jenkins, Docker, Trivy 등 필요한 모든 소프트웨어가 사전 설치된 '골든 AMI'를 코드로 생성했습니다. 이를 통해 어떤 환경에서든 일관되고 검증된 서버를 빠르게 배포할 수 있는 기반을 마련했습니다.

## 4\. 보안 강화 'Before & After' 증명

이 프로젝트의 핵심은 실제 보안 취약점을 발견하고, 이를 개선한 전후 차이를 명확하게 증명하는 것입니다.

| 항목 | Before (취약한 초기 상태) | After (보안 강화) |
| :--- | :--- | :--- |
| **마스터 노드 보안 그룹** | SSH(22), K8s API(6443) 포트가 **`0.0.0.0/0`으로 전체 공개**되어 무차별 대입 공격에 매우 취약한 상태였습니다. | SSH와 K8s API 접근을 **특정 IP(`my_home_ip`)에서만 가능**하도록 제한하여 외부 공격 노출을 최소화했습니다. |
| **EC2 IAM 역할** | IAM 역할이 할당되지 않아, 서버가 어떤 권한을 가지는지 통제할 수 없었고 Access Key를 사용해야 하는 위험한 상태였습니다. | \*\*`k8s-node-role`\*\*이라는 최소한의 권한을 가진 역할을 명시적으로 부여하여, 서버의 신원과 권한을 명확히 통제했습니다. |
| **민감 정보 관리** | `app.py` 소스 코드 내에 **DB 비밀번호가 하드코딩**되어 있어, 코드 유출 시 심각한 보안 사고로 이어질 수 있었습니다. | **AWS Secrets Manager** 리소스를 생성하여 민감 정보를 안전하게 격리하고, IAM 역할을 통해 애플리케이션만 접근하도록 설계했습니다. |
| **CI/CD 파이프라인** | 보안 검증 단계가 없어, 개발자가 취약한 코드를 커밋하더라도 그대로 배포될 수 있는 위험한 상태였습니다. | SonarQube와 Trivy가 보안 검사를 수행하여, **취약점이 발견되면 자동으로 빌드를 실패시키고 배포를 차단**하는 안전장치를 마련했습니다. |

## 5\. 사용된 기술 스택 (Tech Stack)

  * **Cloud:** AWS (EC2, VPC, Subnet, IGW, NAT GW, S3, IAM, Secrets Manager)
  * **IaC:** Terraform, Packer
  * **CI/CD & Automation:** Jenkins, Docker, Git, GitHub
  * **Security Tools:** SonarQube (SAST), Trivy (SCA)
  * **OS & Scripting:** Amazon Linux 2, Shell Script

## 6\. 겪었던 문제 및 해결 과정 (Challenges & Lessons Learned)

> **이 부분이 기술 면접에서 당신을 빛나게 할 최고의 무기입니다.**

  * **Challenge 1: 젠킨스 파이프라인의 반복적인 Java 버전 충돌**

      * **문제:** `Jenkinsfile`에서 `tools` 블록, `withEnv` 등 여러 방법으로 JDK 17을 지정했음에도, SonarQube 스캐너 실행 시 계속해서 서버의 기본 Java 8 버전이 사용되어 `UnsupportedClassVersionError`가 발생했습니다.
      * **해결 과정:** `journalctl`을 통해 시스템 서비스 로그를 분석하여, 파이프라인 단계의 환경 변수 설정이 실제 실행 환경을 바꾸지 못함을 확인했습니다.
      * **최종 해결책:** 젠킨스 설정에 의존하는 대신, `packer-runner` 서버 자체의 기본 Java를 `alternatives` 명령어로 JDK 17로 직접 변경하여, 어떤 프로세스가 실행되든 원하는 Java 버전을 사용하도록 환경을 통제하여 문제를 해결했습니다.

  * **Challenge 2: Packer 빌드 시 반복된 네트워크 타임아웃**

      * **문제:** Packer가 임시 EC2 인스턴스를 생성하여 `yum update`를 실행할 때, 외부 리포지토리에 접속하지 못하고 계속해서 `Connection timeout` 오류가 발생했습니다.
      * **해결 과정:** 라우팅 테이블(IGW 연결), 네트워크 ACL(아웃바운드 규칙)을 순서대로 점검하며 문제가 없음을 확인했습니다. 최종적으로 Packer 설정 파일에 `associate_public_ip_address = true` 옵션을 추가하여, 임시 인스턴스에 공인 IP가 할당되지 않는 것이 근본 원인임을 파악하고 해결했습니다.
      * **배운 점:** 클라우드 네트워크 문제 해결 시, 라우팅, NACL, 보안 그룹뿐만 아니라, 리소스 자체의 네트워크 속성(공인 IP 할당 여부)까지 종합적으로 확인해야 함을 배웠습니다.
