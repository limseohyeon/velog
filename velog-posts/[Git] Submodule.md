<h1 id="서브모듈submodule">서브모듈(Submodule)</h1>
<hr />
<h2 id="1-서브모듈-이란">1. 서브모듈 이란?</h2>
<p>Git 프로젝트에서 다른 Git 프로젝트를 하위 디렉토리에 포함시키는 방법이다. 하나의 Repository에서 여러 개의 프로젝트를 관리할 수 있고 각각의 프로젝트는 독립적으로 존재한다.</p>
<h3 id="장점-여러-프로젝트에서-공통-모듈을-사용할-때-관리가-용이하다">장점. 여러 프로젝트에서 공통 모듈을 사용할 때 관리가 용이하다.</h3>
<p>공통 모듈을 사용하고 프로젝트 각각 적용하는 경우 공통 모듈에 수정이 발생하면 각 프로젝트들은 변경 사항을 알 수 없다. 변경사항을 개발자가 직접 수동으로 싱크를 맞춰야하는 상황이 발생한다.</p>
<p>하지만, 서브모듈을 적용하는 경우 프로젝트에서 레포를 하나 더 관리하면 된다. 서브모듈에 변경사항이 생겼다면 서브모듈의 경로로 이동해 <code>commit</code> <code>push</code>하면 된다.</p>
<p>branch를 나눠서 작업하고 <code>merge</code>하는 등 <code>git</code> 의 기능도 사용할 수 있기 때문에 <strong>개발 시 훨씬 높은 유연성을 제공</strong>한다.</p>
<hr />
<h2 id="2-서브모듈-주의사항">2. 서브모듈 주의사항</h2>
<p>서브모듈을 사용하는 프로젝트는 <code>main project</code>와 <code>sub project</code>가 부모 자식 관계를 가지고 연결되어 있다. 즉, <strong>외부에서 로컬</strong>로 데이터를 받아 갱신해야할 때(clone, pull, update 등…) 모두 <code>main → sub</code> 순서로 진행되어야 한다. </p>
<p>그러나, <strong>로컬에서 외부</strong>로 데이터를 내보낼 때(push)는 <code>sub→main</code> 의 순서로 진행되어야 한다.</p>
<aside>

<h3 id="⚠️submodule-동작-순서">⚠️<strong>Submodule 동작 순서</strong></h3>
<hr />
<p><strong>외부 → 로컬 :</strong> <code>main</code> → <code>sub</code></p>
<p><strong>로컬 → 외부 :</strong> <code>sub</code> → <code>main</code></p>
</aside>

