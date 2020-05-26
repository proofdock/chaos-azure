from chaoslib.exceptions import FailedActivity

from pdchaosazure.aks.constants import RES_TYPE_AKS
from pdchaosazure.common.resources.graph import fetch_resources


def fetch_aks(filter, configuration, secrets):
    aks = fetch_resources(filter, RES_TYPE_AKS, secrets, configuration)

    if not aks:
        raise FailedActivity("No AKS clusters found")

    return aks
