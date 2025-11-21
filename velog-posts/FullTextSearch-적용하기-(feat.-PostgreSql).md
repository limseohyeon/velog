<!-- ENTRY_ID: https://velog.io/@limseohyeon/FullTextSearch-%EC%A0%81%EC%9A%A9%ED%95%98%EA%B8%B0-feat.-PostgreSql -->
<!-- SOURCE_TITLE: FullTextSearch 적용하기 (feat. PostgreSql) -->

<p>왜 like 연산자를 사용하면 안 되는지, full Text Search에 어떤 이점이 있는지는 해당 글에서 다루지 않는다.</p>
<p>오늘은 FTS 구성과 사용 방법에 대해 간단하게 알아보는 것을 목표로 한다.</p>
<h1 id="1-공식문서">1. 공식문서</h1>
<hr />
<p><a href="https://www.postgresql.org/docs/current/textsearch.html">Chapter 12. Full Text Search</a></p>
<h1 id="2-적용">2. 적용</h1>
<hr />
<pre><code class="language-sql">// 기존
&lt;select id=&quot;findUserIdByName&quot; parameterType=&quot;string&quot; resultType=&quot;string&quot;&gt;
    SELECT user_nm AS name
    FROM tb_user
    WHERE user_nm = #{userName} 
&lt;/select&gt;

//변경 후
 &lt;select id=&quot;findUserIdByName&quot; parameterType=&quot;string&quot; resultType=&quot;string&quot;&gt;
        SELECT
            user_nm AS name
        FROM tb_user
        WHERE to_tsvector(user_nm) @@ to_tsquery(replace(#{userName}, ' ', ' &amp;amp; ') || ':*');
    &lt;/select&gt;</code></pre>
<ul>
<li><strong>tsvector</strong> :데이터(문장)를 단어/형태소 리스트로 변환 (즉, 검색 필드 모음)</li>
<li><strong>to_tsquery 함수</strong> : 검색어를 검색 쿼리로 변환 (AND, OR 가능)</li>
<li><strong>plainto_tsquery</strong> : 검색어를 자연어 검색식으로 변환(공백 분리된 문자열을 자연어 검색쿼리로 변환 즉, 그냥 단어 입력시 자동으로 tsquery 변환 (기준이 공백인 것)</li>
<li><code>@@</code> : <code>tsvector</code> 와 <code>tsquery</code> 를 비교하는 <strong>매칭 연산자</strong></li>
</ul>
<h1 id="3-예시">3. 예시</h1>
<hr />
<h3 id="기본-예시">기본 예시</h3>
<pre><code class="language-sql">SELECT user_nm
FROM tb_user
WHERE to_tsvector(user_nm) @@ plainto_tsquery('철수');</code></pre>
<p>👉 결과: <code>'철수'</code> 라는 단어가 들어간 레코드 검색</p>
<p>(철수가 / 철수는 / 김철수 / 철수야 / 철수다 모두 가능 그러나 철수안경, 철수바지 와 같은 것은 불가능하다.</p>
<p>PostgreSQL의 한국어 형태소 분석 방식은 조사 (은/는/가/이/야/다 등)은 분리하여 판단하기 때문에 검색 가능하지만 철수안경은 한 단어로 취급하여 형태소로 분리되지 않는다.</p>
<hr />
<h3 id="and-검색-두-단어-모두-포함된-문장">AND 검색 (두 단어 모두 포함된 문장)</h3>
<pre><code class="language-sql">WHERE to_tsvector(user_nm) @@ to_tsquery('김 &amp; 철수');</code></pre>
<p>→ <code>&quot;김&quot;</code> <strong>AND</strong> <code>&quot;철수&quot;</code> 모두 포함된 문장만 검색</p>
<hr />
<h3 id="or-검색-둘-중-하나라도">OR 검색 (둘 중 하나라도)</h3>
<pre><code class="language-sql">WHERE to_tsvector(user_nm) @@ to_tsquery('김 | 철수');</code></pre>
<hr />
<h3 id="부분-검색접두어-검색">부분 검색(접두어 검색)</h3>
<p><code>:*</code> 붙이면 <code>&quot;철수&quot;</code>로 시작하는 모든 단어 검색</p>
<pre><code class="language-sql">WHERE to_tsvector(user_nm) @@ to_tsquery('철수:*');</code></pre>
<hr />
<h3 id="mybatis-예시로-정리">MyBatis 예시로 정리</h3>
<pre><code class="language-xml">&lt;select id=&quot;findUserIdByName&quot; parameterType=&quot;string&quot; resultType=&quot;string&quot;&gt;
    SELECT user_nm AS name
    FROM tb_user
    WHERE to_tsvector('simple', user_nm) @@ plainto_tsquery('simple', #{userName});
&lt;/select&gt;</code></pre>
<p>아래는 유사검색을 적용하기 위한 경우에 적용될 수 있는 쿼리다.</p>
<pre><code class="language-sql">WHERE to_tsvector(user_nm) @@ to_tsquery(replace(#{userName}, ' ', ' &amp;amp; ') || ':*');
</code></pre>
<ul>
<li><code>${userName}</code> :  myBatis에서 바인딩 되는 값</li>
<li><code>(replace(#{userName}, ' ', ' &amp;amp; ')</code><ul>
<li>공백을 &amp;(AND) 연산자로 치환하기 위해 사용</li>
<li><code>&amp;amp</code> : XML에서 &amp;는 예약 문자이기 때문에 escape 적용</li>
<li><code>|| ':*’</code> PostgreSQL에서 접두사 검색 의미</li>
</ul>
</li>
</ul>
<h3 id="toto">//TOTO</h3>
<p>  like, 단순 where, FTS 성능 비교하기!</p>