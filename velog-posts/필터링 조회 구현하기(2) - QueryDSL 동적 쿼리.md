<h1 id="0-개요">0. 개요</h1>
<p>앞 글에 필터링 조회 기능을 구현하기 위해 <strong>Query DSL</strong>을 사용하기로 결정 했었다.</p>
<aside>

<p>🔔<strong>요구사항</strong></p>
<ul>
<li>관리자는 모든 회원을 조회 할 수 있다.</li>
<li>관리자는 회원을 아래 조건에 따라 조회할 수 있다.<ul>
<li>회원 상태 (가입, 탈퇴)</li>
<li>가입 기간 (start_date - end_date)</li>
<li>회원 등급 (사용자, 관리자)</li>
<li>email 혹은 닉네임 검색</aside>

</li>
</ul>
</li>
</ul>
<h1 id="1-query-dsl">1. Query DSL</h1>
<hr />
<p>Query DSL의 기본적인 사용 방법과 설명은 이 글에서는 생략 했으므로 아래 링크를 참조.</p>
<h2 id="12-qclass">1.2 Qclass</h2>
<p>QueryDsl을 사용할 때 Qclass가 기본적으로 생성 되는데 왜 Entity를 사용하지 않고 QClass를 만들어서 사용할까?</p>
<h3 id="121-jpa_apt">1.2.1 JPA_APT</h3>
<p>JPA_API는 <code>@Entity</code>같은 특정 어노테이션을 찾고 해당 클래스를 분석해 QClass를 만드는 역할을 한다.</p>
<ul>
<li>APT<ul>
<li>어노테이션이 있는 기존 코드를 바탕으로 새로운 코드 혹은 파일을 만든다. 쉬운 예q시로 Lonbok의 <code>@Getter</code>, <code>@Setter</code>가 있다.</li>
</ul>
</li>
</ul>
<h3 id="122-그래서-qclass란">1.2.2 그래서 QClass란?</h3>
<p>엔티티 클래스의 메타 정보를 담고 있는 클래스로, 이를 통해 타입 안정성을 보장하며 쿼리를 작성할 수 있다.</p>
<ul>
<li>QClass는 엔티티 속성을 정적인 방식으로 표현하므로 IDE의 <strong>자동 완성 기능을 활용</strong>할 수 있고, 속성 이름을 직접 기억하거나 확인하지 않아도 된다.</li>
<li>QClass는 엔티티 속성의 타입을 정확하게 표현하므로, 타입에 맞지 않는 연산이나 비교를 시도하면 <strong>컴파일러 오류를 감지</strong>할 수 있다.</li>
</ul>
<p>엔티티 클래스는 데이터베이스 테이블의 매핑을 담당하고, QClass는 쿼리 작성을 위한 편의성과 안전성을 제공하며 유지보수의 편의성 및 실수 방지를 막는다. 즉, 컴파일 단계에서 에러를 잡을 수 있도록 한다. (JPQL은 런타임에서 오류가 발생한다.)</p>
<h2 id="13-projection">1.3 Projection</h2>
<p>일반적으로 생성되는 QClass는 Eneity의 모든 필드를 생성한다. 하지만 Entity 이외의 값을 리턴하거나 필요한 필드만 반환해야 하는 경우 QClass를  이용한 반환은 비효율 적이다. 이때 사용하는 것이 Projection 이다.</p>
<h3 id="131-프로젝션을-사용하는-방법은-총-3가지가-있다">1.3.1 프로젝션을 사용하는 방법은 총 3가지가 있다.</h3>
<ul>
<li>Field 조회</li>
<li>생성자 조회</li>
<li>Setter 조회</li>
</ul>
<h3 id="132-field-조회">1.3.2 Field 조회</h3>
<p>데이터를 담고 싶은 클래스의 필드명을 활용하는 방법.</p>
<p><strong>entity.class</strong></p>
<pre><code class="language-java">@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public classStudent {
    private String name;
    private int age;
}</code></pre>
<p>필드명에 맞는 변수명을 넣어 사용한다.</p>
<pre><code class="language-java">
@Repository
public class StudentRepositoryImpl {

    @Autowired
    private JPAQueryFactory jpaQueryFacotry;

    public List&lt;SomeStudent&gt; findForStudentList() {
        return jpaQueryFacotry.select(Projections.fields(Student.class,
                                                                 QStudent.student.name,
                                                                 QStudent.student.age))
                                      .from(QStudent.student)
                                      .fetch();
    }
}</code></pre>
<h3 id="133-생성자-조회">1.3.3 생성자 조회</h3>
<p>클래스에 존재하는 생성자를 이용하기 때문에 필드명이 동일하지 않아도 정상적으로 사용 가능하다.</p>
<pre><code class="language-java">@Repository
public class StudentRepositoryImpl {

    @Autowired
    private JPAQueryFactory jpaQueryFacotry;

