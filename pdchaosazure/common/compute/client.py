from azure.mgmt.compute import ComputeManagementClient

from pdchaosazure import load_secrets, load_subscription_id, auth


def init() -> ComputeManagementClient:
    secrets = load_secrets()
    subscription_id = load_subscription_id()
    base_url = secrets.get('cloud').endpoints.resource_manager

    with auth(secrets) as credentials:
        client = ComputeManagementClient(
            credential=credentials, subscription_id=subscription_id, base_url=base_url)

        return client
