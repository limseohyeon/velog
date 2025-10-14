<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/be53e5b2-b5d5-4278-b10f-77272f5a731a/image.png" />
<a href="https://youtu.be/JHuk4ouuvs4?si=3uuaE2qJClNq3rH6">10분 테코톡 - Spring Bean은 왜</a></p>
<h1 id="0-개요">0. 개요</h1>
<hr />
<p>이번 영상을 통해 왜 Spring에서 DI와 Singleton을 구현했는가?에 대해 알아볼 것이다.</p>
<h1 id="1-spring은-왜-di를-지원해주는가">1. Spring은 왜 DI를 지원해주는가?</h1>
<hr />
<p>다들 아는 것 처럼 DI의 대표적인 장점으로 유지보수성⬆️, 테스트성⬆️ 가 있다.</p>
<p> DI를 개발자가 직접 구현하게 된다면</p>
<p>의존관계 변경이 발생하면 비즈니스 로직 클래스, 테스트 코드, DI코드 모든 것의 변경이 발생하고 이를 계속 수정해줘야한다. 이러한 반복적인 작업을 Spring에서 대신해주는 것이다.</p>
<h1 id="2-spring은-왜-signton을-지원해주는가">2. Spring은 왜 Signton을 지원해주는가?</h1>
<hr />
<h2 id="21-싱글톤이-아니면-뭐가-문제일까">2.1 싱글톤이 아니면 뭐가 문제일까?</h2>
<p>Request 100개 발생에 따라 → Controller/Service/Repository 전부 100개씩 생성</p>
<p>⇒ 싱글톤을 유지함으로써 객체 생성과 메모리 비용을 감소시킬 수 있다.</p>
<h2 id="22-singleton을-직접-구현하면">2.2 Singleton을 직접 구현하면</h2>
<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/c0449606-84de-4c9f-bb17-ecd4df366d46/image.png" /></p>
<p>위 이미지는 가장 기본적인 싱글톤 패턴 코드로 이를 개발자가 직접 구현하면 아래와 같은 문제가 발생한다.</p>
<ul>
<li>private로 관리되기 때문에 다형성 적용 불가</li>
<li>메모리상에서 한 개의 인스턴스가 존재하기 때문에 테스트 순서에 따라 결과 달라짐</li>
<li>개발자가 매번 반복해서 작성해야함</li>
</ul>
<h2 id="23-spring의-singleton-구현방법">2.3 Spring의 Singleton 구현방법</h2>
<hr />
<p>그럼 스프링은 위와 같은 문제를 어떻게 해결했을까?</p>
<p>여기서 알아야 할 건 사실 싱글톤 패턴과 싱글톤 빈은 같지 않다.</p>
<ul>
<li>싱글톤 패턴 : one instance per application lifetime</li>
<li>싱글톤 빈 : one bean per bean id in a container</li>
</ul>
<p>이러한 차이가 존재하고 싱글톤 빈을 구현하고 있는 것이 SingletonBean Registry이다.</p>
<h2 id="24-singleton-bean-구현방법">2.4 Singleton Bean 구현방법</h2>
<hr />
<p>Spring가 Signleton Bean을 구현하는 과정은 아래와 같다.</p>
<ol>
<li><code>@SpringBootApplication</code> class 실행 → <code>@Component</code>가 컴포넌트 스캔 진행</li>
<li>스캔한 컴포넌트로 <strong>BeanDefinition 생성</strong>, 이때 빈 설계도(클래스 이름, 생성방식, 스코프 저장)를 이용</li>
<li>BeanDefinition을 <strong>BeanDefinitionRegistry</strong>에 저장 (<code>Map&lt;String, BeanDefinition&gt;</code>)</li>
<li>class와 BeanDefinition을 이용해 실제 객체 생성 <strong>SingletonBeanRegistry</strong>(<code>Map&lt;Stirng, Object&gt;</code>)에 저장한다.</li>
<li>빈이 필요할 때 SignletonBeanRegistry에서 확인한다.</li>
</ol>
<p><img alt="image.png" src="attachment:84f1341f-3f27-4c98-9169-49293f14b3ed:image.png" /></p>
<p>즉, 실제로 일반 객체를 생성해서 이를 싱글톤처럼 이용할 뿐 싱글톤 패턴을 이용한 것은 아니다.</p>