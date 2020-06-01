from azure.mgmt.compute import ComputeManagementClient
from chaoslib.exceptions import FailedActivity, InterruptExecution
from logzero import logger
from msrestazure import azure_exceptions
from pdchaoskit import scripts

from pdchaosazure.machine.constants import OS_LINUX, OS_WINDOWS, RES_TYPE_VM
from pdchaosazure.vmss.constants import RES_TYPE_VMSS_VM

UNSUPPORTED_WINDOWS_SCRIPTS = ['network_latency']


def prepare_path(machine: dict, path: str):
    os_type = __get_os_type(machine)
    if os_type == OS_LINUX:
        result = "/root/burn" if path is None else path
    else:
        result = "C:/burn" if path is None else path

    return result


def prepare(compute: dict, script_id: str):
    """Prepare the script
    :param compute: The instance to be attacked.
    :param script_id: The script's filename without the filename ending. Is named after the activity name.
    :return: A tuple of the Command Id and the script content
    """
    os_type = __get_os_type(compute)

    if os_type == OS_LINUX:
        command_id = 'RunShellScript'
        script_name = "{}.sh".format(script_id)
    else:
        if script_id in UNSUPPORTED_WINDOWS_SCRIPTS:
            raise InterruptExecution("'{}' is not supported for os '{}'"
                                     .format(script_id, OS_WINDOWS))
        command_id = 'RunPowerShellScript'
        script_name = "{}.ps1".format(script_id)

    script_content = scripts.get_content(script_name)
    return command_id, script_content


def run(resource_group: str, compute: dict, timeout: int, parameters: dict, client: ComputeManagementClient):
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
        raise FailedActivity(e.message)

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
