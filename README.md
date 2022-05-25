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

## CACHE

Opções de gerenciadores de Cache para serem utilizados:

- [Walrus Cache](/docs/cache/walrus_cache.md): gerenciador baseado na lib Walrus

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
ALFRED_AWS_ACCESS_KEY_ID=id
ALFRED_AWS_SECRET_ACCESS_KEY=key

SQS_QUEUE_URL=endereço-da-sua-fila-default
```

Como utilizar

```python
@app.on_sqs_message(queue=SQS_QUEUE_URL)
def handle_sqs_message(event):
     alfred.sqs.handle_sqs_message(event, queue=SQS_QUEUE_URL)
```

Para multiplas filas

```python

from your.settings import SQS_SECOND_QUEUE_NAME, SQS_SECOND_QUEUE_URL

@app.on_sqs_message(queue=SQS_SECOND_QUEUE_NAME)
def handle_second_sqs_message(event):
     alfred.sqs.handle_sqs_message(event, queue_url=SQS_SECOND_QUEUE_URL)

# app.tasks.py
@SQSTask(bind=True, queue_url=SQS_SECOND_QUEUE_URL)
def task_very_important(self, charge_id):
     # very important script

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

## Fila Morta

Objetivo da fila morta é de fazer o reenvio das mensagens que não foram enviadas nas primeiras tentativas.

### **Anteriormente**

Utilizando o sqs, após a ultima tentativa do retry adicionamos um erro e nunca mais viamos estes casos.

### **Atualmente**

Após implementado esta função de fila morta, conseguimos salvar as mensagens em uma tabela do dynamo para ser feito o reenvio em uma data futura. Você pode querer utilizar esta feature quando o que você esta enviando é algo importante. Vou mostrar 2 opções, uma de como utilizar e a outra de como `não` utilizar a fila morta

> Exemplo de como fazer o uso da fila morta:

```python
# Só adicionar a flag dead_retry=True
@SQSTask(bind=True, queue_url=SQS_SECOND_QUEUE_URL, dead_retry=True)
def task_very_important(self, charge_id):
     ...

```

> Exemplo de quando você `não` quer utilizar a fila morta:

```python
# Por padrão a flag dead_retry=False
@SQSTask(bind=True, queue_url=SQS_SECOND_QUEUE_URL)
def task_very_important(self, charge_id):
     ...

```

Caso você queira saber mais sobre como as mensagens são salvas na tabela, vocẽ poderá acessar a classe [DeadTask](alfred/sqs/models.py)

Agora que aprendemos o objetivo da fila morta e como salvar as mensagens em uma tabela, veremos como fazer o envio delas.

Na nossa classe, temos um método para fazer o envio das mensagens salvas no banco. Sendo assim, precisamos da instancia para fazer o envio.

```python
# Importando a Classe
from alfred.sqs.models import DeadTask


# Pegando uma mensagem que foi salva no banco
dead_task = DeadTask.scan().__next__()


# Fazendo o envio da mensagem salva no banco utilizando o método run
dead_task.run()

```

## Tools

Verificação de e-mail:

- [EmailListVerifyOne](/docs/tools/email_verify.md)

## Gestão de Cache em processamento de Task com SQSTask

Objetivo do cache na classe `SQSTask` é evitar duplicidade de processamento de tasks, através de uma verificação de `cache` a classe consegue identificar se determinada task foi ou não processada. Abaixo um exemplo de aplicação:

> Exemplo de como fazer o uso do cache

```python
@SQSTask(once_time=60*60)
def foo(param_a, param_b):
    return "bar"
```

O parâmetro `once_time` é a definição do tempo de cache de uma determinada task.

> Exemplo de como `não` fazer o uso do cache

```python
@SQSTask()
def foo(param_a, param_b):
    return "bar"
```

Caso o parâmetro `once_time` não seja informado, quando chamar a task por `default` o valor será `None`. Dessa forma, não utilizando o `cache` da classe SQSTask.
