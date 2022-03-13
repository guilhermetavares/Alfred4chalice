# Email Verify 

## EmailListVerifyOne

Para utilizar o EmailListVerifyOne serão necessários:
- Adicionar a variável de ambiente:
```
ALFRED_EMAIL_VERIFY_TOKEN=meu_token
```

Para validar e-mails pode-se usar a seguinte classe abaixo que faz uso da API [Email List Verify](https://www.emaillistverify.com):

```python
client = EmailListVerifyOne()
client.verify(email)
```
o método verify retorna:
- True:
    Se o email for válido ou caso estoure alguma exceção 
- False:
    Se o email for inválido

