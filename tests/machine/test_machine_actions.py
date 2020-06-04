from unittest.mock import MagicMock, patch

from azure.mgmt.compute import ComputeManagementClient

import pdchaosazure
from pdchaosazure.common import config
from pdchaosazure.machine.actions import (burn_io, fill_disk, delete_machines, network_latency,
                                          restart_machines, stop_machines, stress_cpu)
from tests.data import machine_provider, config_provider, secrets_provider

MACHINE_ALPHA = {
    'name': 'VirtualMachineAlpha',
    'resourceGroup': 'group'}

MACHINE_BETA = {
    'name': 'VirtualMachineBeta',
    'resourceGroup': 'group'}


class AnyStringWith(str):
    def __eq__(self, other):
        return self in other


@patch('pdchaosazure.machine.actions.fetch_machines', autospec=True)
@patch('pdchaosazure.machine.actions.init_client', autospec=True)
def test_delete_one_machine(init, fetch):
    client = MagicMock()
    init.return_value = client

    fetch.return_value = [MACHINE_ALPHA]

    configuration = config_provider.provide_default_config()
    secrets = secrets_provider.provide_secrets_via_service_principal()

    f = "where resourceGroup=='myresourcegroup' | sample 1"
    delete_machines(f, configuration, secrets)

    fetch.assert_called_with(f, configuration, secrets)
    assert client.virtual_machines.delete.call_count == 1


@patch('pdchaosazure.machine.actions.fetch_machines', autospec=True)
@patch('pdchaosazure.machine.actions.init_client', autospec=True)
def test_delete_two_machines(init, fetch):
    client = MagicMock()
    init.return_value = client

    fetch.return_value = [MACHINE_ALPHA, MACHINE_BETA]

    configuration = config_provider.provide_default_config()
    secrets = secrets_provider.provide_secrets_via_service_principal()

    f = "where resourceGroup=='myresourcegroup' | sample 2"
    delete_machines(f, configuration, secrets)

    fetch.assert_called_with(f, configuration, secrets)
    assert client.virtual_machines.delete.call_count == 2


@patch('pdchaosazure.machine.actions.fetch_machines', autospec=True)
@patch('pdchaosazure.machine.actions.init_client', autospec=True)
def test_stop_one_machine(init, fetch):
    client = MagicMock()
    init.return_value = client

    machines = [MACHINE_ALPHA]
    fetch.return_value = machines

    configuration = config_provider.provide_default_config()
    secrets = secrets_provider.provide_secrets_via_service_principal()

    f = "where resourceGroup=='myresourcegroup' | sample 1"
    stop_machines(f, configuration, secrets)

    fetch.assert_called_with(f, configuration, secrets)
    assert client.virtual_machines.power_off.call_count == 1


@patch('pdchaosazure.machine.actions.fetch_machines', autospec=True)
@patch('pdchaosazure.machine.actions.init_client', autospec=True)
def test_stop_two_machines(init, fetch):
    client = MagicMock()
    init.return_value = client

    fetch.return_value = [MACHINE_ALPHA, MACHINE_BETA]

    configuration = config_provider.provide_default_config()
    secrets = secrets_provider.provide_secrets_via_service_principal()

    f = "where resourceGroup=='myresourcegroup' | sample 2"
    stop_machines(f, configuration, secrets)

    fetch.assert_called_with(f, configuration, secrets)
    assert client.virtual_machines.power_off.call_count == 2


@patch('pdchaosazure.machine.actions.fetch_machines', autospec=True)
@patch('pdchaosazure.machine.actions.init_client', autospec=True)
def test_restart_one_machine(init, fetch):
    client = MagicMock()
    init.return_value = client

    fetch.return_value = [MACHINE_ALPHA]

    configuration = config_provider.provide_default_config()
    secrets = secrets_provider.provide_secrets_via_service_principal()

    f = "where resourceGroup=='myresourcegroup' | sample 1"
    restart_machines(f, configuration, secrets)

    fetch.assert_called_with(f, configuration, secrets)
    assert client.virtual_machines.restart.call_count == 1


@patch('pdchaosazure.machine.actions.fetch_machines', autospec=True)
@patch('pdchaosazure.machine.actions.init_client', autospec=True)
def test_restart_two_machines(init, fetch):
    client = MagicMock()
    init.return_value = client

    fetch.return_value = [MACHINE_ALPHA, MACHINE_BETA]

    configuration = config_provider.provide_default_config()
    secrets = secrets_provider.provide_secrets_via_service_principal()

    f = "where resourceGroup=='myresourcegroup' | sample 2"
    restart_machines(f, configuration, secrets)

    fetch.assert_called_with(f, configuration, secrets)
    assert client.virtual_machines.restart.call_count == 2


@patch('pdchaosazure.machine.actions.fetch_machines', autospec=True)
@patch('pdchaosazure.machine.actions.init_client', autospec=True)
@patch.object(pdchaosazure.common.compute.command, 'prepare', autospec=True)
@patch.object(pdchaosazure.common.compute.command, 'run', autospec=True)
def test_stress_cpu(mocked_command_run, mocked_command_prepare, mocked_init_client, fetch):
    # arrange mocks
    operation_name = stress_cpu.__name__
    mocked_command_prepare.return_value = 'RunShellScript', '{}.sh'.format(operation_name)

    machine = machine_provider.default()
    fetch.return_value = [machine]

    mocked_client = MagicMock(spec=ComputeManagementClient)
    mocked_init_client.return_value = mocked_client

    configuration = config_provider.provide_default_config()
    secrets = secrets_provider.provide_secrets_via_service_principal()

    timeout = config.load_timeout(configuration)
    duration = 60

    # act
    stress_cpu(
        filter="where name=='some_linux_machine'", duration=duration, configuration=configuration, secrets=secrets)

    # assert
    fetch.assert_called_with("where name=='some_linux_machine'", configuration, secrets)
    mocked_command_prepare.assert_called_with(machine, operation_name)
    mocked_command_run.assert_called_with(
        machine['resourceGroup'], machine, duration + timeout,
        {
            'command_id': 'RunShellScript',
            'script': ['{}.sh'.format(operation_name)],
            'parameters': [
                {'name': "input_duration", 'value': duration}
            ]
        },
        mocked_client
    )


