from unittest.mock import patch

import pytest
from chaoslib.exceptions import FailedActivity

from pdchaosazure.aks.actions import restart_node, stop_node, delete_node
from tests.data import aks_provider


@patch('pdchaosazure.aks.actions.fetch_aks', autospec=True)
@patch('pdchaosazure.aks.actions.delete_machines', autospec=True)
def test_delete_node(delete, fetch):
    aks = aks_provider.default()
    fetch.return_value = [aks]

    delete_node(None, None, None)


@patch('pdchaosazure.aks.actions.fetch_aks', autospec=True)
@patch('pdchaosazure.aks.actions.stop_machines', autospec=True)
def test_stop_node(stop, fetch):
    aks = aks_provider.default()
    resource_list = [aks]
    fetch.return_value = resource_list

    stop_node(None, None, None)


@patch('pdchaosazure.aks.actions.fetch_aks', autospec=True)
@patch('pdchaosazure.aks.actions.restart_machines', autospec=True)
def test_restart_node(restart, fetch):
    aks = aks_provider.default()
    resource_list = [aks]
    fetch.return_value = resource_list

    restart_node(None, None, None)
