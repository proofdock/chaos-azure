from unittest.mock import patch

from pdchaosazure.vmss.probes import count_instances
from tests.data import vmss_provider


@patch('pdchaosazure.vmss.probes.fetch_all_vmss_instances', autospec=True)
@patch('pdchaosazure.vmss.probes.fetch_vmss', autospec=True)
def test_count_instances(mocked_fetch_vmss, mocked_all_vmss_instances):
    mocked_fetch_vmss.return_value = [vmss_provider.provide_scale_set()]
    mocked_all_vmss_instances.return_value = [vmss_provider.provide_instance()]

    count = count_instances(None, None)

    assert count == 1


@patch('pdchaosazure.vmss.probes.fetch_all_vmss_instances', autospec=True)
@patch('pdchaosazure.vmss.probes.fetch_vmss', autospec=True)
def test_count_instances_for_two_sets(mocked_fetch_vmss, mocked_all_vmss_instances):
    scale_sets = []
    scale_sets.append(vmss_provider.provide_scale_set())
    scale_sets.append(vmss_provider.provide_scale_set())
    mocked_fetch_vmss.return_value = scale_sets
    mocked_all_vmss_instances.return_value = [vmss_provider.provide_instance()]

    count = count_instances(None, None)

    assert count == 2
