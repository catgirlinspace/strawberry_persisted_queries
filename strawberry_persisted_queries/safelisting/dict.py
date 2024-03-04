from graphql import GraphQLError


class DictSafelist:
    def __init__(self, lookup_dict):
        self.lookup = lookup_dict

    def get_query(self, hash):
        try:
            return self.lookup[hash]
        except KeyError:
            raise GraphQLError("Hash {} not found".format(hash))
