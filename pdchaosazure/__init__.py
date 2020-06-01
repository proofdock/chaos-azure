# -*- coding: utf-8 -*-

"""Top-level package for chaostoolkit-azure."""

from typing import List

from chaoslib.discovery import (discover_actions, discover_probes, initialize_discovery_result)
from chaoslib.types import (DiscoveredActivities, Discovery)
from logzero import logger

from pdchaosazure.auth import auth
from pdchaosazure.common.config import load_subscription_id, load_secrets  # noqa: F401

__all__ = [
    "__version__", "auth", "discover", "load_secrets", "load_subscription_id"
]
__version__ = '1.0.0'
__package__ = "proofdock-chaos-azure"


def discover(discover_system: bool = True) -> Discovery:
    """
    Discover Azure capabilities offered by this extension.
    """
    logger.info("Discovering capabilities from {}".format(__package__))

    discovery = initialize_discovery_result(__package__, __version__, "azure")
    discovery["activities"].extend(__load_exported_activities())
    return discovery


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
