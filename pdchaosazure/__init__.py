# -*- coding: utf-8 -*-

"""Top-level package for chaostoolkit-azure."""

from typing import List

from azure.mgmt.compute import ComputeManagementClient
from chaoslib.discovery import (discover_actions, discover_probes,
                                initialize_discovery_result)
from chaoslib.types import (Configuration, DiscoveredActivities, Discovery,
                            Secrets)
from logzero import logger

from pdchaosazure.auth import auth
from pdchaosazure.common.config import load_subscription_id, load_secrets

__all__ = [
    "__version__", "auth", "discover", "load_secrets", "init_client"
]
__version__ = '0.8.12-dev4'
__package__ = "proofdock-chaos-azure"


def discover(discover_system: bool = True) -> Discovery:
    """
    Discover Azure capabilities offered by this extension.
    """
    logger.info("Discovering capabilities from {}".format(__package__))

    discovery = initialize_discovery_result(__package__, __version__, "azure")
    discovery["activities"].extend(__load_exported_activities())
    return discovery


def init_client(experiment_secrets: Secrets, experiment_configuration: Configuration) -> ComputeManagementClient:
    secrets = load_secrets(experiment_secrets)
    configuration = load_subscription_id(experiment_configuration)

    with auth(secrets) as authentication:
        base_url = secrets.get('cloud').endpoints.resource_manager
        client = ComputeManagementClient(credentials=authentication,
                                         subscription_id=configuration.get('subscription_id'),
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
