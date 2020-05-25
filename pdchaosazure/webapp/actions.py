from chaoslib import Secrets, Configuration
from chaoslib.exceptions import FailedActivity
from logzero import logger
from msrestazure import azure_exceptions

from pdchaosazure.common import cleanse, config
from pdchaosazure.vmss.records import Records
from pdchaosazure.webapp import init_client

# sort alphabetically to find 'em quicker
__all__ = ["delete_webapp", "restart_webapp", "stop_webapp"]

from pdchaosazure.webapp.fetcher import fetch_webapps


def stop_webapp(filter: str = None,
                configuration: Configuration = None,
                secrets: Secrets = None):
    """
    Stop web app instances either at random or by a defined filter.

    Parameters
    ----------
    filter : str, optional
        Filter the web app instance(s).
    """
    logger.debug("Starting {}: configuration='{}', filter='{}'".format(stop_webapp.__name__, configuration, filter))

    client = init_client(secrets, configuration)
    webapps = fetch_webapps(filter, configuration, secrets)
    webapps_records = Records()

    for webapp in webapps:
        logger.debug("Stopping web app: {}".format(webapp['name']))

        try:
            response = client.web_apps.stop(webapp['resourceGroup'], webapp['name'], raw=True)

        except azure_exceptions.CloudError as e:
            raise FailedActivity(e.message)

        webapps_records.add(cleanse.machine(webapp))

    return webapps_records.output_as_dict('resources')


def restart_webapp(filter: str = None,
                   configuration: Configuration = None,
                   secrets: Secrets = None):
    """
    Restart web app instances either at random or by a defined filter.

    Parameters
    ----------
    filter : str, optional
        Filter the web app instance(s).
    """
    logger.debug("Starting {}: configuration='{}', filter='{}'".format(restart_webapp.__name__, configuration, filter))

    webapps = fetch_webapps(filter, configuration, secrets)
    client = init_client(secrets, configuration)
    webapps_records = Records()
    for webapp in webapps:
        logger.debug("Restarting web app: {}".format(webapp['name']))
        response = client.web_apps.restart(webapp['resourceGroup'], webapp['name'], raw=True)
        webapps_records.add(cleanse.machine(webapp))

    return webapps_records.output_as_dict('resources')


def delete_webapp(filter: str = None,
                  configuration: Configuration = None,
                  secrets: Secrets = None):
    """
    Delete web app instances either at random or by a defined filter.

    **Be aware**: Deleting a web app is an invasive action. You will not be
    able to recover the web app once you deleted it.

    Parameters
    ----------
    filter : str, optional
        Filter the web app instance(s).
    """
    logger.debug("Starting {}: configuration='{}', filter='{}'".format(delete_webapp.__name__, configuration, filter))

    webapps = fetch_webapps(filter, configuration, secrets)
    client = init_client(secrets, configuration)
    webapps_records = Records()
    for webapp in webapps:
        logger.debug("Deleting web app: {}".format(webapp['name']))
        response = client.web_apps.delete(webapp['resourceGroup'], webapp['name'], raw=True)
        webapps_records.add(cleanse.machine(webapp))

    return webapps_records.output_as_dict('resources')
