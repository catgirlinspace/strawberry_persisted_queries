from django.core.cache import cache as default_cache, BaseCache

from strawberry_persisted_queries.cache import PersistedQueryCache


class DjangoPersistedQueryCache(PersistedQueryCache):
    timeout = None  # never expire
    cache: BaseCache = None

    def initialize(self, timeout: int | None = None, cache: BaseCache = default_cache) -> None:
        self.timeout = timeout
        self.cache = cache

    def get(self, query_hash):
        return self.cache.get(query_hash)

    def set(self, query_hash, value):
        self.cache.set(query_hash, value, self.timeout)
