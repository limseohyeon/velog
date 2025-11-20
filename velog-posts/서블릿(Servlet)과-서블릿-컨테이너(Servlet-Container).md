<!-- ENTRY_ID: https://velog.io/@limseohyeon/%EC%84%9C%EB%B8%94%EB%A6%BFServlet%EA%B3%BC-%EC%84%9C%EB%B8%94%EB%A6%BF-%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88Servlet-Container -->
<!-- SOURCE_TITLE: 서블릿(Servlet)과 서블릿 컨테이너(Servlet Container) -->

<h1 id="1-서블릿이란">1. 서블릿이란?</h1>
<hr />
<p>서블릿이란 웹 서버 내에서 실행되는 자바 프로그램으로 클라이언트의 요청을(request) 처리하고, 그 결과를 반환(response)한다.</p>
<p>서블릿이 없으면 직접 HTTP 통신으로 오고가는 문자열을 파싱해 통신해야하기 때문에 비즈니스 로직에 집중하고 편의성을 올리기 위해 사용한다.</p>
<h1 id="2-서블릿-컨테이너">2. 서블릿 컨테이너</h1>
<p>서블릿 컨테이너란 서블릿의 생성, 실행, 파괴를 관리한다. 즉, 서블릿 메서드를 관리하고 실행하는 주체다.</p>
<p>HttpServletRequest, HttpServletResponse 두 객체를 생성하며 GET, POST 여부에 따라 동적인 페이지를 생성해 응답을 보낸다.</p>
<p>대표적인 예로 톰캣(Tomcat)이 있다. (톰캣 = 웹서버 + 서블릿 컨테이너)</p>
<h2 id="21-서블릿-컨테이너-역할"><strong>2.1 서블릿 컨테이너 역할</strong></h2>
<ul>
<li>웹서버와의 통신 지원</li>
<li>서블릿 생명주기 관리</li>
<li>멀티쓰레드 지원 및 관리</li>
<li>선언적인 보안 관리</li>
</ul>
<h2 id="22-서블릿-생명주기-메서드"><strong>2.2 서블릿 생명주기 메서드</strong></h2>
<ul>
<li><code>init</code> : <strong>서블릿 초기화</strong><ul>
<li>서블릿 인스턴스 생성시 처음 호출</li>
<li>DB 커넥션, 초기 자원 로드 등 수행</li>
</ul>
</li>
<li><code>service</code> :  <strong>HTTP 요청 처리 메서드</strong><ul>
<li>클라이언트 요청이 들어올 때 마다 호출</li>
<li>요청에 따라 내부에서 GET/POST에 따라 doGet(), doPost() 호출</li>
</ul>
</li>
<li><code>destroy</code> : <strong>서블릿이 메모리에서 내려갈 때 호출</strong><ul>
<li>서버 종료, DB 커넥션 닫기 같은 쓰레드 종료</li>
</ul>
</li>
</ul>
<h2 id="23-서블릿-컨테이너-요청-처리-흐름">2.3 서블릿 컨테이너 요청 처리 흐름</h2>
<p><img alt="" src="https://velog.velcdn.com/images/kjo6391/post/485b5c74-6169-4717-a136-ffd769fd1822/image.png" /></p>
<ol>
<li><p><strong>브라우저 → 톰캣(coyote)에 http 요청</strong></p>
<p> 이때 요청을 읽고 Requeest 객체 형태로 파싱한다.</p>
</li>
<li><p><strong>Coyote → Catalina</strong></p>
<p> 카타리나는 요청을 어떤 서블릿이 처리할지 결정</p>
</li>
<li><p><strong>Reuest 매핑</strong></p>
<p> 카타리나는 내부 매핑 테이블에서 다음 순서로 서블릿을 찾음</p>
<ul>
<li>정확한 URL 매칭 : <code>/admin/login</code></li>
<li>와일드카드 매칭 : <code>/admin/*</code></li>
<li>확장자 매칭 : <code>.jsp</code></li>
</ul>
</li>
<li><p><strong>서블릿 인스턴스 준비</strong></p>
<ol>
<li>이미 있는 경우 → 바로 service 호출</li>
<li>없는 경우 → 생성 → init → service</li>
</ol>
</li>
</ol>
<h2 id="24-requestresponse-객체-내부-처리-흐름">2.4 Request/Response 객체 내부 처리 흐름</h2>
<ol>
<li>Coyote가 HTTP 요청을 받아 Request 객체 생성된다. (이거를 가지고 카탈리나가 서블릿을 찾는것)</li>
<li>Catalina는 이 객체를 내부적으로 HttpServletRequest 형태로 래핑해 서블릿에게 전달한다. (객체가 사용할 수 있도록)</li>
<li>Response도 비어 있는 객체가 전달되고, 서블릿이 내용 채운다.</li>
<li>service → flushBuffer()가 호출되면<ol>
<li>Catalina 내부 OutputBuffer flush</li>
<li>Coyote가 실질적인 HTTP 응답 전송</li>
<li>브라우저에 전달</li>
</ol>
</li>
</ol>
<h2 id="25--default-servlet-jsp-servlet">2.5 . Default Servlet, JSP Servlet</h2>
<p>모든 요청은 일단 기본 서블릿(Dispatcher)으로 들어가고, 여기서:</p>
<ul>
<li><code>/static/*</code> → DefaultServlet</li>
<li><code>.jsp</code> → JspServlet</li>
<li>그 외 → 내가 만든 서블릿</li>
</ul>