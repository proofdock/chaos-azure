from unittest.mock import patch, ANY

import pytest
from chaoslib.exceptions import FailedActivity

import pdchaosazure
from pdchaosazure.common import config
from pdchaosazure.vmss.actions import delete_instance, restart_instance, stop_instance, \
    deallocate_instance, network_latency, burn_io, fill_disk, stress_cpu
from tests.data import config_provider, secrets_provider, vmss_provider
from tests.vmss.mock_client import MockComputeManagementClient


@patch('pdchaosazure.vmss.actions.fetch_vmss', autospec=True)
@patch('pdchaosazure.vmss.actions.fetch_instances', autospec=True)
@patch('pdchaosazure.vmss.actions.init_client', autospec=True)
def test_deallocate_vmss(client, fetch_instances, fetch_vmss):
    scale_set = vmss_provider.provide_scale_set()
    scale_sets = [scale_set]
    fetch_vmss.return_value = scale_sets

    instance = vmss_provider.provide_instance()
    instances = [instance]
    fetch_instances.return_value = instances

    client.return_value = MockComputeManagementClient()

    deallocate_instance(None, None, None)


@patch('pdchaosazure.vmss.actions.fetch_vmss', autospec=True)
@patch('pdchaosazure.vmss.actions.fetch_instances', autospec=True)
@patch('pdchaosazure.vmss.actions.init_client', autospec=True)
def test_stop_vmss(client, fetch_instances, fetch_vmss):
    scale_set = vmss_provider.provide_scale_set()
    scale_sets = [scale_set]
    instance = vmss_provider.provide_instance()
    instances = [instance]
    fetch_vmss.return_value = scale_sets
    fetch_instances.return_value = instances

    client.return_value = MockComputeManagementClient()

    stop_instance(None, None, None, None)


@patch('pdchaosazure.vmss.actions.fetch_vmss', autospec=True)
@patch('pdchaosazure.vmss.actions.fetch_instances', autospec=True)
@patch('pdchaosazure.vmss.actions.init_client', autospec=True)
def test_restart_vmss(client, fetch_instances, fetch_vmss):
    scale_set = vmss_provider.provide_scale_set()
    scale_sets = [scale_set]
    instance = vmss_provider.provide_instance()
    instances = [instance]
    fetch_vmss.return_value = scale_sets
    fetch_instances.return_value = instances

    client.return_value = MockComputeManagementClient()

    restart_instance(None, None, None)


@patch('pdchaosazure.vmss.actions.fetch_vmss', autospec=True)
@patch('pdchaosazure.vmss.actions.fetch_instances', autospec=True)
@patch('pdchaosazure.vmss.actions.init_client', autospec=True)
def test_delete_vmss(client, fetch_instances, fetch_vmss):
    scale_set = vmss_provider.provide_scale_set()
    scale_sets = [scale_set]
    instance = vmss_provider.provide_instance()
    instances = [instance]
    fetch_vmss.return_value = scale_sets
    fetch_instances.return_value = instances

    client.return_value = MockComputeManagementClient()

    delete_instance(None, None, None)


@patch('pdchaosazure.vmss.actions.fetch_vmss', autospec=True)
@patch('pdchaosazure.vmss.actions.fetch_instances', autospec=True)
@patch('pdchaosazure.vmss.actions.init_client', autospec=True)
@patch.object(pdchaosazure.common.compute.command, 'run', autospec=True)
def test_stress_cpu(mocked_command_run, mocked_init_client, mocked_instances, mocked_vmss):
    # arrange mocks
    scale_set = vmss_provider.provide_scale_set()
    scale_sets = [scale_set]
    instance = vmss_provider.provide_instance()
    instances = [instance]
    mocked_vmss.return_value = scale_sets
    mocked_instances.return_value = instances

    configuration = config_provider.provide_default_config()
    secrets = secrets_provider.provide_secrets_via_service_principal()

    duration = 60
    timeout = config.load_timeout(configuration) + duration

    client = MockComputeManagementClient()
    mocked_init_client.return_value = client

    # act
    stress_cpu(
        filter_vmss="where name=='some_random_instance'", duration=duration, configuration=configuration,
        secrets=secrets)

    # assert
    mocked_vmss.assert_called_with("where name=='some_random_instance'", configuration, secrets)
    mocked_instances.assert_called_with(scale_set, None, mocked_init_client.return_value)
    mocked_command_run.assert_called_with(scale_set['resourceGroup'], instance, timeout, parameters=ANY, client=client)


@patch('pdchaosazure.vmss.actions.fetch_vmss', autospec=True)
@patch('pdchaosazure.vmss.actions.fetch_instances', autospec=True)
@patch('pdchaosazure.vmss.actions.init_client', autospec=True)
@patch.object(pdchaosazure.common.compute.command, 'run', autospec=True)
def test_network_latency(mocked_command_run, mocked_init_client, mocked_fetch_instances, mocked_fetch_vmss):
    # arrange mocks
    scale_set = vmss_provider.provide_scale_set()
    instance = vmss_provider.provide_instance()
    mocked_fetch_vmss.return_value = [scale_set]
    mocked_fetch_instances.return_value = [instance]

    configuration = config_provider.provide_default_config()
    secrets = secrets_provider.provide_secrets_via_service_principal()

    duration = 60
    timeout = config.load_timeout(configuration) + duration

    mocked_client = MockComputeManagementClient()
    mocked_init_client.return_value = mocked_client

    # act
    network_latency(filter_vmss="where name=='some_random_instance'", duration=duration, delay=200, jitter=50,
                    configuration=configuration, secrets=secrets)

    # assert
    mocked_fetch_vmss.assert_called_with("where name=='some_random_instance'", configuration, secrets)
    mocked_fetch_instances.assert_called_with(scale_set, None, mocked_init_client.return_value)
    mocked_command_run.assert_called_with(
        scale_set['resourceGroup'], instance, timeout, parameters=ANY, client=mocked_client)


