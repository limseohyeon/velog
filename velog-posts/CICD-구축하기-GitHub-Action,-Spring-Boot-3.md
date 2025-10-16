<h1 id="0-개요">0. 개요</h1>
<hr />
<p>이전에는 프로젝트를 빌드하고 배포할 때마다 터미널에서 직접 명령어를 입력해 수동으로 진행했다. 빌드 시간이 오래 걸릴 뿐만 아니라, 브랜치 충돌이나 예상치 못한 에러가 발생하면 같은 과정을 여러 번 반복해야 했다. 이러한 비효율을 줄이기 위해 CI/CD 환경을 구축하기로 했다.</p>
<h1 id="1-cicd-란">1. CI/CD 란?</h1>
<hr />
<p>CI/CD란 지속적 통합 (Continuous Integration) 과 지속적 배포 (Continuout Deploymemt) 의 줄임말이다.</p>
<h2 id="11-지속적-통합-ci">1.1 지속적 통합 CI</h2>
<p>지속적 통합은 개발 팀이 코드를 지속적으로 통합하고, 이를 자동으로 테스트해 통합 버그를 최소화하는 프로세스다.</p>
<ul>
<li>코드 변경 사항이 발생할 때마다 자동으로 빌드 및 테스트를 진행한다.</li>
<li>코드 충돌을 미리 발견할 수 있으며 품질 관리 및 버그 발견이 빨라진다.</li>
</ul>
<h2 id="12-지속적-배포-cd">1.2 지속적 배포 CD</h2>
<p>지속적 배포는 통합된 코드를 자동으로 프로덕션 환경에 배포하는 프로세스다.</p>
<ul>
<li>코드 변경 사항이 테스트 및 승인을 거쳐 자동으로 프로덕션 환경에 배포된다.</li>
<li>새로운 기능과 수정 사항이 사용자에게 빠르게 제공된다.</li>
</ul>
<h1 id="2-cicd-종류">2. CI/CD 종류</h1>
<hr />
<p>CI/CD를 위한 도구는 여러가지가 존재한다. 대표적인 몇 개를 알아보고 오늘은 그 특장점만 간단히 비교할 것이다.</p>
<h3 id="bamboo">Bamboo</h3>
<ul>
<li>Atlassian에서 개발한 상용 도구로 Jira, Bitbucket과 같은 Atlassian 도구와 호환성이 좋다.</li>
<li>유료 도구로 개인 프로젝트보다 기업 환경에 적합하다.</li>
</ul>
<h3 id="jenkins">Jenkins</h3>
<ul>
<li>오픈소스 기반 대표 CI/CD 도구로 자료가 많고 플러그인 생태계가 풍부해 유연한 커스터마이징이 가능하다.</li>
<li>그만큼 초기 설정과 관리가 복잡하고(별도의 서버, 설시 필요) 유지보수 부담이 발생한다.</li>
</ul>
<h3 id="github-action">GitHub Action</h3>
<ul>
<li>GitHub 저장소에 통합되어 있는 CI/CD 서비스로 워크플로우를 YAML로 정의해 사용 가능하다.</li>
<li>클라우드 기반으로 별도 서버가 필요 없고 단순하지만 자료가 적다.</li>
</ul>
<h2 id="21-어떤-것을-선택할까">2.1 어떤 것을 선택할까?</h2>
<p>OCI 무료 티어 환경에서는 Jenkins를 설치해 자체 서버에서 CI/CD를 운영하기엔 리소스 제약이 있었다. (이런저런 이유로 GCP를 이용하게 되어 이는 상관 없어졌다…)</p>
<p>GitHub Actions은 클라우드 기반 CI/CD 서비스로, 별도의 서버 자원을 사용하지 않고도 빌드와 테스트를 수행할 수 있다.</p>
<p>또한 애플리케이션 규모가 단순해 Jenkins처럼 복잡한 파이프라인 구성이 필요하지 않았다. 이러한 이유로, 자동화 효율성과 배포 속도를 높이기 위해 GitHub Actions를 선택했다.</p>
<h1 id="3-github-action-더-알아보기">3. GitHub Action 더 알아보기</h1>
<hr />
<p>GitHub Action이란 GitHub 저장소를 기반으로 Workflow를 자동화 할 수 있는 도구이다.</p>
<h2 id="31-github-aciton특징">3.1 Github Aciton특징</h2>
<ul>
<li>컨테이너(도커) 기반으로 동작한다.</li>
<li>YMAL 파일 기반 Workflow를 작성해 다양한 이벤트를 실행시킬 수 있다.</li>
<li>Workflow는 Runners라 불리는 인스턴스에서 Linux, macOS, Windows 환경에서 실행된다.
원하는 OS를 지정할 수 있고, 여러 OS에서 테스트도 가능하다.</li>
<li>GitHub 마켓 플레이스엥서 다른 사용자가 공유한 Workflow를 가져다 쓰거나 공유할 수 있다.</li>
</ul>
<h2 id="32-장점단점">3.2 장점/단점</h2>
<h3 id="장점">장점</h3>
<ul>
<li>별도의 서버 설치가 필요 없다.</li>
<li>비동기적 병렬 실행이 가능하다.</li>
<li>설정이 매우 쉽다.</li>
</ul>
<h3 id="단점">단점</h3>
<ul>
<li>캐싱이 필요한 경우에는 자체 캐싱 로직을 작성해야 한다.</li>
<li>서버에 장애가 일어나거나 리소스를 초과할 경우 개발자가 직접 해결해야 한다.</li>
</ul>
<h2 id="33-구성요소">3.3 구성요소</h2>
<p>GitHub Action의 구성 요소는 Workflow, Event, Job, Step, Action, Runner가 있다.</p>
<h3 id="workflow">workflow</h3>
<p>최상위 개념으로 자동화된 프로세스가 정의되어 있는 하나의 파일이다.</p>
<ul>
<li>하나 이상의 job으로 구성</li>
<li>Push나 PR과 같은 이벤트나 특정 시간대에 실행될 수 있음</li>
<li>빌드, 테스트, 배포 등 각각 역할에 맞는 workflow 추가 가능</li>
<li>.github/workflows 디렉토리에 yaml 형태로 저장</li>
</ul>
<h3 id="runner">Runner</h3>
<p>Workflow가 실행될 인스턴스로 클라우드에서 동작한다.</p>
<ul>
<li>Github에서 호스팅하는 가상 환경 또는 직접 호스팅하는 가상 환경에서 실행 가능</li>
<li>메모리 및 용량 제한이 존재한다.</li>
</ul>
<h3 id="event">Event</h3>
<p>Workflow를 실행할 특정 활동(push, commit 등)이나 규칙이다.</p>
<h3 id="job">Job</h3>
<p>Workflow내에서 실행될 명령이다. Event로 workflow가 실행되면 Job에 작성된 명령들이 실행된다.</p>
<ul>
<li>하나의 Workflow 내에서 독립적으로 실행되며 순서 지정도 가능</li>
<li>Job은 자신의 환경설정과 Step을 가짐</li>
</ul>
<h3 id="step">Step</h3>
<p>Job내에 있는 실행할 수 있는 각각의 Task이다.</p>
<ul>
<li>각 step들은 script, 명령어 또는 action을 실행할 수 있다.</li>
<li>각 step들은 데이터를 공유할 수 있다</li>
</ul>
<h3 id="action">Action</h3>
<p>재사용되는 명령어들의 집합으로 이루어진 작업니다.</p>
<ul>
<li>직접 작성해도 되고 마켓에 등록된 Action을 가져와 사용할 수 있음</li>
</ul>
<h2 id="34-명령어-사용-예시">3.4 명령어 사용 예시</h2>
<p>workflow는 <code>.github/workflows</code> 내부에 <code>이름.yml</code> 형식으로 작성한다.</p>
<ol>
<li><strong>최상단에 name 작성</strong></li>
</ol>
<pre><code class="language-yaml">name: example workflow</code></pre>
<ul>
<li>workflow 이름 지정, 여기서는 example worklow라는 이름을 갖는다.</li>
</ul>
<ol>
<li><strong>Event 정의</strong></li>
</ol>
<pre><code class="language-yaml">on:
  push:
    branches: [ &quot;main&quot; ]</code></pre>