@patch('pdchaosazure.machine.actions.fetch_machines', autospec=True)
@patch('pdchaosazure.machine.actions.init_client', autospec=True)
@patch.object(pdchaosazure.common.compute.command, 'prepare', autospec=True)
@patch.object(pdchaosazure.common.compute.command, 'prepare_path', autospec=True)
@patch.object(pdchaosazure.common.compute.command, 'run', autospec=True)
def test_fill_disk(mocked_command_run, mocked_command_prepare_path, mocked_command_prepare,
                   mocked_init_client, fetch):
    # arrange mocks
    mocked_command_prepare.return_value = 'RunShellScript', 'fill_disk.sh'
    mocked_command_prepare_path.return_value = '/root/burn/hard'

    machine = machine_provider.default()
    fetch.return_value = [machine]

    mocked_client = MagicMock(spec=ComputeManagementClient)
    mocked_init_client.return_value = mocked_client

    configuration = config_provider.provide_default_config()
    secrets = secrets_provider.provide_secrets_via_service_principal()

    duration = 60
    timeout = config.load_timeout(configuration) + duration

    # act
    fill_disk(filter="where name=='some_linux_machine'", duration=duration, size=1000, path='/root/burn/hard',
              configuration=configuration, secrets=secrets)

    # assert
    fetch.assert_called_with("where name=='some_linux_machine'", configuration, secrets)
    mocked_command_prepare.assert_called_with(machine, 'fill_disk')
    mocked_command_run.assert_called_with(
        machine['resourceGroup'], machine, timeout,
        {
            'command_id': 'RunShellScript',
            'script': ['fill_disk.sh'],
            'parameters': [
                {'name': "input_duration", 'value': duration},
                {'name': "input_path", 'value': '/root/burn/hard'},
                {'name': "input_size", 'value': 1000}
            ]
        },
        mocked_client
    )


@patch('pdchaosazure.machine.actions.fetch_machines', autospec=True)
@patch('pdchaosazure.machine.actions.init_client', autospec=True)
@patch.object(pdchaosazure.common.compute.command, 'prepare', autospec=True)
@patch.object(pdchaosazure.common.compute.command, 'run', autospec=True)
def test_network_latency(mocked_command_run, mocked_command_prepare, mocked_init_client, fetch):
    # arrange mocks
    mocked_command_prepare.return_value = 'RunShellScript', 'network_latency.sh'

    machine = machine_provider.default()
    machines = [machine]
    fetch.return_value = machines

    mocked_client = MagicMock(spec=ComputeManagementClient)
    mocked_init_client.return_value = mocked_client

    configuration = config_provider.provide_default_config()
    secrets = secrets_provider.provide_secrets_via_service_principal()

    duration = 60
    timeout = config.load_timeout(configuration) + duration

    # act
    network_latency(
        filter="where name=='some_linux_machine'", duration=duration, delay=200, jitter=50,
        configuration=configuration, secrets=secrets)

    # assert
    fetch.assert_called_with("where name=='some_linux_machine'", configuration, secrets)
    mocked_command_prepare.assert_called_with(machine, 'network_latency')
    mocked_command_run.assert_called_with(
        machine['resourceGroup'], machine, timeout,
        {
            'command_id': 'RunShellScript',
            'script': ['network_latency.sh'],
            'parameters': [
                {'name': "input_delay", 'value': 200},
                {'name': "input_duration", 'value': duration},
                {'name': "input_jitter", 'value': 50},
                {'name': "input_network_interface", 'value': "eth0"}
            ]
        },
        mocked_client
    )


@patch('pdchaosazure.machine.actions.fetch_machines', autospec=True)
@patch('pdchaosazure.machine.actions.init_client', autospec=True)
@patch.object(pdchaosazure.common.compute.command, 'prepare', autospec=True)
@patch.object(pdchaosazure.common.compute.command, 'run', autospec=True)
def test_burn_io(mocked_command_run, mocked_command_prepare, mocked_init_client, fetch):
    # arrange mocks
    mocked_command_prepare.return_value = 'RunShellScript', 'burn_io.sh'

    machine = machine_provider.default()
    machines = [machine]
    fetch.return_value = machines

    configuration = config_provider.provide_default_config()
    secrets = secrets_provider.provide_secrets_via_service_principal()

    mocked_client = MagicMock(spec=ComputeManagementClient)
    mocked_init_client.return_value = mocked_client

    duration = 60
    timeout = config.load_timeout(configuration) + duration

    # act
    burn_io(filter="where name=='some_linux_machine'", duration=duration, configuration=configuration, secrets=secrets)

    # assert
    fetch.assert_called_with("where name=='some_linux_machine'", configuration, secrets)
    mocked_command_prepare.assert_called_with(machine, 'burn_io')
    mocked_command_run.assert_called_with(
        machine['resourceGroup'], machine, timeout,
        {
            'command_id': 'RunShellScript',
            'script': ['burn_io.sh'],
            'parameters': [
                {'name': 'input_duration', 'value': duration},
                {'name': 'input_path', 'value': '/root/burn'}
            ]
        },
        mocked_client
    )
