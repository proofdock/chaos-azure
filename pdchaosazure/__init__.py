# -*- coding: utf-8 -*-

"""Top-level package for chaostoolkit-azure."""

from typing import List

from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resourcegraph import ResourceGraphClient
from chaoslib.discovery import (discover_actions, discover_probes,
                                initialize_discovery_result)
from chaoslib.types import (Configuration, DiscoveredActivities, Discovery,
                            Secrets)
from logzero import logger

from pdchaosazure.auth import auth
from pdchaosazure.common.config import load_configuration, load_secrets

__all__ = [
    "__version__", "discover", "init_client", "init_resource_graph_client"
]
__version__ = '0.8.11'


def discover(discover_system: bool = True) -> Discovery:
    """
    Discover Azure capabilities offered by this extension.
    """
    logger.info("Discovering capabilities from chaostoolkit-azure")

    discovery = initialize_discovery_result(
        "chaostoolkit-azure", __version__, "azure")
    discovery["activities"].extend(__load_exported_activities())
    return discovery


def init_client(
        experiment_secrets: Secrets,
        experiment_configuration: Configuration) -> ComputeManagementClient:

    secrets = load_secrets(experiment_secrets)
    configuration = load_configuration(experiment_configuration)
    with auth(secrets) as authentication:
        base_url = secrets.get('cloud').endpoints.resource_manager
        client = ComputeManagementClient(
            credentials=authentication,
            subscription_id=configuration.get('subscription_id'),
            base_url=base_url)

        return client


def init_resource_graph_client(
        experiment_secrets: Secrets) -> ResourceGraphClient:

    secrets = load_secrets(experiment_secrets)
    with auth(secrets) as authentication:
        base_url = secrets.get('cloud').endpoints.resource_manager
        client = ResourceGraphClient(
            credentials=authentication,
            base_url=base_url)

        return client


###############################################################################
# Private functions
###############################################################################
def __load_exported_activities() -> List[DiscoveredActivities]:
    """
    Extract metadata from actions and probes exposed by this extension.
    """
    activities = []

    # actions
    activities.extend(discover_actions("pdchaosazure.aks.actions"))
    activities.extend(discover_actions("pdchaosazure.machine.actions"))
    activities.extend(discover_actions("pdchaosazure.vmss.actions"))
    activities.extend(discover_actions("pdchaosazure.webapp.actions"))

    # probes
    activities.extend(discover_probes("pdchaosazure.machine.probes"))
    activities.extend(discover_probes("pdchaosazure.vmss.probes"))
    activities.extend(discover_probes("pdchaosazure.webapp.probes"))

    return activities
