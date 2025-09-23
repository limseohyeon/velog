<h1 id="0-개요">0. 개요</h1>
<hr />
<p>관리자 - 회원 관리 페이지 요구 사항이 다음과 같았다.</p>
<aside>

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
<p>이러한 요구사항을 만족하기 위해 필터링을 통한 조회 기능을 구현해야 했다. </p>
<h1 id="1-어떤-방법으로-구현-할-것인가">1. 어떤 방법으로 구현 할 것인가?</h1>
<hr />
<p>Spring 프로젝트에서 필터링 조회를 구현하는 방법을 검색해 본 결과 크게 두 가지가 있었다.</p>
<ol>
<li><strong>JPA Specification</strong></li>
<li><strong>Query Dsl</strong></li>
</ol>
<h1 id="2-jpa-specification">2. JPA Specification</h1>
<hr />
<p><em>(Query DSL은 이미 여러 번 사용한 적이 있는 데 JPA Specification은 처음 들어 봤기 때문에 아래 간단하게 정리해 봤다.)</em></p>
<p>검색 조건을 <strong>메서드 형태로 추상화</strong>해 Repository 인터페이스에서 해당 검색 조건을 조합하고 쿼리하기 쉽게 할 수 있는 Spring Data JPA 기능이다. <strong>즉, 동적 쿼리를 만들 수 있게 지원하는 JPA기능</strong>이다.</p>
<p>JPA에서 제공하는 Criteria를 통해 <strong>Specification을 생성</strong>하고, 여러 <strong>Specification을 조합</strong>해 하나의 동적 쿼리를 만들 수 있다.</p>
<hr />
<h2 id="21-jpa-specificaiton-사용-방법">2.1 JPA Specificaiton 사용 방법</h2>
<h3 id="211-criteria-api">2.1.1 Criteria API</h3>
<p>Criteria API란 동적 쿼리를 사용하기 위한 JPA 라이브러리 이다. JPA Specification은 criteria API 기반으로 만들어진다.</p>
<p><strong>예제) age가 20이상인 학생 list를 조회하기</strong></p>
<pre><code class="language-java">// 1. CriteriaBuilder 가져오기
CriteriaBuilder cb = entityManager.getCriteriaBuilder();

// 2. CriteriaQuery 생성 (해당 쿼리의 결과 타입을 결정한다.)
CriteriaQuery&lt;Student&gt; query = cb.createQuery(Student.class);

// 3. Root 설정 (FROM Student s)
Root&lt;Student&gt; root = query.from(Student.class);

// 4. 조건 설정 (WHERE s.age &gt;= 20)
Predicate agePredicate = cb.greaterThanOrEqualTo(root.get(&quot;age&quot;), 20);

// 5. 조건을 쿼리에 적용
query.where(agePredicate);

// 6. 정렬(Optional) - 예시로 이름 기준 오름차순 정렬
query.orderBy(cb.asc(root.get(&quot;name&quot;)));

// 7. 쿼리 실행
TypedQuery&lt;Student&gt; typedQuery = entityManager.createQuery(query);

// 페이징 처리 (선택 사항) - 0번째부터 최대 10개 가져오기
typedQuery.setFirstResult(0); // offset
typedQuery.setMaxResults(10); // limit

List&lt;Student&gt; studentList = typedQuery.getResultList();

