<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/53b7aa21-ec49-42b7-b61b-d2049ec6a3ff/image.png" />
<a href="https://youtu.be/MuZ-Mx0N-dA?si=kpaWOcL6JcWLHeTd">🔗10분 테코톡 - B-Tree 인덱스와 클러스터링 인덱스</a></p>
<h1 id="0-인덱스란">0. 인덱스란?</h1>
<hr />
<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/1f5c7458-d84b-459c-8c84-8c76172e721e/image.png" /></p>
<p>인덱스는 특정 열 값의 행을 빠르게 찾을 수 있게 돕는 데이터 객체이다.</p>
<p>인덱스의 경수 순차 탐색을 통해 조회를 하는 경우 최악의 경우 O(N) 복잡도가 발생할 수 있다.</p>
<p>이러면 인덱스를 사용하는 것에 대한 큰 이점이 생기지 않는다.</p>
<h1 id="1-이진트리">1. 이진트리</h1>
<hr />
<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/7631260d-d118-4834-84c3-16c388a20260/image.png" /></p>
<p>B-Tree는 이진트리의 확장 버전이기 때문에 이진트리부터 알아보도록 하자</p>
<p>5를 찾는 경우 순차 탐색과 이진 탐색은 아래와 같은 차이를 보인다.</p>
<ul>
<li>순차 탐색 : 1- 2- 3- 4- 5 <strong>총 5회</strong></li>
<li>이진 탐색 : 4 - 6 - 5 <strong>총 3회</strong></li>
</ul>
<h2 id="11-이진트리-단점">1.1 이진트리 단점</h2>
<ul>
<li>트리가 한 쪽으로 경사질 수 있다</li>
<li>저장하려는 키가 많아지면 트리 깊이가 깊어지고, 탐색 수 많아진다.</li>
</ul>
<p><strong><em>⇒ 마찬가지로 최악의 경우 O(N) 복잡도 발생한다.</em></strong></p>
<h1 id="2-b-tree-인덱스">2. B-Tree 인덱스</h1>
<hr />
<p>이러한 이진트리의 단점을 개선하기 위해 사용하는 것이 B-Tree다.</p>
<h2 id="21-b-tree-특징">2.1 B-Tree 특징</h2>
<ul>
<li>항상 Balance 유지 → 경사X</li>
<li>한 노드에 여러개의 키 저장 가능 (k개)</li>
<li>2개 이상의 자식을 가질 수 있음(k+1 개)</li>
<li>키가 항상 정렬되어 저장됨</li>
</ul>
<h2 id="22-b-tree-구성">2.2 B-Tree 구성</h2>
<ul>
<li><strong>루트 노드</strong> : 제일 상위에 있는 노드</li>
<li><strong>리프 노드</strong> : 제밀 끝단에 있는 노드’</li>
<li><strong>브랜치 노드</strong> : 중간에 있는 노드</li>
</ul>
<h2 id="23-b-tree-구조">2.3 B-Tree 구조</h2>
<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/b0f46ed4-3d8f-462a-809e-3d2b8153de9a/image.png" /></p>
<p>9을 찾는 경우 아래와 같이 탐색이 진행된다.</p>
<ul>
<li>9 -3/6 - 7/8 <strong>총 3회</strong></li>
</ul>
<p>⇒ 경사가 발생X, 최악의 경우에도 N 조회X 이진트리에 비해 비교적 빠른 조회 속도</p>
<h2 id="24-b-tree의-범위-탐색">2.4 B-Tree의 범위 탐색</h2>
<p>B-Tree에도 단점이 존재하는데 바로 범위 탐색을 진행하는 경우다.</p>
<p>만일 10, 11, 12, 13을 탐색한다고 가정해보자</p>
<ul>
<li>10, 11, 12 같은 경로에 존재 → 한 번에 탐색이 가능</li>
<li>13 다른 경로에 존재 → 다시 루트 노트부터 탐색을 실행</li>
</ul>
<p><strong><em>⇒ 이러한 특징으로 B-Tree는 범위 검색에 큰 장점을 보이지 않는다.</em></strong></p>
<h1 id="3-btree-인덱스">3. B+Tree 인덱스</h1>
<hr />
<p>일반적인 B-Tree의 단점을 보완한게 B+Tree이다.</p>
<h2 id="31-btree-특징">3.1 B+Tree 특징</h2>
<ul>
<li>리프 노드에 모든 키가 존재</li>
<li>키와 연결된 레코드에 대한 주소를 리프 노트에서만 가짐</li>
<li>같은 높이의 노드들은 서로 연결되어 있음</li>
</ul>
<h2 id="32-btree-구조">3.2 B+Tree 구조</h2>
<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/171910ff-7498-446c-a8e9-c1fddee57764/image.png" /></p>
<p>7 - 8 - 9 범위 검색을 진행해보도록 하자.</p>
<ul>
<li>7 -8 : 같은 경로에 존재 한 번에 탐색 가능</li>
<li>9 : 같은 높이 → 연결되어 있기 때문에 마찬가지로 한 번에 탐색 가능</li>
</ul>
<p>이러한 장점으로 현재 많은 DBMS 의 인덱스에 B+Tree를 이용하고 있다.</p>
<h2 id="33-btree의-삽입연산k3">3.3 B+Tree의 삽입연산(k=3)</h2>
<p>삽입 과정을 보며 어떻게 기울기를 유지하는지 보도록하자.</p>
<aside>

