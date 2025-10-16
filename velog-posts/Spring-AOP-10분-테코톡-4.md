<!-- ENTRY_ID: https://velog.io/@limseohyeon/Spring-AOP-10%EB%B6%84-%ED%85%8C%EC%BD%94%ED%86%A1 -->
<!-- SOURCE_TITLE: Spring AOP - 10분 테코톡 -->

<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/3654e6a9-1311-4756-bd46-3468b8ac85f0/image.png" />
🔗<a href="https://youtu.be/qdZvHRhfqhI?si=lHZCHZ10XhP0_nQf">10분 테코톡 - Spring AOP</a></p>
<p>이번 영상을 통해 두 가지 내용을 중심으로 AOP에 대해 알아볼 것이다.</p>
<ol>
<li>AOP가 왜 필요할까?</li>
<li>AOP를 어떻게 봐야 할까?</li>
</ol>
<h1 id="1-aop">1. AOP</h1>
<hr />
<h2 id="11-우리는-spring을-왜-쓰는가">1.1 우리는 Spring을 왜 쓰는가?</h2>
<p>Spring을 사용하면 Java Enterprise(=복잡한 요구사항) Application을 쉽게 만들 수 있다.</p>
<p>특히, Spring의 AOP는 크로스커팅 문제를 효과적으로 해결할 수 있다.</p>
<h2 id="12-크로스커팅횡단-관심사-문제">1.2 크로스커팅(횡단 관심사) 문제?</h2>
<hr />
<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/9df72cf6-41dc-4a78-a5f5-beed272c1ecc/image.png" /></p>
<p>크로스커팅(cross-cutting concern, 횡단 관심사)란 여러 계층과 서비스에 걸쳐서 반복적으로 동작하는 코드를 의미한다. 대표적인 예로 인증&amp;인가, 로깅, 트랜잭션 처리, 에러처리가 있다.</p>
<p>그렇다면, 이 문제를 객체지향적으로(인터페이스, 추상 클래스)로 해결할 수 없을까? </p>
<p>→ 각 서비스마다 동일한 횡단 관심사 코드를 일일이 구현하거나, 상속 구조를 강제로 도입해야한다. 코드 중복을 완전히 없애지 못하고, 서비스 로직과 섞여 관리가 어렵다. 즉, 객체지향 설계만으로는 횡단 관심사 문제를 깔끔하게 해결하기 어렵다.</p>
<p>이를 보완하기 위해 등장한 접근 방식이 AOP(Aspect Oriented Programming, 관점 지향 프로그래밍)이다.</p>
<h1 id="2-spring-aop">2. Spring AOP</h1>
<hr />
<h2 id="22-aop-핵심-개념">2.2 AOP 핵심 개념</h2>
<ul>
<li>Weaving</li>
<li><strong>Join Point : Advice가 적용될 위치</strong></li>
<li><strong>Advice : 실질적으로 어떤 일을 할 지에 대한 것</strong></li>
<li>Pointcut</li>
<li>Target Object</li>
<li><strong>Aspect : 관심사를 모듈화 한 것</strong></li>
<li>Proxy</li>
<li>Weaving</li>
</ul>
<p>이번엔 Join Point, Advice, Aspect 를 중심으로 AOP를 보도록 할 것이다.</p>
<pre><code class="language-java">import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.stereotype.Component;
import org.springframework.transaction.PlatformTransactionManager;
import org.springframework.transaction.TransactionStatus;
import org.springframework.transaction.support.DefaultTransactionDefinition;

@Aspect
@Component
public class TransactionAspect {

    private final PlatformTransactionManager transactionManager;

    public TransactionAspect(PlatformTransactionManager transactionManager) {
        this.transactionManager = transactionManager;
    }

    @Around(&quot;execution(* com.example.reservation.service..*(..))&quot;)
    public Object manageTransaction(ProceedingJoinPoint joinPoint) throws Throwable {
        TransactionStatus status = transactionManager.getTransaction(new DefaultTransactionDefinition());

        try {
            Object result = joinPoint.proceed();   // 핵심 로직 실행 (Join Point)
            transactionManager.commit(status);    // 성공 시 커밋
            return result;
        } catch (Throwable ex) {
            transactionManager.rollback(status);  // 실패 시 롤백
            throw ex;
        }
    }
}
</code></pre>
<h1 id="3-aop를-어떻게-바라봐야하는가">3. AOP를 어떻게 바라봐야하는가?</h1>
<hr />
<p>그렇다면 객체 지향 없이 모두 AOP로 구현하면 안 될까?</p>
<p>모든 기능을 AOP로 구현하게 된다면</p>
<ul>
<li>디버깅 힘듦</li>
<li>코드 흐름 추적 어려움 → 유지보수성 감소</li>
</ul>
<p><strong>OOP</strong></p>
<ul>
<li>해당 서비스 클래스만 봐도 로직 흐름을 이해할 수 있다.</li>
<li>구조적이고 직관적인 관리 가능</li>
</ul>
<p><strong>AOP</strong></p>
<ul>
<li>중복되는 횡단 관심사를 모듈화해 OOP를 보완한다.</li>
<li>본질적인 비즈니스 로직을 더 깔끔하게 유지할 수 있도록 돕는다.</li>
</ul>
<p><strong><em>정말 횡단 관심사 만 대체하는 것이 핵심으로 AOP는 OOP의 대체제가 아닌 보조 수단이다.</em></strong></p>