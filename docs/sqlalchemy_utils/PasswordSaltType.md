# Field para PasswordSalt

Para quem usa o sqlalchemy e precisar de um campo de password, pode utilizar o campo do PasswordSalt.
O campo criptografa a senha baseado em um salt randômico que também é persistido no banco.
O formato final do valor persistido contem: "password_salt-password_interations-password_hash", separados por um hifen "-".

```python
from alfred.sqlalchemy_utils.fields.password import PasswordSaltType

class SeuModel:
    password = Column(PasswordSaltType, nullable=True)

```
