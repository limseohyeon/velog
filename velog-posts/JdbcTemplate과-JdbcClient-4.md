<!-- ENTRY_ID: https://velog.io/@limseohyeon/JdbcTemplate%EA%B3%BC-JdbcClient -->
<!-- SOURCE_TITLE: JdbcTemplate과 JdbcClient -->

<h1 id="0-jdbc란">0. Jdbc란?</h1>
<hr />
<p>Jdbc(Java Database Connectivity)는 Java 애플리케이션과 데이터베이스를 연결할 수 있도록 하는 자바 API이다.</p>
<h3 id="특징">특징</h3>
<ul>
<li>커넥션/State,emt/ResultSet 직접 관리</li>
<li>try-catch-finally 반복 코드 많음</li>
</ul>
<p>저수준 API로 직접 제어 가능하지만 코드가 길고 실수 위험이 높다는 단점이 있다.</p>
<pre><code class="language-java">Connection conn = DriverManager.getConnection(&quot;jdbc:mysql://localhost:3306/test&quot;, &quot;user&quot;, &quot;pw&quot;);
PreparedStatement ps = conn.prepareStatement(&quot;SELECT * FROM users WHERE id = ?&quot;);
ps.setLong(1, id);
ResultSet rs = ps.executeQuery();
User user = null;
if (rs.next()) {
    user = new User(rs.getLong(&quot;id&quot;), rs.getString(&quot;name&quot;));
}
rs.close();
ps.close();
conn.close();
</code></pre>
<h1 id="1-jdbctemplate">1. JdbcTemplate</h1>
<hr />
<p>그래서 나온 것이 스프링이 제공하는 JDBC 편의 클래스인 JdbcTempate다.</p>
<h3 id="특징-1">특징</h3>
<ul>
<li>커넥션 관리, 리소스 해제 자동 처리</li>
<li>SQL 작성만 하면 됨</li>
</ul>
<pre><code class="language-java">String sql = &quot;SELECT * FROM users WHERE id=?&quot;;
User user = jdbcTemplate.queryForObject(sql,
        new BeanPropertyRowMapper&lt;&gt;(User.class), id);</code></pre>
<h2 id="11-jdbctemplate-와-optional">1.1 JdbcTemplate 와 Optional</h2>
<p> <strong>JdbcTemplate에서는 Optional을 지원하지 않는데 그 이유가 뭘까?</strong></p>
<ul>
<li>너무 많은 메소드 오버로딩 : ueryForObject에 이미 수많은 메소드가 오버로딩 되어있다.</li>
<li>JdbcTempalate의 책임이 아님 (≠ db접근의 편리성을 위한 기능이 아님)</li>
<li>대체 방법이 존재한다.</li>
</ul>
<h1 id="2-jdbcclient">2. JdbcClient</h1>
<hr />
<p>JdbcClient는 스프링 최신 Jdbc Api로 JdbcTemplate의 기능과 더불어 현대적인 문법을 지원한다.(Optional, Stream, Record 등…)</p>
<h3 id="특징-2">특징</h3>
<ul>
<li>메서드 체이닝으로 가독성 향상</li>
<li>직관적인 파라미터 바인딩 (Named Parameter)</li>
<li>Optional, Stream 결과 처리 지원</li>
</ul>
<p>JdbcTemplate의 개선 버전으로 더 깔끔하고 타입 안전하다.</p>
<pre><code class="language-java">User user = jdbcClient.sql(&quot;SELECT * FROM users WHERE id = :id&quot;)
        .param(&quot;id&quot;, id)
        .query(User.class)
        .single();</code></pre>