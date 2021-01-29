from azure.mgmt.monitor import MonitorManagementClient

from pdchaosazure import auth, load_secrets
from pdchaosazure.common.config import load_subscription_id


def init() -> MonitorManagementClient:
    secrets = load_secrets()
    subscription_id = load_subscription_id()
    base_url = secrets.get('cloud').endpoints.resource_manager

    with auth(secrets) as credentials:
        client = MonitorManagementClient(
            credential=credentials, subscription_id=subscription_id, base_url=base_url)

        return client
