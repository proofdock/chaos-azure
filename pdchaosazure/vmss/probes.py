# -*- coding: utf-8 -*-
from chaoslib.types import Configuration, Secrets
from logzero import logger

__all__ = ["count_instances"]

from pdchaosazure.common.compute import init_client
from pdchaosazure.vmss.fetcher import fetch_vmss, fetch_all_vmss_instances


def count_instances(filter: str = None,
                    configuration: Configuration = None,
                    secrets: Secrets = None) -> int:
    """
    Return count of VMSS instances.

    Parameters
    ----------
    filter : str, optional
        Filter the virtual machine scale set(s). If omitted a random VMSS from your subscription is selected.
    """
    logger.debug(
        "Starting {}: configuration='{}', filter='{}'".format(count_instances.__name__, configuration, filter))

    result = []
    client = init_client(secrets, configuration)
    vmss_list = fetch_vmss(filter, configuration, secrets)
    for vmss in vmss_list:
        instances = fetch_all_vmss_instances(vmss, client)
        result.extend(instances)

    return len(result)
