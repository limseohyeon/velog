<p>🔗<a href="https://youtu.be/At4Gyezw8WA?si=aDM02NUeAhnJ8wq6">[10분 테코톡 - Race Condtition 이해하기]</a></p>
<h1 id="1-race-condition이란">1. Race Condition이란?</h1>
<hr />
<p>공통 자원에 병행 접근할 때 실행 순서에 따라 결과가 달라지는 현상</p>
<h2 id="11-특징">1.1 특징</h2>
<ul>
<li><strong>비결정적 결과</strong> : 같은 코드를 실행해도 실행마다 결과가 달라짐</li>
<li><strong>공유 자원 동시 접근</strong> : 여러 스레드/프로세스가 동일한 변수를 읽고 쓰는 상황</li>
<li><strong>실행 순서 의존성</strong> : 작업 실행 순서에 따라 결과가 달라지는 의존성이 존재</li>
</ul>
<h2 id="12-원인">1.2 원인</h2>
<aside>

<p>컴퓨터의 동작 과정</p>
<ol>
<li>read</li>
<li>modify</li>
<li>write</aside>

</li>
</ol>
<p>컴퓨터는 세 순서로 움직이기 때문에 연산이 원자적으로 이루어지지 않는다.</p>
<p>위 과정을 한 번에 처리하는 것이 원자적(Atomic)연산의 핵심이다.</p>