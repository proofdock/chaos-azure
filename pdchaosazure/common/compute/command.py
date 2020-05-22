import os

from chaoslib.exceptions import FailedActivity, InterruptExecution
from logzero import logger
from msrestazure import azure_exceptions

from pdchaosazure import init_client
from pdchaosazure.common import config
from pdchaosazure.machine.constants import OS_LINUX, OS_WINDOWS, RES_TYPE_VM
from pdchaosazure.vmss.constants import RES_TYPE_VMSS_VM

UNSUPPORTED_WINDOWS_SCRIPTS = ['network_latency', 'burn_io']


def prepare_path(machine: dict, path: str):
    os_type = __get_os_type(machine)
    if os_type == OS_LINUX:
        result = "/root/burn" if path is None else path
    else:
        result = "C:/burn" if path is None else path

    return result


def prepare(compute: dict, script: str):
    os_type = __get_os_type(compute)
    if os_type == OS_LINUX:
        command_id = 'RunShellScript'
        script_name = "{}.sh".format(script)
    else:
        if script in UNSUPPORTED_WINDOWS_SCRIPTS:
            raise InterruptExecution("'{}' is not supported for os '{}'"
                                     .format(script, OS_WINDOWS))
        command_id = 'RunPowerShellScript'
        script_name = "{}.ps1".format(script)

    file_path = os.path.join(
        os.path.dirname(__file__), "../scripts", script_name)
    with open(file_path) as file_path:
        script_content = file_path.read()
        return command_id, script_content


def run(resource_group: str, compute: dict, duration: int, parameters: dict,
        secrets, configuration):
    client = init_client(secrets, configuration)
    compute_type = compute.get('type').lower()

    try:
        if compute_type == RES_TYPE_VMSS_VM.lower():
            poller = client.virtual_machine_scale_set_vms.run_command(
                resource_group, compute['scale_set'], compute['instance_id'], parameters)

        elif compute_type == RES_TYPE_VM.lower():
            poller = client.virtual_machines.run_command(
                resource_group, compute['name'], parameters)

        else:
            msg = "Running a command for the unknown resource type '{}'" \
                .format(compute.get('type'))
            raise InterruptExecution(msg)

    except azure_exceptions.CloudError as e:
        msg = e.message
        raise FailedActivity(msg)
        logger.error(msg)

    timeout = config.load_timeout(configuration) + duration
    result = poller.result(timeout)  # Blocking till executed
    if result and result.value:
        logger.debug(result.value[0].message)  # stdout/stderr
    else:
        raise FailedActivity("Operation did not finish properly."
                             " You may consider to increase the timeout in the experiment configuration.")


#####################
# HELPER FUNCTIONS
####################
def __get_os_type(compute):
    compute_type = compute['type'].lower()

    if compute_type == RES_TYPE_VMSS_VM.lower():
        os_type = compute['storage_profile']['os_disk']['os_type']

    elif compute_type == RES_TYPE_VM.lower():
        os_type = compute['properties']['storageProfile']['osDisk']['osType']

    else:
        msg = "Trying to run a command for the unknown resource type '{}'" \
            .format(compute.get('type'))
        raise InterruptExecution(msg)

    if os_type.lower() not in (OS_LINUX, OS_WINDOWS):
        raise FailedActivity("Unknown OS Type: %s" % os_type)

    return os_type.lower()
