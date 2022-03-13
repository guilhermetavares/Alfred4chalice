# Email Verify

## EmailListVerifyOne

Para utilizar o EmailListVerifyOne serão necessários:

- Adicionar a variável de ambiente:

```python
ALFRED_EMAIL_VERIFY_TOKEN=meu_token
```

Para validar e-mails pode-se usar a seguinte classe abaixo que faz uso da API [Email List Verify](https://www.emaillistverify.com):

```python
from alfred.tools.email_verify import EmailListVerifyOne
EmailListVerifyOne.verify(email)
```

o método verify retorna:

- True:
    Se o email for válido ou caso estoure alguma exceção
- False:
    Se o email for inválido

Você pode também utilizar o método is_smtp_email_valid, onde além de validar se o email possui o formato ideal de email antes de enviar para a API, ele também utiliza uma régra de rate.

```python
ALFRED_EMAIL_VERIFY_RATE = 20
```

Para chamar a função

```python
from alfred.tools.email_verify import is_smtp_email_valid

is_smtp_email_valid("valid.email@maistodos.com.br")
```
