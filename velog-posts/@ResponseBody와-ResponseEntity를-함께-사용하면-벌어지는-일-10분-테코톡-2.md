<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/90d04463-b41d-4518-b82f-354bc001e95e/image.png" />
🔗<a href="https://youtu.be/JOLwv6Btayg?si=6ikoZU6k5oyhfWNq">10분 테코톡 - ResponseBody와 ResponseEntity를 함께 사용하면 벌어지는 일</a></p>
<h1 id="0-restcontroller">0. @RestController</h1>
<hr />
<p>Http 응답 메시지 body에 메시지를 설정하는 방법은 다음과 같이 <strong>2가지가 존재</strong>한다.</p>
<h3 id="responseentityt">@ResponseEntity</h3>
<pre><code class="language-java">@GetMapping(&quot;member&quot;)
public ResponseEntity&lt;Member&gt; getMember(){
    return ResponseEntity.ok(new Member());
}</code></pre>
<ul>
<li>HTTP Entity를 상속 받고 있기 때문에 여러 HTTP 옵션을 설정할 수 있다.</li>
</ul>
<h3 id="responsebody반환-객체">@ResponseBody+반환 객체</h3>
<pre><code class="language-java">@ResponseBody
@GetMapping(&quot;member&quot;)
public Member getMember(){
    return new Member();
}</code></pre>
<ul>
<li>어노테이션 추가만으로 간단하게 HTTP 응답을 할 수 있다.</li>
<li>그러나 HTTP 옵션에 대한 유연성은 떨어진다.<ul>
<li>HTTP 헤더 설정 어려움</li>
<li>상태 코드 @ResponseStatus를 붙여야 설정 가능</li>
</ul>
</li>
</ul>
<h3 id="질문">질문</h3>
<blockquote>
<p><strong>Q.</strong> <code>@ResponseBody</code>가 붙은 HandlerMethod가 ResponseEntity를 반환한다면 ResponseEntity와 ResponseEntity의 Body가 둘 중에 어떤 것이 직렬화 될까?</p>
</blockquote>
<pre><code class="language-java">@RestController
@RequestMapping(&quot;/test&quot;)
public class SampleController {