// 결과 반환
return studentList;</code></pre>
<table>
<thead>
<tr>
<th>단계</th>
<th>역할</th>
<th>SQL로 치면</th>
</tr>
</thead>
<tbody><tr>
<td><code>CriteriaBuilder</code></td>
<td>쿼리 만들 도구 제공</td>
<td>없음</td>
</tr>
<tr>
<td><code>CriteriaQuery&lt;Student&gt;</code></td>
<td>쿼리 객체, 결과 타입 정의</td>
<td><code>SELECT * FROM Student</code></td>
</tr>
<tr>
<td><code>Root&lt;Student&gt;</code></td>
<td>테이블의 별칭 설정</td>
<td><code>FROM Student s</code></td>
</tr>
<tr>
<td><code>Predicate</code></td>
<td>조건 생성</td>
<td><code>WHERE s.age &gt;= 20</code></td>
</tr>
<tr>
<td><code>query.where()</code></td>
<td>WHERE 절 추가</td>
<td><code>WHERE</code></td>
</tr>
<tr>
<td><code>query.orderBy()</code></td>
<td>정렬 조건 설정</td>
<td><code>ORDER BY s.name ASC</code></td>
</tr>
<tr>
<td><code>TypedQuery</code></td>
<td>쿼리 실행 준비</td>
<td>준비된 SQL 실행</td>
</tr>
<tr>
<td><code>setFirstResult()</code>, <code>setMaxResults()</code></td>
<td>페이징 처리</td>
<td><code>LIMIT</code>, <code>OFFSET</code></td>
</tr>
<tr>
<td><code>getResultList()</code></td>
<td>쿼리 실행 및 결과 받기</td>
<td>실행 결과 받기</td>
</tr>
</tbody></table>
<hr />
<h3 id="212-jpaspecificationexecutor-인터페이스-상속하기">2.1.2 JpaSpecificationExecutor 인터페이스 상속하기</h3>
<p>Specification을 인자로 받는 <code>findAll()</code> 메서드를 사용하기 위해 <code>Repository JpaSpecificationExcutor&lt;Member&gt;</code> 을 상속 받는다.</p>
<pre><code class="language-java">public interface MemberRepository extends JpaRepository&lt;Member, Long&gt;, CustomMemberRepository,
    JpaSpecificationExecutor&lt;Member&gt; {
}</code></pre>
<p>JpaSpecificationExecutor 는 기존 JpaRepository와 다르게 Specification을 인자로 받는다.</p>
<pre><code class="language-java">public interface JpaSpecificationExecutor&lt;T&gt; {
    Optional&lt;T&gt; findOne(@Nullable Specification&lt;T&gt; spec);
    List&lt;T&gt; findAll(@Nullable Specification&lt;T&gt; spec);
    ...
}</code></pre>
<hr />
<h3 id="213-specification-만들기">2.1.3 Specification 만들기</h3>
<ul>
<li>구현하려는 조건(필터) 별로 Specification을 만든다.</li>
<li><code>findAll(Specification&lt;T&gt; spec);</code> 을 통해 where 쿼리를 날린다.</li>
</ul>
<p><strong>Specification.class</strong></p>
<pre><code class="language-java">import org.springframework.data.jpa.domain.Specification;
import jakarta.persistence.criteria.*;

public class ProductSpecification {

    public static Specification&lt;Product&gt; hasName(String name) {
        return (Root&lt;Product&gt; root, CriteriaQuery&lt;?&gt; query, CriteriaBuilder cb) -&gt;
                cb.like(root.get(&quot;name&quot;), &quot;%&quot; + name + &quot;%&quot;);
    }

    public static Specification&lt;Product&gt; hasCategory(String category) {
        return (Root&lt;Product&gt; root, CriteriaQuery&lt;?&gt; query, CriteriaBuilder cb) -&gt;
                cb.equal(root.get(&quot;category&quot;), category);
    }