    public List&lt;SomeStudent&gt; findForSomeStudentList() {
        return jpaQueryFacotry.select(Projections.constructor(Student.class,
                                                                      Expressions.asString(QStudent.student.name).as(&quot;randomName&quot;), // 필드명 변경하기
                                                                      QStudent.student.age))
                                      .from(QStudent.student)
                                      .fetch();
    }
}</code></pre>
<h3 id="134-setter-조회">1.3.4 Setter 조회</h3>
<p>Setter을 이용하는 방법으로 field와 이름이 같지 않으면 데이터가 정상적으로 적재되지 않는다.</p>
<pre><code class="language-java">@Repository
public class StudentQueryRepository {

    @Autowired
    private JPAQueryFactory jpaQueryFacotry;

    public List&lt;SomeStudent&gt; findForSomeStudentList() {
        return jpaQueryFacotry.select(Projections.bean(SomeStudent.class,
                                                               QStudent.student.name,
                                                               QStudent.student.age))
                                      .from(QStudent.student)
                                      .fetch();
    }
}</code></pre>
<p>현재 사용자에 관한 테이블은 회원의 기본 정보를 담고 있는 Member 테이블과,  Social Login 정보를 담고 있는 Provider 두 개의 테이블이 존재한다. 두 개의 필드를 합친 Dto로 return하기 위해 Projection을 사용해 QBean을 생성해야 한다. 아래는 이를 고려해 생성한 QBean이다.</p>
<p><strong>CustomMemberRepositoryImpl.class</strong></p>
<pre><code class="language-java">
@Repository
@RequiredArgsConstructor
public class CustomMemberRepositoryImpl implements CustomMemberRepository {

    private static final QBean&lt;AdminMemberResponse&gt; adminMemberResponseDto = Projections.fields(
        AdminMemberResponse.class, member.memberId.as(&quot;memberId&quot;), member.email, member.nickname,
        member.role,
        member.memberStatus.as(&quot;status&quot;), member.createdAt,
        socialProvider.oauthProvider.as(&quot;oauthProvider&quot;)
    )
}</code></pre>
<h2 id="13-query-dsl-의-동적-쿼리">1.3 Query DSL 의 동적 쿼리</h2>
<p>Query Dsl에서는 Predicate 구현체를 넘겨주는 것으로 where절을 작성할 수 있다.</p>
<p>이 때 Predicate 구현체로 <strong>BooleanExpression</strong> 객체를 넘기면 된다.</p>
<h3 id="131-query-dsl의-where-절">1.3.1 Query Dsl의 where 절</h3>
<p>Query Dsl의 where절은 null 값을 무시하는 특성이 있다. 따라서, 필터링에 적용되어야 하는 조건은 Predicate를 구현한 구현체를 넘겨주고 적용되지 않는 조건은 null을 넘겨주면 된다.</p>
<h3 id="132-booleanexpression">1.3.2 BooleanExpression</h3>
<ul>
<li>BooleanExpression은 JPQL이 제공하는 모든 검색 조건을 제공한다.</li>
<li>null 값을 받는 경우 IllegalArgumentException이 발생하기 때문에 null이 입력되는 경우에 대한 조건을 작성해야한다.</li>
</ul>
<h3 id="133-작성한-predicate">1.3.3 작성한 Predicate</h3>
<pre><code class="language-java"> // 회원 상태 필터
 private BooleanExpression eqStatus(MemberStatus status) {
        return (status != null ? member.memberStatus.eq(status) : Expressions.TRUE);
    }
// 회원 권한 필터
    private BooleanExpression eqRole(MemberRole role) {
        return (role != null ? member.role.eq(role) : Expressions.TRUE);
    }
// 소셜 필터
    private BooleanExpression eqOAuthProvider(Provider oauthProvider) {
        return ((oauthProvider != null)
            ? socialProvider.oauthProvider.eq(oauthProvider) : Expressions.TRUE);
    }

// 검색 필터
    private BooleanExpression eqSearch(String search) {
        return ((search != null &amp;&amp; !search.isEmpty()) ? member.email.eq(search)
            .or(member.nickname.eq(search)) : Expressions.TRUE);
    }

 // 기간 필터
    private BooleanExpression betweenCreatedAt(LocalDateTime startDate, LocalDateTime endDate) {
        if (startDate != null &amp;&amp; endDate != null)
            return member.createdAt.between(startDate, endDate);
        return Expressions.TRUE;
    }</code></pre>
<h3 id="134-완성-코드">1.3.4 완성 코드</h3>
<pre><code class="language-java">@Slf4j
@Repository
@RequiredArgsConstructor
public class CustomMemberRepositoryImpl implements CustomMemberRepository {

    private static final QBean&lt;WithdrawalMemberResponse&gt; withdrawalMemberResponseDto = Projections.fields(
        WithdrawalMemberResponse.class, member.memberId, member.email, member.nickname,
        member.profileImageUrl, member.role, member.memberStatus,
        member.createdAt, member.updatedAt);