<ul>
<li>main branch에 push 이멘트가 발생할 때 Job 실행 Event</li>
</ul>
<ol>
<li><strong>Job 정의</strong></li>
</ol>
<pre><code class="language-yaml">jobs: 
    example-workflow-job: 
        runs-on: ubuntu-latest</code></pre>
<ul>
<li><code>example-workflow-job</code> 이라는 이름의 job</li>
<li><code>runs-on: ubuntu-latest</code> : 작업을 ubuntu 최신 기반 Runner에서 수행</li>
</ul>
<ol>
<li>Step 정의</li>
</ol>
<pre><code class="language-yaml">jobs:
    workflow-test-job:
        runs-on: ubuntu-latest
            steps:
            - name: Set up JDK 11
              uses: actions/setup-java@v4
              with:
                java-version: '11'
                distribution: 'temurin'</code></pre>
<ul>
<li>name : step 이름 지정</li>
<li>uses : 다른 사람이 만들어둔 액션을 가져옴</li>
<li>with : step을 위한 설정</li>
</ul>
<h1 id="4-구현하기">4. 구현하기</h1>
<hr />
<h2 id="41-요구사항">4.1 요구사항</h2>
<ul>
<li><strong>PR 생성 시</strong> 자동으로 <strong>빌드 및 테스트 수행 (CI)</strong></li>
<li><strong>main 브랜치에 푸시 발생 시</strong> 자동으로 <strong>배포 진행 (CD)</strong></li>
</ul>
<blockquote>
<p>대상 프로젝트: Spring Boot + Java, 배포 환경: GCP</p>
</blockquote>
<h2 id="41-키-발급하기">4.1 키 발급하기</h2>
<p>키 발급 - GCP 설정은 아래 링크를 참고했다.</p>
<p><a href="https://unfinishedgod.netlify.app/2023/06/11/gcp-compute-engine-mobaxterm/">[GCP] Compute Engine 방화벽 및 MobaXterm 연결 - 미완성의신</a></p>
<h2 id="42-환경-변수-설정-github-secrets">4.2 환경 변수 설정 (GitHub Secrets)</h2>
<p>GCP 인스턴스와 연결하기 위해 해당 정보가 필요한데 이를 파일에 직접 올리는건 보안상 문제가 있다. 이를 막기위한 방법으로 GitHub에 환경 변수 값을 설정할 수 있다.</p>
<ol>
<li><strong>프로젝트 레포지토리에서 Settings → Security → Serets and Variables → Action 로 이동한다.</strong></li>
</ol>
<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/1a48c8e7-5920-4a15-89df-c7a2b8161ceb/image.png" /></p>
<ol>
<li><strong>New repository secret를 눌러 설정할 환경변수 값을 입력한다.</strong></li>
</ol>
<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/2d9873ea-9167-4130-8cdb-b42bf585dd50/image.png" /></p>
<h2 id="42-ci">4.2 CI</h2>
<pre><code class="language-yaml">name: CI