    public static Specification&lt;Product&gt; priceGreaterThan(Double price) {
        return (Root&lt;Product&gt; root, CriteriaQuery&lt;?&gt; query, CriteriaBuilder cb) -&gt;
                cb.greaterThan(root.get(&quot;price&quot;), price);
    }
}
</code></pre>
<ul>
<li><p>일반 함수 버전</p>
<pre><code class="language-java">  import org.springframework.data.jpa.domain.Specification;
  import jakarta.persistence.criteria.*;

  public class ProductSpecification {

      // name 필터
      public static Specification&lt;Product&gt; hasName(String name) {
          return new Specification&lt;Product&gt;() {
              @Override
              public Predicate toPredicate(Root&lt;Product&gt; root, CriteriaQuery&lt;?&gt; query, CriteriaBuilder cb) {
                  return cb.like(root.get(&quot;name&quot;), &quot;%&quot; + name + &quot;%&quot;);
              }
          };
      }

      // category 필터
      public static Specification&lt;Product&gt; hasCategory(String category) {
          return new Specification&lt;Product&gt;() {
              @Override
              public Predicate toPredicate(Root&lt;Product&gt; root, CriteriaQuery&lt;?&gt; query, CriteriaBuilder cb) {
                  return cb.equal(root.get(&quot;category&quot;), category);
              }
          };
      }

      // price 필터
      public static Specification&lt;Product&gt; priceGreaterThan(Double price) {
          return new Specification&lt;Product&gt;() {
              @Override
              public Predicate toPredicate(Root&lt;Product&gt; root, CriteriaQuery&lt;?&gt; query, CriteriaBuilder cb) {
                  return cb.greaterThan(root.get(&quot;price&quot;), price);
              }
          };
      }
  }</code></pre>
</li>
</ul>
<p><strong>service.class</strong></p>
<ul>
<li>specification을 조합해서 사용한다.</li>
</ul>
<pre><code class="language-java">import org.springframework.stereotype.Service;
import org.springframework.data.jpa.domain.Specification;
import java.util.List;

@Service
public class ProductService {

    private final ProductRepository productRepository;

    public ProductService(ProductRepository productRepository) {
        this.productRepository = productRepository;
    }

    public List&lt;Product&gt; filterProducts(String name, String category, Double price) {
        Specification&lt;Product&gt; spec = Specification.where(null);

        if (name != null &amp;&amp; !name.isEmpty()) {
            spec = spec.and(ProductSpecification.hasName(name));
        }

        if (category != null &amp;&amp; !category.isEmpty()) {
            spec = spec.and(ProductSpecification.hasCategory(category));
        }

        if (price != null) {
            spec = spec.and(ProductSpecification.priceGreaterThan(price));
        }

        return productRepository.findAll(spec);
    }
}
</code></pre>
<h1 id="3-query-dsl-vs-jpa-specification">3. Query DSL VS JPA Specification</h1>
<hr />
<p>그러나 Specification은 실무에서 잘 사용하지 않는다고 한다. 그 대신 Query DSL을 사용하는데 그 이유는 아래와 같다.</p>
<ul>
<li><strong>Where의 추상</strong> : group, projeccton 등 복잡한 조건을 처리하는 것은 Criteria API를 직접 사용하는 것이 나을 정도로 불편하거나 지원되지 않는다.</li>
<li><strong>타입 안정성</strong> : 문자열로 필드를 넘기기 때문에 오타, 필드 변경 시 런타임 오류가 발생할 가능성이 있다. <code>root.get(&quot;fieldName&quot;)</code></li>
<li><strong>가독성/ 유지보수성</strong> : 복잡한 조건을 추가하려면 코드가 길고 가독성이 떨어진다.</li>
</ul>
<h1 id="4-결론---어떤-것을-사용할-것인가">4. 결론 - 어떤 것을 사용할 것인가?</h1>
<p>현재 내 프로젝트에서는 Social login을 위한 provider 테이블과 member 테이블이 별도로 있기 때문에 <code>join</code>이 필수적이었고, 기간별 조회, 검색, 등급 등… 조건을 중복 적용해야 했기 때문에 Specification을 사용하는 것이 적합하지 않다고 생각 되었다. 즉, 복잡한 쿼리를 작성하지 않아도 된다는 점, Member + Provider Join시 발생할 수 있는 타입 안정성 문제에서도 이점이 있었다.</p>
<p>또한, JPA Specificaion을 사용하는 주된 이유 중 하나가 불필요한 라이브러리를 추가하지 않기 위함인데 현재 프로젝트에서는 이미 Query DSL을 사용하고 있었기 때문에 JPA Specificaition을 고집할 필요가 없었다.</p>
<p><strong>결론 : Query DSL을 이용해 필터 기능을 구현하기로 했다.</strong></p>