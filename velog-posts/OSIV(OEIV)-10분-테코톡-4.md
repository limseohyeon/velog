<!-- ENTRY_ID: https://velog.io/@limseohyeon/OSIVOEIV-10%EB%B6%84-%ED%85%8C%EC%BD%94%ED%86%A1 -->
<!-- SOURCE_TITLE: OSIV(OEIV) - 10분 테코톡 -->

<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/c8293d2e-f6c7-44db-ac81-2c564a844e64/image.png" /></p>
<p>🔗<a href="https://youtu.be/Q2n9I86mav4?si=VJliJX8PZ5Rq-nEn">10분 테코톡 - OSIV</a></p>
<blockquote>
<p><strong>문제</strong>
지연로딩된 객체의 속성을 Controller에서 접근할 수 있을까?</p>
</blockquote>
<h1 id="1-oeiv란">1. OEIV란?</h1>
<hr />
<p>JPA의 EntityManager을 요청 처리 전체 기간 동안 로컬 스레드에 바인딩 하는 것</p>
<ul>
<li>요청 처리 전체 기간 : 요청 ~ 응답까지 EntityManager가 활성화 되어있음</li>
<li>로컬 스레드에 바인딩 : 요청~ 응답까지 하나의 EnetityManager을 공유하며 사용할 것</li>
</ul>
<h2 id="11-oeiv설정-방법">1.1 OEIV설정 방법</h2>
<p>설정파일(.yml, .properties)에서 <code>open-in-view: true</code>를 통해 설정 가능 (default : true)</p>
<ul>
<li>true : 활성화</li>
<li>false : 비활성화</li>
</ul>
<h3 id="osiv와-oeiv">OSIV와 OEIV</h3>
<p>Hibernate에서는 Open Session In View, OSIV라 부르며,</p>
<p>JPA에서는 Open EntityManager In View OEIV라 부른다.</p>
<p>OSIV와 OEIV는 유사하지만 하이버네이트의 OSIV의 단점을 개선한 것이 OEIV라고 생각해도 된다.</p>
<h1 id="2-entitiymanager영속성-컨텍스트-생명-주기">2. EntitiyManager(영속성 컨텍스트) 생명 주기</h1>
<hr />
<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/953862ff-8463-4b0f-8feb-52e30db27ecc/image.png" /></p>
<h2 id="21-open-in-view-가-true인-경우">2.1 Open-In-View 가 true인 경우</h2>
<ul>
<li>EntityManager의 생성 : Interceptor #prehandle 단계에서 생성된다.</li>
<li>EntityManager의 종료 : View렌더링 이후 Interceptor #afterCompletion 단계에서 종료된다.</li>
</ul>
<p>EntityManager은 <code>Interceptor - Controller - View - Service</code> 단계에서만 활성화된다.</p>
<h2 id="22-open-in-view가-false인-경우">2.2 Open-In-View가 false인 경우</h2>
<ul>
<li>Interceptor 등록되지 않는다.</li>
</ul>
<p>EntityManager가 <code>Service</code> 안에서만 활성화된다. 즉, Transaction 범위에서만 활성화 된다.</p>
<p><strong>주의!</strong></p>
<p>이는 지연로딩 가능 여부 차이일 뿐 그외 생성/수정/삭제는 둘 다 Transaction에서만 가능하다.</p>
<h1 id="3-oeiv-장단점">3. OEIV 장/단점</h1>
<hr />
<h2 id="31-장점">3.1 장점</h2>
<ul>
<li>View 렌더링까지 지연로딩 지원한다.</li>
<li>개발 과정에서 지연로딩 위치 신경 쓰지 않아도 된다.</li>
</ul>
<h2 id="32-단점">3.2 단점</h2>
<p>Service에서 Interceptor ~ View 까지 지연로딩이 확장되며 DB커넥션 점유 시간이 증가한다.</p>
<p>(그에따라 Open-Session-View가 안티패턴이라는 의견도 존재하며, Spring 에서도 설정값이 true 되어 있는 경우 해당 사항에 대해 알려준다.)</p>
<h2 id="33-그래서-true-false">3.3 그래서 true? false?</h2>
<p>정답은 없다. 개발규모, 상황에 따라 적절하게 사용하자.</p>