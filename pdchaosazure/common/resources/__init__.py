from azure.mgmt.resourcegraph import ResourceGraphClient
from chaoslib import Secrets

from pdchaosazure import load_secrets, auth


def init_client(experiment_secrets: Secrets) -> ResourceGraphClient:
    secrets = load_secrets(experiment_secrets)

    with auth(secrets) as authentication:
        base_url = secrets.get('cloud').endpoints.resource_manager
        client = ResourceGraphClient(credentials=authentication, base_url=base_url)
        return client
