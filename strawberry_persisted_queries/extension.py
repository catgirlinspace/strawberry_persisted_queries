import json
from hashlib import sha256

import strawberry
from graphql import GraphQLError, ExecutionResult as GraphQLExecutionResult
from strawberry.extensions import SchemaExtension
from strawberry.types import ExecutionContext
from strawberry.utils.await_maybe import AsyncIteratorOrIterator

from strawberry_persisted_queries.cache import PersistedQueryCache


class PersistedQueriesExtension(SchemaExtension):
    def __init__(self, cache_backend: PersistedQueryCache = PersistedQueryCache(), *, execution_context: ExecutionContext):
        super().__init__(execution_context=execution_context)
        self.cache_backend = cache_backend

    def on_operation(self) -> AsyncIteratorOrIterator[None]:
        execution_context = self.execution_context
        body = json.loads(execution_context.context.request.body)
        extensions = body.get("extensions")
        if extensions:
            persisted_query_extension = extensions.get("persistedQuery")
            if persisted_query_extension:
                version = persisted_query_extension.get("version")
                if version != 1:
                    raise GraphQLError("PersistedQueryNotSupported")
                query_hash = persisted_query_extension.get("sha256Hash")
                query = self.cache_backend.get(query_hash)
                if query_hash and query:
                    execution_context.query = query
                elif query_hash and not query:
                    raise GraphQLError("PersistedQueryNotFound")
                elif query_hash and execution_context.query:
                    query_hash2 = sha256(query_hash.encode()).hexdigest()
                    if query_hash == query_hash2:
                        self.cache_backend.set(query_hash, execution_context.query)
        yield
