from unittest.mock import patch, MagicMock

from pdchaosazure.webapp.actions import stop, restart, delete
from tests.data import config_provider, secrets_provider, webapp_provider


@patch('pdchaosazure.webapp.actions.fetch_webapps', autospec=True)
@patch('pdchaosazure.webapp.actions.client.init', autospec=True)
def test_happily_stop_webapp(init, fetch):
    config = config_provider.provide_default_config()
    secrets = secrets_provider.provide_secrets_public()
    webapp = webapp_provider.default()

    client = MagicMock()
    init.return_value = client
    resource_list = [webapp]
    fetch.return_value = resource_list

    f = "where resourceGroup=~'rg'"
    stop(f, config, secrets)

    fetch.assert_called_with(f, config, secrets)
    client.web_apps.stop.assert_called_with(webapp['resourceGroup'], webapp['name'])


@patch('pdchaosazure.webapp.actions.fetch_webapps', autospec=True)
@patch('pdchaosazure.webapp.actions.client.init', autospec=True)
def test_happily_restart_webapp(init, fetch):
    config = config_provider.provide_default_config()
    secrets = secrets_provider.provide_secrets_public()
    webapp = webapp_provider.default()

    client = MagicMock()
    init.return_value = client
    resource_list = [webapp]
    fetch.return_value = resource_list

    f = "where resourceGroup=~'rg'"
    restart(f, config, secrets)

    fetch.assert_called_with(f, config, secrets)
    client.web_apps.restart.assert_called_with(webapp['resourceGroup'], webapp['name'])


@patch('pdchaosazure.webapp.actions.fetch_webapps', autospec=True)
@patch('pdchaosazure.webapp.actions.client.init', autospec=True)
def test_happily_delete_webapp(init, fetch):
    webapp = webapp_provider.default()
    config = config_provider.provide_default_config()
    secrets = secrets_provider.provide_secrets_public()

    client = MagicMock()
    init.return_value = client
    resource_list = [webapp]
    fetch.return_value = resource_list

    f = "where resourceGroup=~'rg'"
    delete(f, config, secrets)

    fetch.assert_called_with(f, config, secrets)
    client.web_apps.delete.assert_called_with(webapp['resourceGroup'], webapp['name'])
