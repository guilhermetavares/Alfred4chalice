# JWT Authorizer

Para utilizar o `jwt_authorizer`, serão necessários:

- Adicionar no seu requirements:

```requirements
pyjwt==2.3.0
cryptography==36.0.0
```

- Adicionar as variáveis de ambiente:

```env
JWT_ALGORITHM
JWT_EXP_DELTA_SECONDS
JWT_SECRET
FERNET_CRYPT_KEY
```

Na sequencia, será necessário registrar o `jwt_authorizer` no seu app chalice.

O argumento `encrypted_fields` aponta quais fields serão criptografados dentro do token

```python
from alfred.auth.jwt_authorizer as alfred_auth

@app.authorizer()
def jwt_authorizer(auth_request):
    encrypted_fields = ["foo", "bar"]
    return alfred_auth.jwt_authorizer(auth_request, encrypted_fields)
```

Para utilizar o authorizer em seus endpoints:

```python
@app.route("/ping", methods=["GET"], authorizer=jwt_authorizer)
def login():
    pass
```

Para criar um token, utilize a função `encode_auth`:

```python
from alfred.auth.utils import encode_auth

token = encode_auth(id, token, date)
```