on:
  pull_request:
    branches: [ &quot;main&quot; ]

jobs:
  ci:
    runs-on: ubuntu-latest
    permissions:
      contents: read

    steps:

      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up JDK 11
        uses: actions/setup-java@v4
        with:
          java-version: '11'
          distribution: 'temurin'

      - name: Grant execute permission for Gradle wrapper
        working-directory: backend
        run: chmod +x ./gradlew

      - name: Build project with Gradle Wrapper
        working-directory: backend
        run: ./gradlew clean build -x test</code></pre>
<h2 id="43-cd">4.3 CD</h2>
<pre><code class="language-yaml">name: CD

on:
  push:
    branches: [ main ]

jobs:
  cicd:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    env:
      JAR_NAME: petmliy.jar 

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up JDK 11
        uses: actions/setup-java@v4
        with:
          java-version: '11'
          distribution: 'temurin'

      - name: Grant execute permission for Gradle wrapper
        working-directory: backend
        run: chmod +x ./gradlew

      - name: Build project with Gradle Wrapper
        working-directory: backend
        run: ./gradlew clean build -x test

      - name: Upload build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: backend-build
          path: backend/build/libs/${{ env.JAR_NAME }}

      - name: Download build artifact
        uses: actions/download-artifact@v4
        with:
          name: backend-build
          path: ./backend

      - name: Copy artifact to GCP server
        uses: appleboy/scp-action@v0.1.5
        with:
          host: ${{ secrets.GCP_HOST }}
          username: ${{ secrets.GCP_USERNAME }}
          key: ${{ secrets.GCP_PRIVATEKEY }}
          port: 22
          source: &quot;./backend/${{ env.JAR_NAME }}&quot;
          target: &quot;/home/action/app/&quot;

      - name: Restart app on GCP
        uses: appleboy/ssh-action@v0.1.10
        with:
          host: ${{ secrets.GCP_HOST }}
          username: ${{ secrets.GCP_USERNAME }}
          key: ${{ secrets.GCP_PRIVATEKEY }}
          port: 22
          script: |
            # 기존 프로세스 종료
            pkill -f $JAR_NAME || true
            # 새 jar 실행
            nohup java -jar /home/action/app/$JAR_NAME &gt; /dev/null 2&gt;&amp;1 &amp;</code></pre>
