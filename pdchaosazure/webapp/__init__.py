from azure.mgmt.web import WebSiteManagementClient
from chaoslib import Secrets, Configuration

from pdchaosazure import auth, load_secrets, load_subscription_id


def init_client(experiment_secrets: Secrets, experiment_configuration: Configuration) -> WebSiteManagementClient:

    secrets = load_secrets(experiment_secrets)
    configuration = load_subscription_id(experiment_configuration)

    with auth(secrets) as authentication:
        base_url = secrets.get('cloud').endpoints.resource_manager
        client = WebSiteManagementClient(
            credentials=authentication, subscription_id=configuration.get('subscription_id'), base_url=base_url)

        return client