<p><strong>단계 1</strong> : <code>7</code> 삽입하기</p>
<ul>
<li>삽입 전 : <code>5</code></li>
<li>삽입 후 : <code>5</code> -<code>7</code></aside>

</li>
</ul>
<aside>

<p><strong>단계 2</strong> <code>6</code> 삽입하기</p>
<ul>
<li>삽입 전 : <code>5</code> - <code>7</code></li>
<li>삽입 후 : <code>5</code> -<code>6</code> -<code>7</code></aside>

</li>
</ul>
<aside>

<p><strong>단계 3-1</strong> <code>4</code> 삽입하기</p>
<ul>
<li>삽입 전 :<code>5</code> -<code>6</code> -<code>7</code></li>
<li>삽입 후 : <code>4</code>-<code>5</code> -<code>6</code> -<code>7</code></li>
</ul>
<p>이때, 최대 노드 개수(k) 초과로 Split(분할) 과정을 거친다.</p>
<p><strong>단계 3-2</strong> Split</p>
<ul>
<li><p>가운데 값 하나를 상위 노드로 보내고 연결</p>
</li>
<li><p>Split 후</p>
<pre><code>              `6`

 `4` - `5`     `6`- `7`</code></pre></li>
</ul>
<p>위와 같은 과정의 반복한다.</p>
</aside>

<h2 id="34-btree의-삭제">3.4 B+Tree의 삭제</h2>
<p>DBMS에서 soft삭제와 같이 마킹만 진행되고 , 실제로 삭제가 발생하지 않는다고 한다.</p>
<h1 id="4-클러스터링-인덱스">4. 클러스터링 인덱스</h1>
<hr />
<h2 id="41-클러스터링-인덱스-사용-전">4.1 클러스터링 인덱스 사용 전</h2>
<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/1d90fea3-c469-4114-a593-492d457e8644/image.png" /></p>
<ul>
<li>B-Tree의 리프 노드 = 데이터 주소(Row ID)</li>
<li>데이터는 삽입 순서대로 저장</li>
<li>like 책 목차에 페이지 번호만 적혀 있음 → 번호 보고 본문 찾아가야 함</li>
</ul>
<h2 id="42-클러스터링-인덱스-사용-후">4.2 클러스터링 인덱스 사용 후</h2>
<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/377d19bf-e4c9-4061-8495-4ed99565c113/image.png" /></p>
<ul>
<li>B-Tree 리프 노드 = 실제 데이터</li>
<li>테이블 전체가 PK 기준으로 정렬됨</li>
<li>like 책 목차에 본문 내용까지 같이 들어 있음 → 바로 읽기 가능</li>
</ul>
<h2 id="43-차이점">4.3 차이점</h2>
<table>
<thead>
<tr>
<th>구분</th>
<th>클러스터링 인덱스 O</th>
<th>클러스터링 인덱스 X</th>
</tr>
</thead>
<tbody><tr>
<td>리프 노드</td>
<td><strong>데이터 자체</strong></td>
<td><strong>Row ID(주소)</strong></td>
</tr>
<tr>
<td>정렬</td>
<td>PK 기준 정렬</td>
<td>없음</td>
</tr>
<tr>
<td>PK 조회</td>
<td>빠름 (바로 데이터)</td>
<td>주소 찾아서 한 번 더 점프</td>
</tr>
<tr>
<td>범위 검색</td>
<td>매우 빠름 (순차 I/O)</td>
<td>느림 (랜덤 I/O)</td>
</tr>
<tr>
<td>보조 인덱스</td>
<td>리프에 <strong>PK 값</strong> 저장</td>
<td>리프에 <strong>Row ID</strong> 저장</td>
</tr>
<tr>
<td>저장 공간</td>
<td>큼 (데이터 포함)</td>
<td>작음 (주소만)</td>
</tr>
<tr>
<td>삽입/삭제</td>
<td>느림 (정렬 유지 필요)</td>
<td>빠름 (뒤에 붙이면 끝)</td>
</tr>
</tbody></table>
<h2 id="44-mysql의-multi-range-read-mrr">4.4 MySQL의 Multi-Range Read (MRR)</h2>
<ul>
<li><strong>보조 인덱스 탐색 → PK 값 모아 정렬 → PK 순서대로 클러스터링 인덱스 접근</strong></li>
<li>불필요한 랜덤 I/O를 줄이고, <strong>PK 정렬된 순차 읽기</strong>로 성능 개선</li>
</ul>
<h2 id="45-클러스터링-인덱스-특징-정리">4.5 클러스터링 인덱스 특징 정리</h2>
<ul>
<li><p><strong>PK를 인덱스로 관리하는 이유</strong></p>
<p>  → 레코드 정렬 상태를 보장해 <strong>범위 검색·정렬 최적화</strong></p>
</li>
<li><p><strong>보조 인덱스에 PK 저장하는 이유</strong></p>
<p>  → Row ID 대신 PK를 쓰면 <strong>주소 변경에도 안정적</strong>이고,</p>
<p>  PK만 있으면 곧바로 클러스터링 인덱스를 통해 데이터 접근 가능</p>
</li>
</ul>