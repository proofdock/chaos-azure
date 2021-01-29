from azure.mgmt.web import WebSiteManagementClient
from chaoslib import Configuration

from pdchaosazure import auth, load_secrets, load_subscription_id


def init(experiment_configuration: Configuration) -> WebSiteManagementClient:

    secrets = load_secrets()
    subscription_id = load_subscription_id(experiment_configuration)

    with auth(secrets) as authentication:
        base_url = secrets.get('cloud').endpoints.resource_manager
        client = WebSiteManagementClient(
            credential=authentication, subscription_id=subscription_id, base_url=base_url)

        return client