    @GetMapping(&quot;/entity&quot;)
    @ResponseBody
    public ResponseEntity&lt;String&gt; withResponseBody() {
        return ResponseEntity.ok(new String());
    }
}</code></pre>
<p>일단 결론부터 말하자면 <strong>ResponseEntity의 Body가 직렬화</strong> 된다.</p>
<p>왜 그럴까? 그 이유를 오늘 알아보고자 한다.</p>
<h1 id="1-handlermethod">1. HandlerMethod</h1>
<hr />
<p>HandlerMethod 반환값 처리기에는 <strong>두 가지 메소드</strong>가 존재한다.</p>
<ul>
<li><code>supportsReturnType()</code> : 반환값을 처리할 수 있는지 판단</li>
<li><code>handleReturnvalue()</code> : 반환값을 실제로 처리(= 직렬화)</li>
</ul>
<h1 id="2-responsebody">2. ResponseBody</h1>
<hr />
<p>ResponseBody 반환값 처리기에 대해 알아보자</p>
<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/114c926b-c32f-463b-9afb-e536650ab4a7/image.png" /></p>
<ul>
<li><code>supportsRetrunType()</code> : ResponseBody인지 확인</li>
<li><code>handleReturnValue()</code><ul>
<li><code>mvcContainer.setRequestHandled</code>를 <code>true</code>로 변경해 요청이 handle되었음을 명시한다.</li>
<li>HandlerAdapter가 null인 mvc를 반환한다.</li>
<li>returnValue를 실제로 Http 응답 바디에 직렬화 한다. 이때, HttpMessageConverter를 사용한다.</li>
</ul>
</li>
</ul>
<h1 id="3-responseentity">3. ResponseEntity</h1>
<hr />
<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/029ad0b8-2ab3-4a94-bd3c-2e8a08baf430/image.png" /></p>
<ul>
<li><code>supportsRetrunType()</code> : HttpEntity혹은 ResponseEntity인지 확인 한다.</li>
<li><code>handleReturnBody()</code><ul>
<li><code>mvcContainer.setRequestHandled</code>를 <code>true</code>로 변경해 요청이 handle되었음을 명시한다.</li>
<li>returnValue를 직접 직렬화 하는 것이 아니라 <strong>ResponseEntity의 body를 직렬화</strong> 한다. 이때, H ttpMessageConverter을 사용한다.</li>
</ul>
</li>
</ul>
<h1 id="4-handlermethod-반환값-처리기-모음집">4. HandlerMethod 반환값 처리기 모음집</h1>
<hr />
<p>HandlerMethod 반환값 처리기란 HandlerMethod가 반환한 값을 Http Response Body에 직렬화 하는 역할을 수행한다.</p>
<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/20547574-0c11-4d9d-ac2f-72d071246841/image.png" /></p>
<ul>
<li>컴포지트 패턴으로 구성되어 있다. (* 컴포지트 패턴 : 복합객체(Composite)와 단일 객체(Leaf)를 동일한 컴포넌트로 취급해 재귀적이고, 동일한 행동을 실행할 수 있도록 하는 디자인 패턴)</li>
</ul>
<h2 id="41-supportsreturntype">4.1 SupportsReturnType</h2>
<p>자신의 HandlerMethod 반환값 처리기 List안에 returnType을 처리할 수 있는 처리기가 자 존재하는가 파악한다.</p>
<h2 id="42--handlereturnvalue">4.2  HandleReturnValue</h2>
<p>선택한 HanlderMethod 반환값 처리기에 handleReturnValue()를 호출한다.</p>
<h2 id="43-반환값-처리기-간의-서열">4.3 반환값 처리기 간의 서열</h2>
<p>HandlerMethod 반환값 처리기 List는 순차 탐색을 통해 조회된다. 그렇기에 List <strong>앞쪽에 위치하는 처리기가 먼저 호출</strong>횐다.</p>
<p>HandlerMethod 반환값 처리기 모음집 내부 List를 확인해보자</p>
<p><img alt="" src="https://velog.velcdn.com/images/limseohyeon/post/b7d484f1-f824-420c-a51e-b67943b290e5/image.png" /></p>
<p>ResponseEntity 반환값 처리기가 ResponseBody 반환값 처리기보다 앞에 존재하기 때문에</p>
<blockquote>
<p>만일   <code>@ResponseBody</code>가 붙은 HandlerMethod가 ResponseEntity를 반환한다면 ResponseEntity와 ResponseEntity의 Body가 둘 중에 어떤 것이 직렬화 될까?</p>
</blockquote>
<p>도입부에 가졌던 의문에 대한 답변이  <strong>ResponseEntity의 Body가 직렬화 된다.</strong>  가 되는 이유이다.</p>
<h1 id="5-responseentity를-반환하면서-restcontroller를-왜-쓰는가">5. ResponseEntity를 반환하면서 RestController를 왜 쓰는가?</h1>
<hr />
<h2 id="51-restcontroller-와-responseentity">5.1 RestController 와 ResponseEntity</h2>
<ul>
<li><strong>RestController</strong> : <code>@Controller</code> + <code>@ResponseBody</code> 수행</li>
<li><strong>ResponseEntity</strong> : http 응답 자체를 포장하는 객체. body 직렬화 + 응답 커밋 수행</li>
</ul>
<p>즉, ResponseEntity는 응답 객체 자체로 <strong>@ResponseBody가 필요가 없음</strong></p>
<h2 id="52-답변">5.2 답변</h2>
<ol>
<li><strong>기술적 관점</strong> : HandlerMethod 반환값의 JSON <strong>직렬화를 보장</strong>하기 위함</li>
<li><strong>명시적 관점</strong> : Restful API용도의 Controller임을 <strong>명시</strong>하기 위함</li>
</ol>