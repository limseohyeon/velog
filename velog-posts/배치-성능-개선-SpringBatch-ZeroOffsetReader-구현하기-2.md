<h1 id="0-개요">0. 개요</h1>
<p>회원약관에 따라 탈퇴상태로 변경 후 6개월이 지나면 DB에서 영구 삭제(HardDelete)를 구현해야했다.</p>
<p>그러던 중 Spring Batch의 ItemReader은 limitoffset 기반으로 처리해야 할 데이터가 클수록 성능이 급격하게 저하된다는 글을 보게 되었다.</p>
<p>이번 글은 Batch의 Reader과 그 동작 방식에 대해 알아보고 ZeroOffset Reader을 구현했던 과정을 기록하고자 한다.</p>
<h1 id="1-batch의-itemreader">1. Batch의 ItemReader</h1>
<hr />
<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/b9aedc9e-f157-4591-a00c-7a01cc6a8a3a/image.png" /></p>
<p>Spirng Batch는 대표적으로 <code>Cursor</code>와 <code>Paging</code> 2개의 Reader 타입을 지원한다.</p>
<h2 id="21-cursor">2.1 Cursor</h2>
<p>Cursor타입은 데이터베이스와 커넥션을 맺은 후 데이터를 Streaming해 보낸다. 그리고 Cursor을 한 칸씩 옮기며 데이터를 가져온다.</p>
<ul>
<li>하나의 커넥션으로 배치가 종료될 때까지 사용한다.</li>
<li>배치가 끝나기 전에 커넥션이 먼저 끊어질 수 있는 위험이 있다.</li>
<li>모든 데이터를 메모리에 저장하기 때문에 메모리 사용량이 많다.</li>
</ul>
<h2 id="22-paging">2.2 Paging</h2>
<p>Paging타입은 페이지라는 Chunk 단위로 커넥션을 맺어 데이터를 가져오는 방식이다.</p>
<ul>
<li>페이징 단위로 커넥션하기 때문에 연결 시간이 상대적으로 적다.</li>
<li>페이징 단위로 메모리에 저장하기 대문에 메모리 사용량이 상대적으로 적다.</li>
</ul>
<p>또한 페이징 타입은 더 많은 작업을 필요로 한다.</p>
<ul>
<li>시작 행 번호(offset), 반환할 행 수(limit)를 지정</li>
<li>그에 따라 데이터가 정렬되어있어야 한다.</li>
</ul>
<h2 id="23-타입에-따른-구현체">2.3 타입에 따른 구현체</h2>
<h3 id="cursor-기반-itemreader-구현체">Cursor 기반 ItemReader 구현체</h3>
<ul>
<li><code>JdbcCursorItemReader</code></li>
<li><code>HibernateCursorItemReader</code></li>
<li><code>StoredProcedureItemReader</code></li>
</ul>
<h3 id="paging-기반-itemreader-구현체">Paging 기반 ItemReader 구현체</h3>
<ul>
<li><code>JdbcPagingItemReader</code></li>
<li><code>HibernatePagingItemReader</code></li>
<li><code>JpaPagingItemReader</code></li>
</ul>
<h1 id="2-limitoffset과-zerooffset">2. LimitOffset과 ZeroOffset</h1>
<hr />
<h2 id="11-offset과-limit">1.1 offset과 limit</h2>
<ul>
<li>offset : 조회 시작 기준점</li>
<li>limit : 조회할 결과 개수</li>
</ul>
<h2 id="11-limitoffset">1.1 LimitOffset</h2>
<p>limitoffset이란 offset을 기준으로 limit 만큼의 데이터를 조회하는 방법이다.</p>
<p>offset이 5000, limit이 10인 경우 바로 5000번째 데이터부터 10개를 조회하기 위해서 5010까지  조회하고 앞에 필요하지 않은 5000개의 데이터는 버린다.</p>
<p>데이터가 작을 때는 문제가 발생하지 않지만 전체 데이터가 커질수록 급격히 성능 저하 문제가 발생한다.</p>
<p><img alt="자료 출처 https://youtu.be/L9K0l65wMbQ?si=qlI6qSIEJ7aR2whi" src="https://velog.velcdn.com/images/limseohyeon/post/6979932c-bd50-4db5-bbf8-0a83e30addfe/image.png" /></p>
<h2 id="12-zerooffset">1.2 ZeroOffset</h2>
<p>위 limit offset 문제를 해결하기 위해 offset의 값을 항상 0으로 유지하는 방법이 있다.</p>
<p>이러한 방법이 zeroOffset으로 offset을 사용하지 않고 특정 id를 기준으로 where 절을 사용해 조회하는 방식이다. 이를 통해 항상 limit 만큼의 데이터만 읽어 성능 저하 문제를 방지할 수 있다.</p>
<p><img alt="자료 출처 https://youtu.be/L9K0l65wMbQ?si=qlI6qSIEJ7aR2whi" src="https://velog.velcdn.com/images/limseohyeon/post/3bb72a92-b405-4fc7-805f-e264bf09fcaf/image.png" />
자료 출처 <a href="https://youtu.be/L9K0l65wMbQ?si=qlI6qSIEJ7aR2whi">https://youtu.be/L9K0l65wMbQ?si=qlI6qSIEJ7aR2whi</a></p>
<h1 id="3-zerooffset-구현하기">3. ZeroOffset 구현하기</h1>
<hr />
<p>zeroOffest을 기반으로 동작하는 ItemReader을 구현해보도록 한다. 쿼리 관리 유용성을 위해 QueryDsl을 사용했다.</p>
<h2 id="31-구현-코드">3.1 구현 코드</h2>
<p><strong>&lt;ZeroOffsetReader(CustomReader)&gt;</strong></p>
<pre><code class="language-java">@Slf4j
public class CustomReader implements ItemReader&lt;Member&gt; {

