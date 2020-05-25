from unittest.mock import patch

from pdchaosazure.vmss.probes import count_instances
from tests.data import vmss_provider
from tests.vmss.mock_client import MockComputeManagementClient


@patch('pdchaosazure.vmss.probes.fetch_all_vmss_instances', autospec=True)
@patch('pdchaosazure.vmss.probes.fetch_vmss', autospec=True)
@patch('pdchaosazure.vmss.probes.init_client', autospec=True)
def test_count_instances(mocked_client, mocked_fetch_vmss, mocked_all_vmss_instances):

    # Arrange
    mocked_fetch_vmss.return_value = [vmss_provider.provide_scale_set()]
    mocked_all_vmss_instances.return_value = [vmss_provider.provide_instance()]

    mocked_client.return_value = MockComputeManagementClient()

    count = count_instances(None, None)

    assert count == 1


@patch('pdchaosazure.vmss.probes.fetch_all_vmss_instances', autospec=True)
@patch('pdchaosazure.vmss.probes.fetch_vmss', autospec=True)
@patch('pdchaosazure.vmss.probes.init_client', autospec=True)
def test_count_instances_for_two_sets(mocked_client, mocked_fetch_vmss, mocked_all_vmss_instances):

    # Arrange
    scale_sets = []
    scale_sets.append(vmss_provider.provide_scale_set())
    scale_sets.append(vmss_provider.provide_scale_set())
    mocked_fetch_vmss.return_value = scale_sets
    mocked_all_vmss_instances.return_value = [vmss_provider.provide_instance()]

    mocked_client.return_value = MockComputeManagementClient()

    count = count_instances(None, None)

    assert count == 2
