import random
from typing import Any, Dict, Iterable, Mapping, List

from azure.mgmt.compute import ComputeManagementClient
from chaoslib.exceptions import FailedActivity
from logzero import logger

from pdchaosazure.common.resources.graph import fetch_resources
from pdchaosazure.vmss.constants import RES_TYPE_VMSS


def fetch_instances(scale_set, instance_criteria, client: ComputeManagementClient) -> List[Dict[str, Any]]:
    if not instance_criteria:
        instance = __random_instance_from(scale_set, client)
        result = [instance]

    else:
        result = instances_by_criteria(scale_set, instance_criteria, client)

    return result


def instances_by_criteria(vmss: dict, instance_criteria, client) -> List[Dict[str, Any]]:
    result = []
    instances = fetch_all_vmss_instances(vmss, client)

    for instance in instances:
        if __is_criteria_matched(instance, instance_criteria):
            result.append(instance)

    if len(result) == 0:
        raise FailedActivity("No VMSS instance found for criteria '{}'".format(instance_criteria))

    return result


def fetch_vmss(filter, configuration, secrets) -> List[dict]:
    vmss = fetch_resources(filter, RES_TYPE_VMSS, secrets, configuration)

    if not vmss:
        raise FailedActivity("No VMSS found")

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
def __random_instance_from(scale_set, client) -> Dict[str, Any]:
    instances = fetch_all_vmss_instances(scale_set, client)
    if not instances:
        raise FailedActivity("No VMSS instances found")
    else:
        logger.debug("Found VMSS instances: {}".format([x['name'] for x in instances]))

    return random.choice(instances)


def __is_criteria_matched(instance: dict, criteria: Iterable[Mapping[str, any]] = None):
    for criterion in criteria:
        mismatch = False

        for key, value in criterion.items():
            if instance[key] != value:
                mismatch = True
                break

        if not mismatch:
            return True

    return False


def __parse_vmss_instances_result(instances, vmss: dict) -> List[Dict]:
    results = []
    for instance in instances:
        instance_as_dict = instance.as_dict()
        instance_as_dict['scale_set'] = vmss['name']
        results.append(instance_as_dict)
    return results
