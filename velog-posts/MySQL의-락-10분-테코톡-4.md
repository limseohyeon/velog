<!-- ENTRY_ID: https://velog.io/@limseohyeon/10%EB%B6%84-%ED%85%8C%EC%BD%94%ED%86%A1-MySQL%EC%9D%98-%EB%9D%BD -->
<!-- SOURCE_TITLE: MySQL의 락 - 10분 테코톡 -->

<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/72d63037-c087-483f-a41e-2c5fd041f4c2/image.png" />
<a href="https://youtu.be/-VzgLlSXm4g?si=fTxgB3x33ZT_pUIb">10분 테코톡 - MySQL의 락</a></p>
<h1 id="1-락lock이란">1. 락(Lock)이란?</h1>
<p>여러 트랜잭션이 <strong>동시에 같은 데이터에 접근</strong>할 때 데이터 일관성과 무결성을 보장하기 위해 <strong>잠그는 것</strong>이다.</p>
<h2 id="11-mysql-락의-종류">1.1 MySQL 락의 종류</h2>
<ul>
<li>글로벌 락</li>
<li>백업 락</li>
<li>네임드 락</li>
<li>메타데이터 락</li>
<li>자동 증가 락</li>
<li><strong>테이블 락</strong></li>
<li><strong>레코드 락</strong></li>
<li><strong>갭 락</strong></li>
<li><strong>넥스트 키 락</strong></li>
</ul>
<p>…등 종류가 많지만 이번엔 테<strong>이블락, 레코드 락, 갭 락, 넥스트 키 락</strong> 이 네가지만 다뤄 보도록 한다.</p>
<h1 id="2-문제-상황">2. 문제 상황</h1>
<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/9b9f5e87-1492-4415-995a-9a8d64917ff3/image.png" /></p>
<p>동시성 문제가 발생하는 상황은 보통 다음과 같다.</p>
<ol>
<li>T1이 트랜잭션을 실행한다. balance = 30,000</li>
<li>T1의 트랜잭션 실행 도중 T2 또한 트랜잭션을 실행한다. balance = 30,000</li>
<li>T1의 트랜잭션이 종료된다. balance = 20,000</li>
<li>T2의 트랜잭션이 종료된다. balance = 25,000</li>
</ol>
<p>T2의 트랜잭션이 종료 되었을 때 balance 기댓값은 15,000지만 하나의 트랜잭션만 적용되는 문제가 발생한 것이다.</p>
<h1 id="3-해결-방법1-테이블-락">3. 해결 방법(1) 테이블 락</h1>
<hr />
<p>테이블 락은 테이블 단위로 락을 거는 것으로 아래와 같이 동작한다.</p>
<ol>
<li>T1 트랜잭션 실행 후 테이블 락 balance = 30,000</li>
<li>T1 트랜잭션이 종료 될 때 까지 T2 대기</li>
<li>T1 트랜잭션 종료 balance = 20,000</li>
<li>T2 트랜잭션 실행 balance =20,000</li>
<li>T2 트랜잭션 종료 balance = 15,000</li>
</ol>
<p>이렇게 테이블 락을 통해 동시성 문제 해결할 수 있다.</p>
<p>그러나 테이블락에도 문제가 있는데 어떤 문제가 더 발생할까?</p>
<h2 id="31-테이블-락의-문제점">3.1 테이블 락의 문제점</h2>
<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/d3c36e42-2b76-43a4-991e-84b990c5e4ee/image.png" /></p>
<p>테에블 락을 사용하는 경우 트랜잭션끼리 다른 레코드에 접근하는 경우 불필요한 락이 걸리기 때문에 성능 저하가 발생할 수 있다.</p>
<ol>
<li>T1은 id =1, T2 = id = 3 레코드에 접근</li>
<li>T1의 트랜잭션이 종료 될 때 까지 T2는 대기 발생</li>
</ol>
<h1 id="4-해결-방법2---레코드-락">4. 해결 방법(2) - 레코드 락</h1>
<hr />
<p>레코드락은 락을 테이블 단위가 아닌 레코드 단위로 거는 것이다.</p>
<p>즉, id = 1, id =3 레코드에 락을 걸어 각각 트랜잭션을 실행할 수 있도록 한다.</p>
<h2 id="41-레코드락-주의사항">4.1 레코드락 주의사항</h2>
<p>MySQL은 InnoDB를 사용하기 때문에 DML은 기본적으로 레코드락, DDL은 테이블 락으로 동작한다.</p>
<p>이때, 레코드락은 B-Tree구조이기 때문에 사실상 인덱스 락이다.</p>
<ol>
<li><strong>index가 아니고, Pk 값이 아닌 값으로 where 조건을 걸면 어떻게 될까?</strong></li>
</ol>
<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/e07aa9a4-45af-4b55-8101-925db87fc222/image.png" /></p>
<p>where 조건을 찾기 위해 Full scan이 발생한다.</p>
<p>이때, 도중 테이블 변경 발생으로 의도되지 않은 동작을 방지하기 위해 locking read를 한다. </p>
<p>즉, 읽은 레코드에 락을 걸어 어떤 레코드도 삽입, 삭제, 수정 불가능 하도록 한다.</p>
<ol>
<li><strong>동일한 조건에 index가 있다면 어떻게 될까?</strong></li>
</ol>
<p>Full scan이 발생하지 않고 필요한 데이터만 잠금 할 수 있다.</p>
<p>그러나 이러한 경우에도 다른 문제가 발생한다. </p>
<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/009b6529-5ed8-498c-97c3-42136dc1ad98/image.png" /></p>
<p>그림은 자료구조를 표로 나타내고 있지만 실제 인덱스는 트리구조이다.
그렇기에 트랜잭션 실행 도중 새로 삽입된 한스에 대해서 위와 같이 변경된다면 해당 값에 대해서는 update를 실행해 줄 수 없다. (읽을 수 가 없기 때문)</p>
<h1 id="5-next-key-lock-과-gap-lock"><strong>5. Next key lock 과 Gap lock</strong></h1>
<h2 id="51-gap-lock">5.1 Gap lock</h2>
<p>T1을 lock 하면 앞에도 lock 을 걸어 값이 들어오지 못하게 막는다. 이를 Gap lock라 한다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/f2ae66f0-dffb-4190-9f9a-ffa743ee0b61/image.png" /></p>
<h2 id="52-next-key-lock">5.2 Next key lock</h2>
<p>이후 이를 반복하며 다른 값에 대해서도 락을 거는데 이것을 Next key lock라한다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/1738bfe6-c838-46a2-9094-cdcb8557610e/image.png" /></p>
<h1 id="6-정리">6. 정리</h1>
<ul>
<li>스캔 했던 레코드는 잠근다</li>
<li>인덱스X 컬럼 조건 : 모든 레코드 스캔 → 모든 레코드 잠금</li>
<li>인덱스O 컬럼 조건 : 해당 레코드와 앞, 뒤를 잠금</li>
</ul>
<p>성능상의 이점을 얻으려면 불필요한 락을 발생시키지 않는 것이 중요하다. </p>
<p>PK는 인덱스 + 유니크이기 때문에 PK를 조건으로 걸면 하나의 레코드만 잠글 수 있다는 이점이 있다.</p>