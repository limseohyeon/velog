<!-- ENTRY_ID: https://velog.io/@limseohyeon/Annotation-10%EB%B6%84-%ED%85%8C%EC%BD%94%ED%86%A1 -->
<!-- SOURCE_TITLE: Annotation - 10분 테코톡 -->

<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/43de24b2-b000-4fdb-9230-0593c4cd97db/image.png" />
<a href="https://youtu.be/NdTgIXLm-Nk?si=LWM4ljec7yXPQp6v">10분 테코톡 - Annotation</a></p>
<h1 id="1-annotation">1. Annotation</h1>
<hr />
<h2 id="11-annotation-란">1.1 Annotation 란?</h2>
<p>Annotation란? 주석처럼 프로그래밍 언어에 영향을 미치지 않으며 다른 프로그램, 프로그래머에게 유익한 정보를 제공하는 메타데이터의 형태이다.</p>
<p>과거 .java와 .xml 별도로 구성 → 파일 커지고 복잡 &amp; 버전 불일치의 문제가 발생했다. 그 결과 .java 파일에서 이를 한꺼번에 관리하게 되면서 Annotation이 등장하게  되었다.</p>
<h2 id="12-annotation-역할">1.2 Annotation 역할</h2>
<ol>
<li><p><strong>컴파일러를 위한 정보 제공</strong></p>
<p> 그 예로, <code>@Override</code> 는 컴파일러에게 해당 메소드가 오버라이드 된 메소드임을 알린다.</p>
</li>
<li><p><strong>컴파일러나 빌드 도구가 코드, XML, 설정파일을 자동 생성하도록 정보 제공</strong></p>
<p> 그 예로, <code>@Getter</code>/<code>@Setter</code>/<code>@AllArgsConstruct</code> 와 같이 해당 메서드, 생성자를 생성하는 정보를 제공한다.</p>
</li>
<li><p><strong>프로그램이 실행 중(런타임)일 때 동작을 제어하도록 정보 제공</strong></p>
<p> 그 예로, <code>@Controller</code>/ <code>@RequestMappting</code>/ <code>@GetMapping</code> 가 그 역할을 한다.</p>
</li>
</ol>
<h2 id="13-annotation-장점">1.3 Annotation 장점</h2>
<ul>
<li>코드와 설정 파일을 한 곳에서 관리하며 설정 파일 <strong>의존성 감소</strong></li>
<li>보일러 플레이트 코드 제거로 <strong>가독성 향상</strong></li>
<li>커스텀 어노테이션 등을 활용해 유지보수, <strong>확장성 향상</strong></li>
</ul>
<h1 id="2-meta-annotation">2. Meta Annotation</h1>
<hr />
<p>Meta Annotation이란 어노테이션을 사용할 때 사용하는 어노테이션이다.</p>
<h2 id="21-meta-annotation-종류">2.1 Meta Annotation 종류</h2>
<table>
<thead>
<tr>
<th>Annotation</th>
<th>설명</th>
</tr>
</thead>
<tbody><tr>
<td><code>@Target</code></td>
<td>어노테이션을 어디서 사용할지 지정한다.</td>
</tr>
<tr>
<td><code>@Retention</code></td>
<td>어노테이션이 유지되는 범위를 지정한다.</td>
</tr>
<tr>
<td><code>@Inherited</code></td>
<td>어노테이션을 상속할 수 있도록 한다.</td>
</tr>
<tr>
<td><code>@Documented</code></td>
<td>어노테이션 정보를 Javadoc 문서에 포함시킨다.</td>
</tr>
<tr>
<td><code>@Repeatable</code></td>
<td>어노테이션을 반복해서 사용할 수 있게 한다.</td>
</tr>
</tbody></table>
<h3 id="211-target">2.1.1 @Target</h3>
<p>어노테이션을 어디에 사용할지 지정한다.</p>
<pre><code class="language-java">@Target(ElementType.ANNOTATION_TYPE)
public interface Target{...}</code></pre>
<p><strong>종류</strong></p>
<ul>
<li>ANNOTATION_TYPE</li>
<li>CONSTRUCTOR</li>
<li>FIELD</li>
<li>LOCAL_VARIABLE</li>
<li>METHOD</li>
<li>MODULE</li>
<li>PACKAGE</li>
<li>PARAMETER</li>
<li>RECORD_COMPONENT</li>
<li>TYPE</li>
<li>TYPE_PARAMETER</li>
<li>TYPE_USE</li>
</ul>
<h3 id="212-retention">2.1.2 @Retention</h3>
<p>어노테이션 유지범위를 지정한다.</p>
<pre><code class="language-java">@Retention(RetentionPolicy.SOURCE)
public interface Target{...}</code></pre>
<p><strong>종류</strong></p>
<ul>
<li>CLASS</li>
<li>SOURCE</li>
<li>RUNTIME</li>
</ul>
<h3 id="223-documented">2.2.3 @Documented</h3>
<p>어노테이션 정보를 javadoc 문서에 포함한다.</p>
<pre><code class="language-java">@Doucumented
public interface Target{...}</code></pre>
<h1 id="3-annotation-동작-원리">3. Annotation 동작 원리</h1>
<hr />
<p>Annotation은 두 가지 시점에 동작한다.</p>
<ul>
<li>컴파일 시점 : 컴파일러 내부 처리, Annotation Processor</li>
<li>런타임 시점 : Reflaction</li>
</ul>
<h2 id="31-컴파일-시점">3.1 컴파일 시점</h2>
<h3 id="311-annoation-processor">3.1.1 Annoation Processor</h3>
<p>javac(Java 컴파일러)가 컴파일 시점에 어노테이션을 분석하고 처리할 수 있도록 제공하는 기능이다.</p>
<h3 id="312-동작-과정">3.1.2 동작 과정</h3>
<p>@Getter을 예로 동작 과정을 살펴 보자. 아래는 Getter 어노테이션의 설정이다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/a1c49407-c3bb-458a-9f00-98dd516b2903/image.png" /></p>
<ul>
<li>FIELD, TYPE : 필드와 타입에 붙일 수 있음</li>
<li>SOURCE : 컴파일 시점까지 유지됨</li>
</ul>
<aside>

