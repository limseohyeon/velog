<p>🔗 <a href="https://youtu.be/L6teh1j0IRU?si=ISxidLCLR-Gnt1xU">10분 테코톡 Spring Boot Profile과 외부 설정</a></p>
<h1 id="0-서비스-개발과-환경">0. 서비스 개발과 환경</h1>
<p>서비스를 만들 때 개발자는 여러 환경에 놓이게 되고 각 환경은 다른 우선순위를 갖는다.</p>
<ul>
<li>Dev → 디버깅 등 개발 편의성이 우선</li>
<li>Stage → 안정성 확인을 위해 실제 환경과 유사해야 함</li>
<li>Prod → 실제 사용자가 접근하기 때문에 청책, 성능등 고려해야 함</li>
</ul>
<p>스프링에서는 이러한 환경을 분리하기 위해 두 가지  기능을 제공한다.</p>
<h1 id="1-externalized-configuration">1. Externalized Configuration</h1>
<hr />
<p>외부화된 속성을 주입할 수 있는 메커니즘</p>
<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/81877d3e-2d21-473f-8ac8-f5947a4a0e8d/image.png" /></p>
<hr />
<ul>
<li>추상화된 Environment : 외부 속성들 관리</li>
<li>PropertySource : 외부 속성 출처를 관리</li>
</ul>
<p>한 곳에서 각자 필요한 Bean을 스프링 컨테이너에서 가져와 사용한다.</p>
<h1 id="2-profile">2. Profile</h1>
<hr />
<p><code>@Profile</code>을 통해 조건별로 다른 설정과 Bean을 활성화 할 수 있다.</p>
<pre><code class="language-java">@Service
@Profile({&quot;dev&quot;, &quot;test&quot;})
public class BetaFeatureService {
    public String getFeature() {
        return &quot;Beta feature is enabled&quot;;
    }
}

@Service
@Profile(&quot;!prod&quot;) // Exclude production
public class ExperimentalFeatureService {
    public String getFeature() {
        return &quot;Experimental feature is enabled&quot;;
    }
}</code></pre>
<h2 id="21-동작-방식">2.1 동작 방식</h2>
<ol>
<li>SpringApplication.run() : 애플리케이션 실행</li>
<li>prepareEnvironment() : 기본 속성 설정 (CLI, 환경변수 등)</li>
<li>profile별 속성 설정</li>
<li>@Profile 조건에 맞는 빈 컨테이너에 등록(=active profile)</li>
</ol>
<h1 id="3-yml">3. yml</h1>
<hr />
<h2 id="31-yml파일-관리하기">3.1 yml파일 관리하기</h2>
<h3 id="방법-1--단일-파일로-관리하기">방법 (1) : 단일 파일로 관리하기</h3>
<ul>
<li>하나의 파일에서 모든 파일 관리 가능</li>
<li>규모 커지면 실수, 충돌 발생 가능성 올라감</li>
</ul>
<h3 id="방법-2--복수-파일-관리">방법 (2) : 복수 파일 관리</h3>
<ul>
<li>application-name.yml 형식으로 관리</li>
<li>충돌 발생 가능성 감소, 협업 효율 상승</li>
<li>관리해야 할 파일 개수 늘어남</li>
</ul>
<h2 id="32-사용시-주의사항">3.2 사용시 주의사항</h2>
<h3 id="1-active-profile은-applicationyml을-이용하지-말-것"><strong>1. active profile은 application.yml을 이용하지 말 것.</strong></h3>
<pre><code class="language-java">ymldp spring.profiles.active=prod</code></pre>
<p>처럼 하드코딩하면 환경 바꿀 때 파일 수정이 발생하기 때문에 재빌드가 발생한다.</p>
<pre><code class="language-java">java -jar app.jar --spring.profiles.active=dev</code></pre>
<p>위와 같이 실행시 CLI/환경변수에서 지정해야한다.</p>
<p><strong>이 경우 우선순위가 존재하기 때문에 고려해 설정해야한다.</strong></p>
<aside>

<p><strong>우선순위</strong></p>
<p>(높음) CLI 인자 - JVM 시스템 속성 - 환경 변수 - <a href="http://application.properties">application.properties</a> - application.yml (낮음)</p>
<pre><code class="language-java">java -jar app.jar --spring.profiles.active=dev1, dev2</code></pre>
<p>뒤에 있을 수록 우선 순위가 높다. dev2 &gt; dev1 &gt; default</p>
</aside>

<h3 id="2-민감한-정보는-외부에-노출하지-않도록-조심하자"><strong>2. 민감한 정보는 외부에 노출하지 않도록 조심하자</strong></h3>
<p><strong>관리 방법 (1) 환경 변수로 관리하기</strong></p>
<ul>
<li>장점<ul>
<li>코드와 분리되어 있음</li>
<li>클라우드/컨테이너 친화적</li>
<li>구조를 공유해 엽업에 도움</li>
</ul>
</li>
<li>단점<ul>
<li>관리/설정 부담</li>
<li>디버깅 어려움</li>
</ul>
</li>
</ul>
<p><strong>관리 방법(2) gitignore로 무시하기</strong></p>
<pre><code class="language-java">spring:
        config:
                import: secret.yml (.gitignore)</code></pre>
<ul>
<li>장점<ul>
<li>보안성 높음</li>
<li>설정이 단순</li>
<li>디버깅 용이</li>
</ul>
</li>
<li>단점<ul>
<li>협업 복잡</li>
<li>파일 전달 부담</li>
<li>코드 변경과 동기화 안됨</li>
</ul>
</li>
</ul>
<p><strong>관리 방법(3) 암호화 하기</strong></p>
<ul>
<li>장점<ul>
<li>유출 시 보호</li>
<li>구조 완정 공유</li>
</ul>
</li>
<li>단점<ul>
<li>키 관리 필요성</li>
<li>운영 복잡도 상성</li>
<li>라이브러리 의존성</li>
</ul>
</li>
</ul>