<h1 id="5-트러블슈팅">5. 트러블슈팅</h1>
<hr />
<h2 id="51-키-인증-실패">5.1 키 인증 실패</h2>
<p><strong>문제</strong></p>
<p>기존 mobaXterm SSH 세션 연결을 위해 사용했던 키를 그대로 사용했더니 아래와 같은 에러 메시지가 떴다.</p>
<ul>
<li><code>ssh: this private key is passphrase protected</code>, <code>no supported methods remain</code></li>
<li><code>ssh: this private key is passphrase protected</code></li>
</ul>
<p><strong>원인</strong></p>
<ul>
<li>로컬(MobaXterm)에서는 PuTTY 기반 <code>.ppk</code> 키를 사용 중이었으나, GitHub Actions는 <code>OpenSSH</code> 형식의 private key만 인식</li>
<li>passphrase가 포함된 키를 사용해 CI 환경에서 인증이 거부됨.</li>
</ul>
<p><strong>해결</strong></p>
<ul>
<li><strong>새로운 passphrase 없는 OpenSSH 형식의 키 쌍을 생성.</strong>
아래 해당 부분을 입력하지 않고 키를 발급한다.</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/a462ffdd-9cc0-4cfb-bd7a-e7137af8498e/image.png" /></p>
<ul>
<li><strong>발급받은 private key를 SSH 형식으로 변환</strong>
mobaXterm - Tool - Generator - Conversions - Export OpenSSH key</li>
</ul>
<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/ea63aed0-7681-4284-b2d3-88d6b0e611ec/image.png" /></p>
<ul>
<li><strong>변환한 키를 GCP 인스턴스의 SSH Keys에 등록</strong></li>
</ul>
<h2 id="52-jar-파일명-불일치">5.2 Jar 파일명 불일치</h2>
<p><strong>오류 내용</strong></p>
<ul>
<li><code>.yml</code> 파일 내에서 JAR 파일명을 변수로 관리하려 했으나, 변수 처리 과정에서 파일명이 일치하지 않아 SCP 전송 시 <code>&quot;파일을 찾을 수 없음&quot;</code> 오류가 반복 발생했다.</li>
</ul>
<p><strong>원인</strong></p>
<ul>
<li>GitHub Actions 워크플로우에서 정의한 환경변수가 실제 빌드 결과물(<code>.jar</code> 파일명)과 동기화되지 않음</li>
<li>빌드 시점마다 버전이나 타임스탬프가 붙는 구조라 동적 파일명을 제대로 참조하지 못한 것</li>
</ul>
<p><strong>해결</strong></p>
<ul>
<li>일단 환경변수 의존을 제거하고, <strong>JAR 파일명을 하드코딩</strong>하는 방식으로 빌드·배포를 마무리했다.</li>
</ul>
<p><strong>추후 개선 방향</strong></p>
<p>실제 서비스 환경에서는 빌드 결과가 매번 달라지기 때문에 하드코딩 방식은 유지보수에 불편함이 크다. 이를 관리할 방법에 대해 알아보고 나중에 변경하면 좋을 것 같다.</p>
<hr />
<h1 id="참고">참고</h1>
<hr />
<p><a href="https://velog.io/@rokwon_k/Github-Action%EA%B3%BC-%ED%95%84%EC%9A%94%ED%95%9C-%EA%B0%9C%EB%85%90%EC%A0%95%EB%A6%AC">Github Action과 필요한 개념정리</a></p>
<p><a href="https://velog.io/@sangwoong/CICD-GitHub-Action%EC%9C%BC%EB%A1%9C-CICD-%EA%B5%AC%EC%B6%95%ED%95%98%EA%B8%B0">[CICD] GitHub Action으로 CI/CD 구축하기</a></p>