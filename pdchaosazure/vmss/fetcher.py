from typing import Any, Dict, List

import jmespath
from azure.mgmt.compute import ComputeManagementClient
from chaoslib.exceptions import InterruptExecution

from pdchaosazure.common import kustolight
from pdchaosazure.common.resources.graph import fetch_resources
from pdchaosazure.vmss.constants import RES_TYPE_VMSS


def fetch_instances(vmss, filter_instances: str, client: ComputeManagementClient) -> List[Dict[str, Any]]:
    if not filter_instances:
        filter_instances = "sample 1"

    try:
        instances = fetch_all_vmss_instances(vmss, client)
        result = kustolight.filter_resources(instances, filter_instances)
    except jmespath.exceptions.ParseError:
        raise InterruptExecution("'{}' is an invalid query. Please have a look at the documentation.".format(
            filter_instances))

    return result


def fetch_vmss(filter_vmss, configuration, secrets) -> List[dict]:
    vmss = fetch_resources(filter_vmss, RES_TYPE_VMSS, secrets, configuration)
    return vmss


def fetch_all_vmss_instances(vmss, client: ComputeManagementClient) -> List[Dict]:
    vmss_instances = []
    pages = client.virtual_machine_scale_set_vms.list(vmss['resourceGroup'], vmss['name'])
    first_page = pages.advance_page()
    vmss_instances.extend(list(first_page))

    while True:
        try:
            page = pages.advance_page()
            vmss_instances.extend(list(page))
        except StopIteration:
            break

    results = __parse_vmss_instances_result(vmss_instances, vmss)
    return results


#############################################################################
# Private helper functions
#############################################################################
def __parse_vmss_instances_result(instances, vmss: dict) -> List[Dict]:
    results = []
    for instance in instances:
        instance_as_dict = instance.as_dict()
        instance_as_dict['scale_set'] = vmss['name']
        results.append(instance_as_dict)
    return results
