from typing import List

from chaoslib.types import Configuration, Secrets
from logzero import logger

from pdchaosazure.aks.fetcher import fetch_aks
from pdchaosazure.machine.actions import delete_machines, stop_machines, \
    restart_machines

__all__ = ["delete_node", "restart_node", "stop_node"]


def delete_node(filter: str = None,
                configuration: Configuration = None,
                secrets: Secrets = None):
    """
    Delete a node at random from a managed Azure Kubernetes Service.

    **Be aware**: Deleting a node is an invasive action. You will not be able
    to recover the node once you deleted it.

    Parameters
    ----------
    filter : str
        Filter the managed AKS. If the filter is omitted all AKS in
        the subscription will be selected as potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug("Start {}: configuration='{}', filter='{}'".format(delete_node.__name__, configuration, filter))

    aks = fetch_aks(filter, configuration, secrets)
    query = __query_from_aks(aks)

    return delete_machines(query, configuration, secrets)


def stop_node(filter: str = None,
              configuration: Configuration = None,
              secrets: Secrets = None):
    """
    Stop a node at random from a managed Azure Kubernetes Service.

    Parameters
    ----------
    filter : str
        Filter the managed AKS. If the filter is omitted all AKS in
        the subscription will be selected as potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug("Starting {}: configuration='{}', filter='{}'".format(stop_node.__name__, configuration, filter))

    aks = fetch_aks(filter, configuration, secrets)
    query = __query_from_aks(aks)

    return stop_machines(query, configuration, secrets)


def restart_node(filter: str = None,
                 configuration: Configuration = None,
                 secrets: Secrets = None):
    """
    Restart a node at random from a managed Azure Kubernetes Service.

    Parameters
    ----------
    filter : str
        Filter the managed AKS. If the filter is omitted all AKS in
        the subscription will be selected as potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug("Starting {}: configuration='{}', filter='{}'".format(restart_node.__name__, configuration, filter))

    aks = fetch_aks(filter, configuration, secrets)
    query = __query_from_aks(aks)

    return restart_machines(query, configuration, secrets)


##################################################################
# HELPER FUNCTIONS
##################################################################
def __query_from_aks(aks_list: List[dict]) -> str:
    result = "where resourceGroup =~ '{}'".format(aks_list[0]['properties']['nodeResourceGroup'])

    for aks in aks_list[1:]:
        node_resource_group = aks['properties']['nodeResourceGroup']
        result += " or resourceGroup =~ '{}'".format(node_resource_group)

    return result
