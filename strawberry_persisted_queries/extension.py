import json
from hashlib import sha256

import strawberry
from graphql import GraphQLError, ExecutionResult as GraphQLExecutionResult
from strawberry.extensions import SchemaExtension
from strawberry.types import ExecutionContext
from strawberry.utils.await_maybe import AsyncIteratorOrIterator

from strawberry_persisted_queries.cache import PersistedQueryCache

debug = False


def debug_print(*args, **kwargs):
    if debug:
        print(*args, **kwargs)


class PersistedQueriesExtension(SchemaExtension):
    def __init__(self, cache_backend: PersistedQueryCache = PersistedQueryCache(), *,
                 execution_context: ExecutionContext):
        super().__init__(execution_context=execution_context)
        self.cache_backend = cache_backend

    def on_operation(self) -> AsyncIteratorOrIterator[None]:
        debug_print("cache status")
        debug_print(self.cache_backend.cache)
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
                debug_print(query_hash, query)
                if query_hash and query:
                    debug_print("have query hash and found a query")
                    execution_context.query = query
                elif query_hash and execution_context.query:
                    debug_print("have query hash and request query...")
                    debug_print(execution_context.query)
                    query_hash2 = sha256(execution_context.query.encode()).hexdigest()
                    debug_print(query_hash, query_hash2, query_hash == query_hash2)
                    if query_hash == query_hash2:
                        self.cache_backend.set(query_hash, execution_context.query)
                    else:
                        raise GraphQLError(
                            "provided hash does not match query")  # Apollo server actually uses `sha` instead of `hash`
                elif query_hash and not query:
                    debug_print("no have a query, but hash provided")
                    raise GraphQLError("PersistedQueryNotFound")
        yield
