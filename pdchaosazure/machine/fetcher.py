from typing import List

from pdchaosazure.common.resources.graph import fetch_resources
from pdchaosazure.machine.constants import RES_TYPE_VM


def fetch_machines(filter, configuration, secrets) -> List[dict]:
    machines = fetch_resources(filter, RES_TYPE_VM, secrets, configuration)
    return machines
