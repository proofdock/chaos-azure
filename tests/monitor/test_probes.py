from unittest.mock import patch, MagicMock

from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.monitor.v2018_03_01.models import MetricAlertStatusCollection

from pdchaosazure.monitor import probes
from tests.monitor.fixtures import alert_status


@patch('pdchaosazure.monitor.probes.client.init', autospec=True)
def test_is_alert_healthy_is_called_properly(client):
    # arrange
    client = MagicMock(spec=MonitorManagementClient)

    # act
    probes.is_alert_healthy(
        resource_group="sample-rg",
        alert_rule="sample-alert-rule",
        configuration={},
        secrets={}
    )

    client.metric_alerts_status.list.called_once_with("sample-rg", "sample-alert-rule", {}, {})


@patch('pdchaosazure.monitor.probes.client.init', autospec=True)
def test_is_alert_healthy_is_happy(client):
    # arrange
    magic_client = MagicMock(spec=MonitorManagementClient)
    client.return_value = magic_client

    status = alert_status.healthy()
    collection = MetricAlertStatusCollection(value=status['value'])
    magic_client.metric_alerts_status.list.return_value = collection

    # act
    is_healthy = probes.is_alert_healthy(
        resource_group="sample-rg",
        alert_rule="sample-alert-rule",
        configuration={},
        secrets={}
    )

    assert is_healthy


@patch('pdchaosazure.monitor.probes.client.init', autospec=True)
def test_is_alert_healthy_is_unhappy(client):
    # arrange
    magic_client = MagicMock(spec=MonitorManagementClient)
    client.return_value = magic_client

    status = alert_status.unhealthy()
    collection = MetricAlertStatusCollection(value=status['value'])
    magic_client.metric_alerts_status.list.return_value = collection

    # act
    is_healthy = probes.is_alert_healthy(
        resource_group="sample-rg",
        alert_rule="sample-alert-rule",
        configuration={},
        secrets={}
    )

    assert not is_healthy
