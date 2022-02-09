# Basic Auth Cached Authorizer

A validação `basic_auth_cached_authorizer` faz uso de do `alfred.cache.walrus_cache.Cache` para
adicionar uma camada de Cache na validação, reduzindo o numero de requisições no banco.
Verificar configurações do Cache na documentação específica.

Para utilizar o `basic_auth_cached_authorizer`, serão necessários no seu requirements:

```requirements
pynamodb>=5.1.0
walrus>=0.8.2
    # via
        alfred.cache.walrus_cache.Cache
```

Será necessário também o acesso a um banco de dados Dynamodb. Detalhes da configuração
do banco em: (<https://docs.aws.amazon.com/dynamodb/index.html>)

Primeiro, é necessário criar a tabela do `BasicAuthUser`, com o seguinte script:

```python
from alfred.auth.models import BasicAuthUser
from alfred.settings import DYNAMODB_PREFIX

class DynamoDBException(Exception):
    pass


def dynamodb_create_tables():
    if not DYNAMODB_PREFIX:
        raise DynamoDBException("DYNAMODB_PREFIX enviroment variable must be set")

    if not BasicAuthUser.exists():
        BasicAuthUser.create_table(
            read_capacity_units=1, write_capacity_units=1, wait=True
        )


if __name__ == "__main__":
    dynamodb_create_tables()

```

Na sequencia, será necessário registrar o `basic_auth_cached_authorizer` no seu app chalice.

```python
from alfred.auth.basic_auth_cached_authorizer as alfred_auth

@app.authorizer()
def basic_auth_cached_authorizer(auth_request):
    return alfred_auth.basic_auth_cached_authorizer(auth_request)
```

Agora basta popular o tabela de usuários e utilizar o authorizer em seus endpoints.

```python
@app.route("/ping", methods=["GET"], authorizer=basic_auth_cached_authorizer)
def login():
    pass
```
