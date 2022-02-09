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

## SQLALCHEMY_UTILS

Opções de campos personalizados para serem utilizados na definição de um Model do SqlAlchemy

- [ImageType](/docs/sqlalchemy_utils/ImageType.md): para armazenar arquivos de imagem
- [PasswordSaltType](/docs/sqlalchemy_utils/PasswordSaltType.md): para armazenar password com salt randômico
- [PasswordType](/docs/sqlalchemy_utils/PasswordType.md): para armazenar password com salt fixo

## AUTH

Opções de authorizers para serem utilizados na definição de uma nova api

- [basic_auth_authorizer](/docs/auth/basic_auth_authorizer.md): para validação do tipo Basic Auth sem cache
- [basic_auth_cached_authorizer](/docs/auth/basic_auth_cached_authorizer.md): para validação do tipo Basic Auth com cache
- [jwt_authorizer](/docs/auth/jwt_authorizer.md): para validação do tipo token JWT

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

## Feature Flag

Para utilizar o `Feature Flag`, você deve instanciar a classe FeatureFlag passando como parâmetro o `id` e `data`.

```python
from alfred.feature_flag.models import FeatureFlag

FeatureFlag(id=1, data={"foo": "bar"}).save()
```

Como acessar as informações:

- Passando o `id` no método `get_data`, você acessa os dados contido no campo `data`:

```python
flag = FeatureFlag.get_data(id=1)
```

Resposta:

```python
print(flag)

# >>> {"foo": "bar"}
```

- Caso o parâmetro `id` seja **Nulo** ou **id que não existe** o método irá retornar **None**.
