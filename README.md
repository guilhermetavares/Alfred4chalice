# Alfred para Chalice

![Alfred](https://upload.wikimedia.org/wikipedia/commons/8/80/Alfred_Thaddeus_Crane_Pennyworth.jpg)

Alfred Thaddeus Crane Pennyworth é um personagem fictício da DC Comics. Ele é mordomo e tutor do bilionário Bruce Wayne.

Alfred tem sua origem muitas vezes envolta em mistério e pouco se fala de suas atividades antes de ele se tornar mordomo da rica e tradicional família Wayne. Em algumas mini-series e edições avulsas das HQs fala-se de sua distante ligação com a Scotland Yard onde ele teria trabalhado como um de seus agentes mais discretos.

Sabe-se ainda de um passado como ator competente, tendo essa experiência na dramaturgia se provado útil em diversas ocasiões. Como, por exemplo, tendo ensinado ao Bruce, ainda jovem, como modificar sua voz para imitar as vozes de outras pessoas. Algo que se provou muito útil na criação da persona do Homem-Morcego.

Demonstra também muitas outras habilidades úteis, como conhecimentos médicos básicos, por exemplo. Contudo, fica-se com a impressão que nem Bruce Wayne conhece totalmente esse passado de seu mordomo. Muitas vezes, as palavras de Alfred são sugestões quase que subliminares que ajudam o "cruzado mascarado" na solução de enigmas complexos de crimes. Mesmo assim, Alfred, várias vezes, faz o papel de ingênuo.

## Rodando o projeto local

Primeiramente você deve instanciar o docker com o comando

```bash
make build
```

Após o build, é só rodar os testes

```bash
make test
```

## Setup para o Cache

Para utilizar a classe de cache do Alfred, primeiramente deve adicionar o walrus (<https://walrus.readthedocs.io/en/latest/api.html>) no seu requirements, recomendamos versões maiores que a **0.8.2**

```requirements
walrus==X.X.X
```

Após adicionar o walrus no projeto, você deve adicionar a sua conexação com o redis nas variáveis de ambiente do projeto.

```python
ALFRED_REDIS_HOST=sua-conexao-com-redis
```

Como utilizar

```python
from alfred.cache import Cache

value = 100
Cache.set("cache_key", value, 60)
Cache.get("cache_key")
Cache.delete("cache_key")
```

## Field para Password

Para quem usa o sqlalchemy e precisar de um campo de password, pode utilizar o campo do alfred, que já faz as validações de senha.

Primeiro deve definir a sua chave de criptografia

```python
ALFRED_PASSWORD_SALT = very-numric-key
```

```python
from alfred.sqlalchemy_utils.fields.password import PasswordType

class SeuModel:
    password = Column(PasswordType, nullable=True)

```

## Field para PasswordSalt

Para quem usa o sqlalchemy e precisar de um campo de password, pode utilizar o campo do PasswordSalt.
O campo criptografa a senha baseado em um salt randômico que também é persistido no banco.
O formato final do valor persistido contem: "password_salt-password_interations-password_hash", separados por um hifen "-".

```python
from alfred.sqlalchemy_utils.fields.password import PasswordSaltType

class SeuModel:
    password = Column(PasswordSaltType, nullable=True)

```

## Basic Auth Authorizer

Para utilizar o `basic_auth_authorizer`, serão necessários no seu requirements:

```requirements
pynamodb>=5.1.0
```

Será necessário também o acesso a um banco de dados Dynamodb. Detalhes da configuração
do banco em: (<https://docs.aws.amazon.com/dynamodb/index.html>)

Primeiro, é necessário criar a tabela do `BasicAuthUser`, com o seguinte script:

```python
from alfred.auth.models import BasicAuthUser
from alfred.settings import DYNAMO_PREFIX

class DynamoDBException(Exception):
    pass


def dynamodb_create_tables():
    if not DYNAMO_PREFIX:
        raise DynamoDBException("DYNAMO_PREFIX enviroment variable must be set")

    if not BasicAuthUser.exists():
        BasicAuthUser.create_table(
            read_capacity_units=1, write_capacity_units=1, wait=True
        )


if __name__ == "__main__":
    dynamodb_create_tables()

```

Na sequencia, será necessário registrar o `basic_auth_authorizer` no seu app chalice.

```python
from alfred import auth

@app.authorizer()
def basic_auth_authorizer(auth_request):
    return auth.basic_auth_authorizer(auth_request)
```

Agora basta popular o tabela de usuários e utilizar o authorizer em seus endpoints.

```python
@app.route("/ping", methods=["GET"], authorizer=basic_auth_authorizer)
def login():
    pass
```

## JWT Authorizer

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

```python
from alfred import auth

@app.authorizer()
def jwt_authorizer(auth_request):
    return auth.jwt_authorizer(auth_request)
```

Para utilizar o authorizer em seus endpoints:

```python
@app.route("/ping", methods=["GET"], authorizer=basic_auth_authorizer)
def login():
    pass
```

Para criar um token, utilize a função `encode_auth`:

```python
from alfred.auth import encode_auth

token = encode_auth(id, token, date)
```

## SQS

Para utilizar o `sqs`, primeiro você deve adicionar o endereço de sua fila default na AWS as variáveis de ambiente do projeto:

```python
SQS_QUEUE_URL=endereço-da-sua-fila-default
```

Como utilizar

```python
@app.on_sqs_message(queue=SQS_QUEUE_URL)
def handle_sqs_message(event):
     alfred.sqs.handle_sqs_message(event)
```
