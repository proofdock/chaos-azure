from azure.mgmt.web import WebSiteManagementClient

from pdchaosazure import auth, load_secrets, load_subscription_id


def init() -> WebSiteManagementClient:
    secrets = load_secrets()
    subscription_id = load_subscription_id()
    base_url = secrets.get('cloud').endpoints.resource_manager

    with auth(secrets) as authentication:
        client = WebSiteManagementClient(
            credential=authentication, subscription_id=subscription_id, base_url=base_url)

        return client
