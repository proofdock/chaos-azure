from chaoslib.exceptions import FailedActivity

from pdchaosazure.common.resources.graph import fetch_resources
from pdchaosazure.webapp.constants import RES_TYPE_WEBAPP


def fetch_webapps(filter, configuration, secrets):
    result = fetch_resources(filter, RES_TYPE_WEBAPP, secrets, configuration)

    if not result:
        raise FailedActivity("No web apps found")

    return result
