# Field para Password

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
