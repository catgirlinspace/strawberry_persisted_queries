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
        PersistedQueriesExtension,
    ],
)
```