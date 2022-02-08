# Field ImageType

Para quem usa o sqlalchemy e precisa de um campo para armazenar arquivos de imagem, sugerimos o campo do ImageType.
O campo gerencia o envio e requisição da imagem para o `DEFAULT_STORAGE` definido.

Para isso, é necessário definir a variável de ambiente `DEFAULT_STORAGE`.

As opções de DEFAULT_STORAGE são:

- `s3`: para armazenar o arquivo em um bucket S3. Para isso, também serão necessárias as variáveis `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` e `BUCKET_S3`
- `dummy`: para um comportamento dummy, apenas simulando um armazenamento.

```python
from alfred.sqlalchemy_utils.fields.image import ImageType

class SeuModel:
    password = Column(ImageType(upload_to="nome_da_pasta"), nullable=True)

```
