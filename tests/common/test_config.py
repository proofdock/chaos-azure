import os

from pdchaosazure.common import config

settings_dir = os.path.join(os.path.dirname(__file__), "fixtures")


def test_load_secrets_from_credential_file(monkeypatch):
    # arrange
    monkeypatch.setenv("AZURE_AUTH_LOCATION", os.path.join(settings_dir, 'credentials.json'))

    # act
    secrets = config.load_secrets()

    # assert
    assert secrets.get('client_id') == "AZURE_CLIENT_ID"
    assert secrets.get('client_secret') == "AZURE_CLIENT_SECRET"
    assert secrets.get('tenant_id') == "AZURE_TENANT_ID"
    assert secrets.get('cloud').endpoints.resource_manager == "https://management.azure.com/"


def test_load_subscription_from_credential_file(monkeypatch):
    # arrange
    monkeypatch.setenv(
        "AZURE_AUTH_LOCATION",
        os.path.join(settings_dir, 'credentials.json'))

    # act
    subscription_id = config.load_subscription_id()

    # assert
    assert subscription_id == "AZURE_SUBSCRIPTION_ID"


def test_load_explicit_timeout_from_experiment_dict():
    # arrange
    experiment_configuration = {
        "azure_subscription_id": "AZURE_SUBSCRIPTION_ID",
        "timeout": 500
    }

    # act
    timeout = config.load_timeout(experiment_configuration)

    # assert
    assert timeout == 500


def test_load_implicit_timeout_from_experiment_dict():
    # arrange
    experiment_configuration = {
        "azure_subscription_id": "AZURE_SUBSCRIPTION_ID",
    }

    # act
    timeout = config.load_timeout(experiment_configuration)

    # assert
    assert timeout == 600
