from azure.mgmt.compute import ComputeManagementClient
from chaoslib import Secrets, Configuration

from pdchaosazure import load_secrets, load_subscription_id, auth


def init(experiment_secrets: Secrets, experiment_configuration: Configuration) -> ComputeManagementClient:
    secrets = load_secrets(experiment_secrets)
    subscription_id = load_subscription_id(experiment_configuration)

    with auth(secrets) as credentials:
        base_url = secrets.get('cloud').endpoints.resource_manager
        client = ComputeManagementClient(
            credential=credentials, subscription_id=subscription_id, base_url=base_url)

        return client
