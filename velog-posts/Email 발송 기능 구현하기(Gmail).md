<h1 id="문제">문제</h1>
<hr />
<p>매일 자정 배송이 완료된 주문건에 대해 사용자에게 <strong>email을 통해 안내</strong>한다.</p>
<p>이를 위해서 Spring Boot에서 email을 발송하는 기능을 구현해야 했다.</p>
<h1 id="1-구글-계정-설정">1. 구글 계정 설정</h1>
<hr />
<p>Gmail의 STMP 서버를 활용하기 위한 절차가 필요하다. 해당 과정은 아래 링크를 참고해 진행했다.</p>
<p><a href="https://velog.io/@tjddus0302/Spring-Boot-%EB%A9%94%EC%9D%BC-%EB%B0%9C%EC%86%A1-%EA%B8%B0%EB%8A%A5-%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0-Gmail">Spring Boot | 메일 발송 기능 구현하기 (Gmail)</a></p>
<h1 id="2-gradle--yml-변경">2. gradle &amp; yml 변경</h1>
<hr />
<p><strong>&lt;build.gradle&gt;</strong></p>
<pre><code class="language-java">dependencies {
...
implementation 'org.springframework.boot:spring-boot-starter-mail'
...
}</code></pre>
<p><strong>&lt;application.yml&gt;</strong></p>
<pre><code class="language-java">spring:
  mail:
    host: smtp.gmail.com # SMTP 서버 호스트
    port: 587 # SMTP 서버 포트
    username: ${mail.username} # SMTP 서버 로그인 아이디
    password: ${mail.password} # SMTP 서버 로그인 비밀번호
    properties:
      mail:
        smtp:
          auth: true # 사용자 인증 시도 여부 (기본값 : false)
          timeout: 5000 # Socket Read Timeout 시간 (기본값: 무한)
          starttls:
            enable: true # StartTLS 활성화 여부 (기본값 : false)</code></pre>
<h1 id="3-config">3. Config</h1>
<pre><code class="language-java">@Getter
@Setter
@Builder
public class EmailMessage {
    private String to;  //수신자
    private String subject; //메일 제목
    private String massage; //메일 내용
}</code></pre>
<h1 id="4-service">4. Service</h1>
<pre><code class="language-java">@Slf4j
@RequiredArgsConstructor
@Service

public class EmailService {
    private final JavaMailSender javaMailSender;
    private final SpringTemplateEngine templateEngine;

    public void sendMail(EmailMessage emailMessage) {
        MimeMessage mimeMessage = javaMailSender.createMimeMessage();
        try{
            MimeMessageHelper mimeMessageHelper = new MimeMessageHelper(mimeMessage, false, &quot;UTF-8&quot;);
            mimeMessageHelper.setTo(emailMessage.getTo());
            mimeMessageHelper.setSubject(emailMessage.getSubject());
            mimeMessageHelper.setText(emailMessage.getMassage(), true);
            javaMailSender.send(mimeMessage);
        } catch (MessagingException e) {
            throw new RuntimeException(e);
        }
    }
}</code></pre>
<h1 id="5-controller">5. Controller</h1>
<pre><code class="language-java">@Slf4j
@RequiredArgsConstructor
@RestController
@RequestMapping(&quot;/api&quot;)
public class EmailController {

    private final EmailService emailService;

    @PostMapping(&quot;/mail&quot;)
    public ResponseEntity EmailController() {
        EmailMessage emailMessage = EmailMessage.builder()
            .to(&quot;l_mon_ster@naver.com&quot;)
            .subject(&quot;테스트 메일 제목&quot;)
            .massage(&quot;테스트 메일 본문&quot;)
            .build();
        emailService.sendMail(emailMessage);
        return new ResponseEntity(HttpStatus.OK);
    }
}</code></pre>