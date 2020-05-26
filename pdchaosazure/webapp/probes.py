from chaoslib import Configuration, Secrets
from logzero import logger

from pdchaosazure.common.resources.graph import fetch_resources
from pdchaosazure.webapp.constants import RES_TYPE_WEBAPP


def describe_webapps(filter: str = None,
                     configuration: Configuration = None,
                     secrets: Secrets = None):
    """Describe web app instances.

    Parameters
    ----------
    filter : str, optional
        Filter the web app instance(s). If omitted a random instance from your subscription is selected.
    """
    logger.debug(
        "Starting {}: configuration='{}', filter='{}'".format(describe_webapps.__name__, configuration, filter))

    return fetch_resources(filter, RES_TYPE_WEBAPP, secrets, configuration)


def count_webapps(filter: str = None,
                  configuration: Configuration = None,
                  secrets: Secrets = None) -> int:
    """Return count of web app instances.

    Parameters
    ----------
    filter : str, optional
        Filter the web app instance(s). If omitted a random instance from your subscription is selected.
    """
    logger.debug("Start {}: configuration='{}', filter='{}'".format(count_webapps.__name__, configuration, filter))

    webapps = fetch_resources(filter, RES_TYPE_WEBAPP, secrets, configuration)
    return len(webapps)