    private static final QBean&lt;AdminMemberResponse&gt; adminMemberResponseDto = Projections.fields(
        AdminMemberResponse.class, member.memberId.as(&quot;memberId&quot;), member.email, member.nickname,
        member.role,
        member.memberStatus.as(&quot;status&quot;), member.createdAt,
        socialProvider.oauthProvider.as(&quot;oauthProvider&quot;)
    );

    private static final QMember qmember = QMember.member;

    private final JPAQueryFactory jpaQueryFactory;

    @Override
    public PageResponse&lt;AdminMemberResponse&gt; findAllMembers(Pageable pageable) {
        List&lt;AdminMemberResponse&gt; members = jpaQueryFactory
            .select(adminMemberResponseDto)
            .from(member)
            .leftJoin(socialProvider).on(socialProvider.member.memberId.eq(member.memberId))
            .offset(pageable.getOffset())
            .limit(pageable.getPageSize())
            .orderBy(member.email.asc())
            .fetch();

        long total = jpaQueryFactory
            .select(member.count())
            .from(member)
            .fetchOne();

        return new PageResponse&lt;&gt;(new PageImpl&lt;&gt;(members, pageable, total));
    }
    @Override
    public Page&lt;WithdrawalMemberResponse&gt; findAllWithdrawMembers(Pageable pageable) {
        List&lt;WithdrawalMemberResponse&gt; members = jpaQueryFactory
            .select(withdrawalMemberResponseDto)
            .from(member)
            .where(member.memberStatus.eq(MemberStatus.WITHDRAWAL))
            .offset(pageable.getOffset())
            .limit(pageable.getPageSize())
            .orderBy(member.email.asc())
            .fetch();

        long total = jpaQueryFactory
            .select(member.count())
            .from(member)
            .where(member.memberStatus.eq(MemberStatus.WITHDRAWAL))
            .fetchOne();

        return new PageImpl&lt;&gt;(members, pageable, total);
    }

    @Override
    public PageResponse&lt;AdminMemberResponse&gt; findAllMemberWithFilter(Pageable pageable,
        MemberFilterRequest filter) {

        List&lt;AdminMemberResponse&gt; members = jpaQueryFactory
            .select(adminMemberResponseDto)
            .from(member)
            .leftJoin(socialProvider).on(socialProvider.member.memberId.eq(member.memberId))
            .where(
                eqSearch(filter.getSearch()),
                eqStatus(filter.getStatus()),
                eqRole(filter.getRole()),
                eqOAuthProvider(filter.getOAuthProvider()),
                betweenCreatedAt(filter.getStartDate(), filter.getEndDate())
            )
            .offset(pageable.getOffset())
            .limit(pageable.getPageSize())
            .orderBy(member.email.asc())
            .fetch();

        long total = jpaQueryFactory
            .select(member.count())
            .from(member)
            .leftJoin(socialProvider).on(socialProvider.member.memberId.eq(member.memberId))
            .where(
                eqSearch(filter.getSearch()),
                eqStatus(filter.getStatus()),
                eqRole(filter.getRole()),
                eqOAuthProvider(filter.getOAuthProvider()),
                betweenCreatedAt(filter.getStartDate(), filter.getEndDate())
            )
            .fetchOne();

        return new PageResponse&lt;&gt;(new PageImpl&lt;&gt;(members, pageable, total));
    }

    @Override
    public Optional&lt;Member&gt; findByProviderAndSocialId(Provider provider, String socialId) {
        return Optional.ofNullable(jpaQueryFactory.select(member)
            .from(member)
            .innerJoin(socialProvider)
            .on(member.memberId.eq(socialProvider.member.memberId))
            .where(socialProvider.oauthProvider.eq(provider)
                .and(socialProvider.socialId.eq(socialId))).fetchOne());
    }

    private BooleanExpression eqStatus(MemberStatus status) {
        return (status != null ? member.memberStatus.eq(status) : Expressions.TRUE);
    }

    private BooleanExpression eqRole(MemberRole role) {
        return (role != null ? member.role.eq(role) : Expressions.TRUE);
    }

    private BooleanExpression eqOAuthProvider(Provider oauthProvider) {
        return ((oauthProvider != null)
            ? socialProvider.oauthProvider.eq(oauthProvider) : Expressions.TRUE);
    }

    // 검색
    private BooleanExpression eqSearch(String search) {
        return ((search != null &amp;&amp; !search.isEmpty()) ? member.email.eq(search)
            .or(member.nickname.eq(search)) : Expressions.TRUE);
    }

    // 기간 조회
    private BooleanExpression betweenCreatedAt(LocalDateTime startDate, LocalDateTime endDate) {
        if (startDate != null &amp;&amp; endDate != null)
            return member.createdAt.between(startDate, endDate);
        return Expressions.TRUE;
    }
}</code></pre>