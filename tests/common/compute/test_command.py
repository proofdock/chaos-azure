from unittest.mock import MagicMock

import pytest
from azure.mgmt.compute import ComputeManagementClient
from chaoslib.exceptions import InterruptExecution

from pdchaosazure.common.compute import command
from tests.data import machine_provider


def test_prepare_path_linux():
    # arrange
    linux_machine = machine_provider.default()
    path = command.prepare_path(linux_machine, None)

    # assert
    assert path == "/root/burn"


def test_prepare_path_windows():
    # arrange
    windows_machine = machine_provider.default('Windows')
    path = command.prepare_path(windows_machine, None)

    # assert
    assert path == "C:/burn"


def test_prepare_unsupported_script_for_windows_machine():
    # arrange
    windows_machine = machine_provider.default('Windows')

    # assert
    with pytest.raises(InterruptExecution):
        command.prepare(windows_machine, "network_latency")


def test_prepare_supported_script_for_windows_machine():
    # arrange
    windows_machine = machine_provider.default('Windows')

    # act
    cmd_id, script_content = command.prepare(windows_machine, "stress_cpu")

    # assert
    assert cmd_id == 'RunPowerShellScript'


def test_run():
    # arrange
    machine = machine_provider.default()
    timeout = 120
    cmd, parameters = command.prepare(machine, "stress_cpu")
    mocked_client = MagicMock(spec=ComputeManagementClient)

    # act
    command.run(machine['resourceGroup'], machine, timeout, parameters, mocked_client)


def test_run_for_unknown_type():
    # arrange
    machine = machine_provider.default()
    machine['type'] = "Microsoft.Compute/unknownType"
    timeout = 120

    # act
    with pytest.raises(InterruptExecution):
        cmd, parameters = command.prepare(machine, "stress_cpu")
        mocked_client = MagicMock(spec=ComputeManagementClient)
        command.run(machine['resourceGroup'], machine, timeout, parameters, mocked_client)
