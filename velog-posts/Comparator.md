<!-- ENTRY_ID: https://velog.io/@limseohyeon/Comparator -->
<!-- SOURCE_TITLE: Comparator -->

<h1 id="comparator">Comparator</h1>
<hr />
<pre><code class="language-java">* o1(앞), o2(뒤) 인 경우
Collections.sort(list, new Comparator&lt;String&gt;() {
            @Override
            public int compare(String o1, String o2) {

                                return o1.compareTo(o2); // 오름차순
                        //return o2.compareTo(o1); // 내림차순

            }
        });</code></pre>
<p>사용자가 정한 규칙대로 두 값을 비교하는 인터페이스</p>
<p>반환 값에 따라 정렬 우선순위를 결정 한다. </p>
<table>
<thead>
<tr>
<th>return</th>
<th></th>
</tr>
</thead>
<tbody><tr>
<td>음수</td>
<td>O1 - O2</td>
</tr>
<tr>
<td>0</td>
<td>O1 == O2 (순서X)</td>
</tr>
<tr>
<td>양수</td>
<td>O2 - O1</td>
</tr>
</tbody></table>
<p>return 값이 음수, 양수냐에 따라 정렬 순서가 결정되기 때문에</p>
<p>기본적으로 return o1-o2; 과 같이 사용해도 되지만 문자열은 빼기가 불가능하기 때문에  <code>compareTo()</code> 를 사용해 비교한다.</p>