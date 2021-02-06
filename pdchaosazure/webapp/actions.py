from azure.core.exceptions import HttpResponseError
from chaoslib import Configuration, Secrets
from chaoslib.exceptions import FailedActivity
from logzero import logger

from pdchaosazure.common import cleanse
from pdchaosazure.vmss.records import Records

# sort alphabetically to find 'em quicker
__all__ = ["delete", "restart", "stop"]

from pdchaosazure.webapp import client

from pdchaosazure.webapp.fetcher import fetch_webapps


def stop(filter: str = None,
         configuration: Configuration = None,
         secrets: Secrets = None):
    """Stop web app instances.

    Parameters
    ----------
    filter : str, optional
        Filter the web app instance(s). If omitted a random instance from your subscription is selected.
    """
    logger.debug("Starting {}: configuration='{}', filter='{}'".format(stop.__name__, configuration, filter))

    clnt = client.init()
    webapps = fetch_webapps(filter, configuration, secrets)
    webapps_records = Records()

    for webapp in webapps:
        try:
            logger.debug("Stopping web app: {}".format(webapp['name']))
            clnt.web_apps.stop(webapp['resourceGroup'], webapp['name'])
            webapps_records.add(cleanse.machine(webapp))

        except HttpResponseError as e:
            raise FailedActivity(e.message)

    return webapps_records.output_as_dict('resources')


def restart(filter: str = None,
            configuration: Configuration = None,
            secrets: Secrets = None):
    """Restart web app instances.

    Parameters
    ----------
    filter : str, optional
        Filter the web app instance(s). If omitted a random instance from your subscription is selected.
    """
    logger.debug("Starting {}: configuration='{}', filter='{}'".format(restart.__name__, configuration, filter))

    webapps = fetch_webapps(filter, configuration, secrets)
    clnt = client.init()
    webapps_records = Records()

    for webapp in webapps:
        try:
            logger.debug("Restarting web app: {}".format(webapp['name']))
            clnt.web_apps.restart(webapp['resourceGroup'], webapp['name'])
            webapps_records.add(cleanse.machine(webapp))
        except HttpResponseError as e:
            raise FailedActivity(e.message)

    return webapps_records.output_as_dict('resources')


def delete(filter: str = None,
           configuration: Configuration = None,
           secrets: Secrets = None):
    """Delete web app instances.

    **Be aware**: Deleting a web app is an invasive action. You will not be
    able to recover the web app once you deleted it.

    Parameters
    ----------
    filter : str, optional
        Filter the web app instance(s). If omitted a random instance from your subscription is selected.
    """
    logger.debug("Starting {}: configuration='{}', filter='{}'".format(delete.__name__, configuration, filter))

    webapps = fetch_webapps(filter, configuration, secrets)
    clnt = client.init()
    webapps_records = Records()

    for webapp in webapps:
        try:
            logger.debug("Deleting web app: {}".format(webapp['name']))
            clnt.web_apps.delete(webapp['resourceGroup'], webapp['name'])
            webapps_records.add(cleanse.machine(webapp))
        except HttpResponseError as e:
            raise FailedActivity(e.message)

    return webapps_records.output_as_dict('resources')