<hr />
<h1 id="서브-모듈-명령어">서브 모듈 명령어</h1>
<hr />
<h2 id="clone--원격-저장소에서-서브-모듈-처음-받아오기">Clone : 원격 저장소에서 서브 모듈 처음 받아오기</h2>
<h3 id="방법1"><strong>방법1</strong></h3>
<pre><code class="language-bash"># main root
git clone [main프로젝트 주소]
git submodule init
git submodule update
git submodule foreach git checkout main</code></pre>
<ul>
<li><code>git clone [main 프로젝트 주소]</code> : main에 들어가면 .gitmodules 파일이 생성된다. 이 파일에는 main에 위치할 sub의 폴더명과 git repo 주소가 적혀있다.</li>
<li><code>submodule init</code> : .gitmodule에 있는 정보를 .git/config에 등록한다.</li>
<li><code>submodule update</code> : sub의 원격 저장소에서 데이터를 가져오고 sub에 대한 checkout을 한다.</li>
<li><code>submodule foreach</code> <code>git checkout main</code> : sub를 main로 checkout 한다.
(submodule update를 하면 sub는 detached HEAD 상태로 어떤 branch에도 속하지 않기 때문이다.)</li>
</ul>
<h3 id="방법2"><strong>방법2</strong></h3>
<pre><code class="language-bash"># main root
git clone [main프로젝트 주소]
git submodule update --init
git submodule foreach git checkout main</code></pre>
<ul>
<li>init과 update를 한 번에 수행하는 방법</li>
</ul>
<h3 id="방법3"><strong>방법3</strong></h3>
<pre><code class="language-bash"> git clone --recurse-submodules https://github.com/prgrms-web-devcourse-final-project/WEB2_3_SIGNAL-BUDDY_BE.git</code></pre>
<ul>
<li>위 모든 과정을 통합한 방법</li>
</ul>
<hr />
<h2 id="pull--원격-저장소에서-변경사항-가져오기">pull : 원격 저장소에서 변경사항 가져오기</h2>
<pre><code class="language-bash"># main root
git pull
git submodule update --remote --merge</code></pre>
<p><strong>*특정 sub만 update 하기</strong></p>
<pre><code class="language-bash"> git submodule update --remote &lt;REMOTE-REPO-NAME&gt; --merge</code></pre>
<h2 id="commit--push--원격-저장소에-변경사항-보내기">Commit &amp; Push : 원격 저장소에 변경사항 보내기</h2>
<h3 id="주의사항">주의사항</h3>
<ul>
<li>main을 commit 할 때, sub의 변경사항이 있는 경우 <strong>main과 sub 각각 두 번의 commit</strong>을 해야 한다. 이 때 순서는 반드시 <code>sub → main</code> 이 되어야 한다. 
(main을 먼저 commit 하면 main은 새로운 sub를 참조하지 않게 된다.)</li>
<li>sub를 update를 하는 경우 <code>Detached HEAD</code> 상태인지 확인해야 한다. 해당 상태인 경우에는 checkout main 등을 수행해 원하는 branch로 <code>checkout</code>한 다음에 코드를 수정해야 한다.</li>
</ul>
<h3 id="서브-모듈만-commit--push-하기">서브 모듈만 commit &amp; push 하기</h3>
<pre><code class="language-bash"># submodule root
git add .
git commit -m &quot;메시지&quot;
git push</code></pre>
<pre><code class="language-bash"># main root
git add submodule
git commit -m &quot;메시지&quot;
git push</code></pre>
<ul>
<li>일반적인 commit 방법과 동일하다.</li>
<li>sub를 push가 수정되면 main 입장에서 sub의 commit이 변경된 것이다. 그렇기 때문에 <strong>main은 sub의 변경사항을 commit 해야한다.</strong></li>
</ul>
<h3 id="main--sub-commit--push-하기">main + sub commit &amp; push 하기</h3>
<p>만일 sub를 push 하지 않은 경우 main은 sub의 변경 사항을 추적하지 않기 때문에 conflict를 발생할 수 도 있다. 아래는 이를 방지하기 위한 명령어다.</p>
<pre><code class="language-bash"># main root
git push --recurse-submodules=check</code></pre>
<ul>
<li>submodule이 모두 push된 상태인지 확인 후 올바른 상태이면 main push</li>
</ul>
<pre><code class="language-bash"># main root
git push --recurse-submodules=on-demand</code></pre>
<ul>
<li>sub를 push하고 성공하면 main push</li>
</ul>
<pre><code class="language-bash"># git push --recurse-submodules=check
git config push.recurseSubmodules check
# git push --recurse-submodules=on-demand
git config push.recurseSubmodules on-demand</code></pre>
<ul>
<li>위 명령어를 항상 수행하도록 설정을 변경할 수 있다.</li>
</ul>
<h1 id="참고-블로그">참고 블로그</h1>
<hr />
<p><a href="https://velog.io/@2ast/%EB%8B%A4%EC%A7%90-%EB%94%94%EC%9E%90%EC%9D%B8-%EC%8B%9C%EC%8A%A4%ED%85%9C-Github-%EC%84%9C%EB%B8%8C%EB%AA%A8%EB%93%88-%EA%B4%80%EB%A6%AC-%ED%9A%8C%EA%B3%A0">다짐) 디자인 시스템 Git Submodule 관리 회고</a></p>
<p><a href="https://pinedance.github.io/blog/2019/05/28/Git-Submodule">Git submodule 사용하기</a></p>