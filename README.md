# 🍓Strawberry Persisted Queries

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

For Django, a Django cache backend is available.
```python
from strawberry_persisted_queries.django_cache import DjangoPersistedQueryCache

PersistedQueriesExtension(cache_backend=DjangoPersistedQueryCache())
```