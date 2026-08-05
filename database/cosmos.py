import os
from azure.cosmos import CosmosClient, PartitionKey
from dotenv import load_dotenv

load_dotenv()

COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_KEY      = os.getenv("COSMOS_KEY")
DATABASE_NAME   = os.getenv("COSMOS_DATABASE", "lumibeauty")

_client     = None
_database   = None
_containers = {}


def get_client() -> CosmosClient:
    global _client
    if _client is None:
        _client = CosmosClient(COSMOS_ENDPOINT, credential=COSMOS_KEY)
    return _client


def get_database():
    global _database
    if _database is None:
        _database = get_client().create_database_if_not_exists(id=DATABASE_NAME)
    return _database


def get_container(name: str, partition_key: str = "/id"):
    """Lấy (hoặc tạo mới) container Cosmos DB."""
    if name not in _containers:
        _containers[name] = get_database().create_container_if_not_exists(
            id=name,
            partition_key=PartitionKey(path=partition_key),
        )
    return _containers[name]
