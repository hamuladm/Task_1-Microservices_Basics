import hazelcast
import yaml


def create_client(cluster_members: list[str] | str):
    client = hazelcast.HazelcastClient(
        cluster_name="dev", cluster_members=[cluster_members]
    )
    return client


def read_yaml(file_path):
    with open(file_path, "r") as file:
        return yaml.safe_load(file)