<p><strong>@Getter 어노테이션이 동작되는 과정</strong></p>
<ol>
<li>@Getter로 Lombock에게 정보 제공</li>
<li>javac(컴파일러) 컴파일 시작</li>
<li>Lombok Annotation Processor 로딩</li>
<li>Lombk이 Annotation 스캔 &amp; 분석</li>
<li>Lombok이 필요한 작업 수행 (코드 생성, 검증 등)</li>
<li>javac가 생성된 코드를 포함하여 최종 컴파일</aside>

</li>
</ol>
<h2 id="32-런타임-시점">3.2 런타임 시점</h2>
<h3 id="321-reflection">3.2.1 Reflection</h3>
<p>자바에서 클래스, 메서드, 필드 등의 정보를 실행 중에 동적으로 조회하거나 조작할 수 있는 기능</p>
<h3 id="322-동작-과정">3.2.2 동작 과정</h3>
<p>@RequestMapping(Spring MVC), @Entity(JPA) 을 예로 동작 과정을 살펴 보자. </p>
<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/1319e31e-8058-4406-a2c1-aa3c37a616aa/image.png" /></p>
<ul>
<li>TYPE, METHOD : 타입, 메서드에 사용가능</li>
<li>RUNTIME : 유지 시점 런타임</li>
</ul>
<aside>

<p><strong>@RequestMapping 어노테이션이 동작되는 과정</strong></p>
<ol>
<li>@RequestMapping로 Spring에게 정보 제공</li>
<li>JVM에 클래스 로딩(어플리케이션 실행)</li>
<li>Reflection으로 클래스/메서드 접근</li>
<li>Annotation 조회</li>
<li>Annotation 값 추출 (/admin)</li>
<li>조건 분기, 객체 생성 등 로직 수행 (뷰, URL과 메서드 매칭)</aside>

</li>
</ol>
<h1 id="4-custom-annotation">4. Custom Annotation</h1>
<hr />
<ol>
<li><strong>어노테이션 설정</strong></li>
</ol>
<pre><code class="language-java">@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface AnnotationExample {
    String Value() default &quot;기본 어노테이션&quot;;
}</code></pre>
<ul>
<li>어노테이션은 interface의 일종이다.</li>
<li>위 어노테이션은 default 값이 “기본 어노테이션”으로 별도의 Vaule가 설정되지 않으면 이 값이 반환된다.</li>
</ul>
<ol>
<li><strong>어노테이션 클래스에서 사용하기</strong></li>
</ol>
<pre><code class="language-java">public class Example{
    @AnnotationExample(&quot;성공 어노테이션&quot;)
    public vovid pass() {
    }

    @AnnotationExample(&quot;실패 어노테이션&quot;)
    public vovid fail() {
    }

    @AnnotationExample(&quot;성공 어노테이션&quot;)
    public vovid basic() {
    }

    public vovid notiong() {
    }
}</code></pre>
<ol>
<li><strong>결과 확인</strong></li>
</ol>
<ul>
<li>메서드에 Annotation가 붙어있으면 Annotation 값을 가져오기</li>
</ul>
<pre><code class="language-java">fail : 실패 어노테이션
pass : 성공 어노테이션
basic : 기본 어노테이션</code></pre>
<h1 id="5-마무리">5. 마무리</h1>
<hr />
<p>그간  어노테이션 정의만 알고 컴파일, 런타임 시점 등 그 동작 과정에 대해 잘 알지 못했다. 그래서 Lombok을 무지성으로 사용했고 이에 코드가 꼬인적이 꽤나 있었다.</p>
<p>지난 시간 그 많은 오류를 만났는데 제대로 알려하지 않고 돌아가기에 급급한 코드를 만들었구나… 하는 생각이 들었다.</p>
<p>…</p>
<p>그냥… 그런 생각이 들었다고…  </p>
<p>아무튼 새로운 지식을 알게 된 것과 더불어 개인적인 반성을 하게 됐다… 알아야 할 게 정말 산더미 같다. </p>
<p>나중에 Custom Annotaion을 만들어보고 싶다.</p>