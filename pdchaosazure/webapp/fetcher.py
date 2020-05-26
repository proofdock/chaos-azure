from pdchaosazure.common.resources.graph import fetch_resources
from pdchaosazure.webapp.constants import RES_TYPE_WEBAPP


def fetch_webapps(filter, configuration, secrets):
    result = fetch_resources(filter, RES_TYPE_WEBAPP, secrets, configuration)
    return result
