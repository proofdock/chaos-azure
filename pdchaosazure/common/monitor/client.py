from azure.mgmt.monitor import MonitorManagementClient
from chaoslib import Secrets
from chaoslib.types import Configuration

from pdchaosazure import auth, load_secrets
from pdchaosazure.common.config import load_subscription_id


def init(experiment_secrets: Secrets, experiment_configuration: Configuration) -> MonitorManagementClient:
    secrets = load_secrets(experiment_secrets)
    subscription_id = load_subscription_id(experiment_configuration)

    with auth(secrets) as credentials:
        base_url = secrets.get('cloud').endpoints.resource_manager
        client = MonitorManagementClient(
            credential=credentials, subscription_id=subscription_id, base_url=base_url)
        return client