    private final JPAQueryFactory queryFactory;
    private final int pageSize;
    private Long lastSeenId;
    private List&lt;Member&gt; currentPage;
    private int currentIndex;

    public CustomReader(EntityManagerFactory entityManagerFactory, int pageSize) {
        EntityManager entityManager = entityManagerFactory.createEntityManager();
        this.queryFactory = new JPAQueryFactory(entityManager);
        this.pageSize = pageSize;
        this.lastSeenId = null;
        this.currentIndex = 0;
    }

    @Override
    public Member read() {
        if (currentPage == null || currentIndex &gt;= currentPage.size()) {
            fetchNextPage();
        }

        if (currentPage == null || currentPage.isEmpty()) {
            return null;
        }

        Member member = currentPage.get(currentIndex);
        currentIndex++;
        return member;
    }

    private void fetchNextPage() {
        QMember qMember = QMember.member;

        currentPage = queryFactory
            .selectFrom(qMember)
            .where(
                lastSeenId != null ? qMember.memberId.gt(lastSeenId) : null,
                qMember.memberStatus.eq(MemberStatus.WITHDRAWAL).and(qMember.updatedAt.loe(
                    LocalDateTime.now().minusMonths(6)))
            ).orderBy(qMember.memberId.asc())
            .offset(0)
            .limit(pageSize)
            .fetch();

        if (!currentPage.isEmpty()) {
            lastSeenId = currentPage.get(currentPage.size() - 1).getMemberId();
        }
        currentIndex = 0;
    }

}
</code></pre>
<h2 id="31-성능-비교">3.1 성능 비교</h2>
<p>10,000건 기준 JdbcPagingReader(limitOffset) 과 CustomReader(zeroOffset) 처리 시간을 비교해봤다. </p>
<table>
<thead>
<tr>
<th>방식</th>
<th>처리 시간 (ms)</th>
</tr>
</thead>
<tbody><tr>
<td>JdbcPagingItemReader (limit-offset)</td>
<td>38,93</td>
</tr>
<tr>
<td>CustomReader (zero-offset)</td>
<td>29,50</td>
</tr>
</tbody></table>
<p>9,42ms, 차이로 약 24% 속도 개선 되었음을 알 수 있었다.</p>
<h1 id="4-마무리">4. 마무리</h1>
<hr />
<p>처음으로 라이브러리 내장함수를 뒤적거려가며 분석해 봤는데 단순히 배치를 사용하는 것과 그 내부 동작 원리를 이해하는 것은 전혀 다르다는 걸 느꼈다. </p>
<p>이번엔 Reader 성능 개선에 집중했지만, 참고했던 자료에서 다룬 Writer 최적화 부분도 다음 단계로 구현해보며 배치 전체의 효율성을 높이고 싶다.</p>
<h1 id="참고">참고</h1>
<hr />
<p><a href="https://tech.kakaopay.com/post/ifkakao2022-batch-performance-read/">[if kakao 2022] Batch Performance를 고려한 최선의 Reader | 카카오페이 기술 블로그</a></p>
<p><a href="https://tech.kakaopay.com/post/ifkakao2022-batch-performance-aggregation/">[if kakao 2022] Batch Performance를 고려한 최선의 Aggregation | 카카오페이 기술 블로그</a></p>
<p><a href="https://youtu.be/L9K0l65wMbQ?si=qlI6qSIEJ7aR2whi">Batch Performance 극한으로 끌어올리기: 1억 건 데이터 처리를 위한 노력 / if(kakao)2022</a></p>