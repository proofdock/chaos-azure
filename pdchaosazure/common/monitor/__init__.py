from azure.mgmt.monitor import MonitorClient
from chaoslib import Secrets
from chaoslib.types import Configuration
from pdchaosazure import auth, load_secrets
from pdchaosazure.common.config import load_subscription_id


def init_client(experiment_secrets: Secrets, experiment_configuration: Configuration) -> MonitorClient:
    secrets = load_secrets(experiment_secrets)
    subscription_id = load_subscription_id(experiment_configuration)

    with auth(secrets) as authentication:
        base_url = secrets.get('cloud').endpoints.resource_manager
        client = MonitorClient(credentials=authentication,
                               subscription_id=subscription_id,
                               base_url=base_url)
        return client
