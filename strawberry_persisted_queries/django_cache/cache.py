from django.core.cache import cache

from strawberry_persisted_queries.cache import PersistedQueryCache


class DjangoPersistedQueryCache(PersistedQueryCache):
    timeout = None  # never expire

    def get(self, query_hash):
        return cache.get(query_hash)

    def set(self, query_hash, value):
        cache.set(query_hash, value, self.timeout)
