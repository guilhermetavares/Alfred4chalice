# Walrus Cache

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
from alfred.cache.walrus_cache import Cache

value = 100
Cache.set("cache_key", value, 60)
Cache.get("cache_key")
Cache.delete("cache_key")
```
