# -*- coding: utf-8 -*-
from chaoslib.types import Configuration, Secrets
from logzero import logger

from pdchaosazure.machine.constants import RES_TYPE_VM
from pdchaosazure.common.resources.graph import fetch_resources

__all__ = ["describe_machines", "count_machines"]


def describe_machines(filter: str = None,
                      configuration: Configuration = None,
                      secrets: Secrets = None):
    """Describe Azure virtual machine instance(s).

    Parameters
    ----------
    filter : str
        Filter the virtual machine instance(s). If omitted a random instance from your subscription is selected.
    """
    logger.debug(
        "Starting {}: configuration='{}', filter='{}'".format(describe_machines.__name__, configuration, filter))

    result = fetch_resources(filter, RES_TYPE_VM, secrets, configuration)
    return result


def count_machines(filter: str = None,
                   configuration: Configuration = None,
                   secrets: Secrets = None) -> int:
    """
    Return count of Azure virtual machine instance(s).

    Parameters
    ----------
    filter : str
        Filter the virtual machine instance(s). If omitted a random instance from your subscription is selected.
    """
    logger.debug(
        "Starting {}: configuration='{}', filter='{}'".format(count_machines.__name__, configuration, filter))

    result = fetch_resources(filter, RES_TYPE_VM, secrets, configuration)
    return len(result)
