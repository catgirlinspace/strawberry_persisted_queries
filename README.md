# 🍓Strawberry Persisted Queries

[![PyPI](https://img.shields.io/pypi/v/strawberry_persisted_queries?logo=pypi&logoColor=white&style=for-the-badge)](https://pypi.org/project/strawberry_persisted_queries/)

Apollo-compatible persisted queries for Strawberry. 

## Usage

Add `PersistedQueriesExtension` to your extensions.

```python
import strawberry
from strawberry_persisted_queries import PersistedQueriesExtension

schema = strawberry.Schema(
    query=Query,
    extensions=[
        PersistedQueriesExtension(),
    ],
)
```

### Django

For Django, a Django cache backend is available.
```python
from strawberry_persisted_queries.django_cache import DjangoPersistedQueryCache

PersistedQueriesExtension(cache_backend=DjangoPersistedQueryCache())
```

### Safelisted Queries

`DictSafelist` can be used to require persisted queries to already be saved.
This can be used with a build tool to ensure only queries used within an app are available.

```python
from strawberry_persisted_queries.safelisting import DictSafelist

PersistedQueriesExtension(safelist=DictSafelist({
    'sha256Hash': 'query {...}',
}))
```

## Custom Cache Backends

Custom cache backends allow using another cache for persisted queries, such as memcached or a database.
Custom cache backends can inherit from `strawberry_persisted_queries.PersistedQueryCache`. 

```python
from strawberry_persisted_queries.cache import PersistedQueryCache

class MyCache(PersistedQueryCache):
    def get(self, query_hash):
        return cache.get(query_hash)

    def set(self, query_hash, value):
        cache.set(query_hash, value)

PersistedQueriesExtension(cache_backend=MyCache())
```