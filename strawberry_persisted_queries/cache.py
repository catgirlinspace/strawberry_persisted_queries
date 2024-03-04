class PersistedQueryCache:
    cache: dict[str, str] = {}

    def get(self, query_hash):
        return self.cache.get(query_hash, None)

    def set(self, query_hash, value):
        self.cache[query_hash] = value
