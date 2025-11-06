<!-- ENTRY_ID: https://velog.io/@limseohyeon/Gradle-10%EB%B6%84-%ED%85%8C%EC%BD%94%ED%86%A1 -->
<!-- SOURCE_TITLE: Gradle - 10분 테코톡 -->

<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/de9001a3-5756-4b42-b1af-90e2c943e7e7/image.png" />
<a href="https://youtu.be/CEThRTpWErM?si=bsgaPIwM02Tc3hUR">10분 테코톡 - Gradle</a></p>
<h1 id="0-build-툴이-왜-필요할까">0. Build 툴이 왜 필요할까?</h1>
<hr />
<h2 id="01-build-란">0.1 Build 란?</h2>
<p><code>Source Code</code> [.java] → <code>Complile</code> [.class] → <code>Test</code> [.class] → <code>Deploy</code> [.jar, .war, .exe] 의 과정을 거친다.</p>
<p>위 과정을 수행하기 위해 개발자가 터미널에 명령어를 입력하는 과정을 자동화 해주는 역할을 한다.</p>
<h1 id="1-gradle">1. Gradle</h1>
<hr />
<h2 id="11-역할">1.1 역할</h2>
<p><strong>Build 성능 개선</strong></p>
<ul>
<li><strong>Incremental Build</strong> : 이전의 빌드 과정에서 변화가 없는 부분을 제외한 부분만 Build 한다.<ul>
<li>추가) Gradle은 변경된 Java 파일만 수정하고 Maven 은 바뀐 Java 파일이 포함되어 있는 모듈을 재컴파일하기 때문에 좀 더 섬세하게 성능 개선이 가능하다.</li>
</ul>
</li>
<li><strong>Build Cache</strong> : 이전에 빌드 과정에서 나온 결과물의 변경이 없다면 다음 빌드에서 재사용 한다.</li>
</ul>
<h1 id="2-dependency">2. Dependency</h1>
<hr />
<p>개발을 하면서 JWT나 Spring Framework처럼 외부 프로젝트를 사용하게 되는데 이를 외부 프로젝트에 ‘의존’한다고 한다.</p>
<h2 id="21-transitive-dependency">2.1 Transitive Dependency</h2>
<p>Transitive Dpendency란 내가 의존하고 있는 대상이 의존하는 대상으로 즉, 내가 간접적으로 의존하고 있는 경우를 의미한다.</p>
<p>예를 들어 Spring Framework 의존성을 추가하더라도 이만 추가되는 것이 아니라 그 외 참조되는 많은 의존성이 추가된다.</p>
<h2 id="22-dependencies-block">2.2 Dependencies Block</h2>
<p>buiuld.gradle 파일에서 사용할 의존성을 기입하는 공간이다.</p>
<pre><code class="language-jsx">dependencies {
    implemention 'org.springframework.boot:spring-boot-starter'
}</code></pre>
<p><strong>좀 더 자세히 살펴보자</strong></p>
<pre><code class="language-jsx">configuration '&lt;groupID&gt; : &lt;artifactId&gt; : &lt;version&gt;'
implemention 'org.springframework.boot:spring-boot-starter'</code></pre>
<ul>
<li>configuration : 사용할 의존성 범위 지정</li>
<li>groupID : 의존성 그룹 식별자</li>
<li>artifactId : 의존성 식별자</li>
<li>version : 의존성 버전</li>
</ul>
<h1 id="3-configuration">3. Configuration</h1>
<hr />
<p>위에 설명한 것 과 같이 Configuration은 의존성 범위를 지정하는 역할을 한다. </p>
<h2 id="31-configuration-종류">3.1 Configuration 종류</h2>
<p>Configurationd은 종류가 다양하다. 자세히 알아보자.</p>
<h3 id="311-comfileonly">3.1.1 ComfileOnly</h3>
<pre><code class="language-jsx">dependencies {
    complieOnly project(':complie-only');
}</code></pre>
<p>의존성의 범위를 컴파일 시점으로 구성한다.</p>
<h3 id="312-runtimeonly">3.1.2 runtimeOnly</h3>
<pre><code class="language-jsx">dependencies {
    runtimeOnly project(':runtime-only');
}</code></pre>
<p>의존성 범위를 런타임 시점으로 구성한다.</p>
<h3 id="313-implementation">3.1.3 Implementation</h3>
<pre><code class="language-jsx">dependencies {
    implementation project('implementation');
}</code></pre>
<p>컴파일과 런타임 모두로 구성한다.</p>
<h3 id="314-그외">3.1.4 그외</h3>
<ul>
<li><strong><code>testImplementation</code>, <code>testComplieOnly</code>, <code>testRuntimeOnly</code></strong> : 테스트 시점에 구성되는 것으로 Junit, Mockito와 같은 테스트 프레임워크이다.</li>
<li><strong><code>developmentOnly</code></strong> : 개발 환경에서만 필요한 라이브러리를 지정한다. 프로덕션 빌드에는 포함되지 않는다.</li>
<li><strong><code>annotationProcessor</code></strong> : 컴파일 시점에 애노테이션 프로세서를 사용하여 코드를 사용하거나 변환해야 할 때 사용한다.<ul>
<li>그 예로 Lombok가 있다. @Getter, @Setter와 같은 애노테이션을 통해 컴파일 시점에 코드를 자동으로 생성하기 때문에 annotationProcessor 설정을 통해 Lombok을 등록해야 한다.</li>
</ul>
</li>
</ul>
<h1 id="4-마무리">4. 마무리</h1>
<hr />
<p><strong><em>의존성 설정을 잘 구분하면 빌드 최적화, 의존성 충돌 방지, 최종 빌드 파일 크기 감소 등의 이점을 얻을 수 있다.</em></strong></p>
<p>그간 의존성 설정에 대해 깊이 생각해 본 적이 없는데 의존성 설정이 개발 비용 감소에 영향을 끼친다는 것을 처음 알았다. 이 기회에 기존 프로젝트 의존성 파일을 한 번 살펴봐야 할 것 같다.</p>
<p>또한, build 툴은 Gradle만 사용해 봤는데 다른 툴들과 어떻게 다른지 알아둘 필요가 있을 것 같다.</p>
<p>이는 다음 블로그 포스팅 주제로…🥲</p>
<h1 id="참고">참고</h1>
<hr />
<p><a href="https://lonelywolf.tistory.com/23">[Gradle] 의존성 설정 알아보기</a></p>