@patch('pdchaosazure.vmss.actions.fetch_vmss', autospec=True)
@patch('pdchaosazure.vmss.actions.fetch_instances', autospec=True)
@patch('pdchaosazure.vmss.actions.init_client', autospec=True)
@patch.object(pdchaosazure.common.compute.command, 'run', autospec=True)
def test_burn_io(mocked_command_run, mocked_init_client, fetch_instances, fetch_vmss):
    # arrange mocks
    scale_set = vmss_provider.provide_scale_set()
    scale_sets = [scale_set]
    instance = vmss_provider.provide_instance()
    instances = [instance]
    fetch_vmss.return_value = scale_sets
    fetch_instances.return_value = instances

    configuration = config_provider.provide_default_config()
    secrets = secrets_provider.provide_secrets_via_service_principal()

    mocked_client = MockComputeManagementClient()
    mocked_init_client.return_value = mocked_client

    duration = 60
    timeout = config.load_timeout(configuration) + duration

    # act
    burn_io(
        filter_vmss="where name=='some_random_instance'", duration=duration,
        configuration=configuration, secrets=secrets)

    # assert
    fetch_vmss.assert_called_with("where name=='some_random_instance'", configuration, secrets)
    fetch_instances.assert_called_with(scale_set, None, mocked_init_client.return_value)
    mocked_command_run.assert_called_with(
        scale_set['resourceGroup'], instance, timeout, parameters=ANY, client=mocked_client)


@patch('pdchaosazure.vmss.actions.fetch_vmss', autospec=True)
@patch('pdchaosazure.vmss.actions.fetch_instances', autospec=True)
@patch('pdchaosazure.vmss.actions.init_client', autospec=True)
@patch.object(pdchaosazure.common.compute.command, 'prepare_path', autospec=True)
@patch.object(pdchaosazure.common.compute.command, 'run', autospec=True)
def test_fill_disk(mocked_command_run, mocked_command_prepare_path, mocked_init_client, fetch_instances, fetch_vmss):
    # arrange mocks
    mocked_command_prepare_path.return_value = '/root/burn/hard'

    scale_set = vmss_provider.provide_scale_set()
    instance = vmss_provider.provide_instance()
    fetch_vmss.return_value = [scale_set]
    fetch_instances.return_value = [instance]

    configuration = config_provider.provide_default_config()
    secrets = secrets_provider.provide_secrets_via_service_principal()

    mocked_client = MockComputeManagementClient()
    mocked_init_client.return_value = mocked_client

    duration = 60
    timeout = config.load_timeout(configuration) + duration

    # act
    fill_disk(
        filter_vmss="where name=='some_random_instance'", duration=duration, size=1000, path='/root/burn/hard',
        configuration=configuration, secrets=secrets)

    # assert
    fetch_vmss.assert_called_with("where name=='some_random_instance'", configuration, secrets)
    fetch_instances.assert_called_with(scale_set, None, mocked_init_client.return_value)
    mocked_command_run.assert_called_with(
        scale_set['resourceGroup'], instance, timeout, parameters=ANY, client=mocked_client)


@patch('pdchaosazure.vmss.actions.fetch_vmss', autospec=True)
@patch('pdchaosazure.vmss.actions.fetch_instances', autospec=True)
@patch('pdchaosazure.vmss.actions.init_client', autospec=True)
@patch.object(pdchaosazure.common.compute.command, 'prepare_path', autospec=True)
@patch.object(pdchaosazure.common.compute.command, 'run', side_effect=FailedActivity("Activity monkey has failed"))
def test_unhappily_fill_disk(mocked_command_run, mocked_command_prepare_path,
                             mocked_init_client, fetch_instances, fetch_vmss):
    # arrange mocks
    mocked_command_prepare_path.return_value = '/root/burn/hard'

    scale_set = vmss_provider.provide_scale_set()
    instance = vmss_provider.provide_instance()
    fetch_vmss.return_value = [scale_set]
    fetch_instances.return_value = [instance]

    configuration = config_provider.provide_default_config()
    secrets = secrets_provider.provide_secrets_via_service_principal()

    mocked_client = MockComputeManagementClient()
    mocked_init_client.return_value = mocked_client

    # act
    with pytest.raises(FailedActivity):
        fill_disk(
            filter_vmss="where name=='some_random_instance'", duration=60, size=1000, path='/root/burn/hard',
            configuration=configuration, secrets=secrets)

    # assert
    fetch_vmss.assert_called_with("where name=='some_random_instance'", configuration, secrets)
    fetch_instances.assert_called_with(scale_set, None, mocked_init_client.return_value)
