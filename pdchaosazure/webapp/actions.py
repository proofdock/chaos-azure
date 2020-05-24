from chaoslib import Secrets, Configuration
from chaoslib.exceptions import FailedActivity
from logzero import logger
from msrestazure import azure_exceptions

from pdchaosazure import init_client
from pdchaosazure.common import cleanse, config
from pdchaosazure.common.resources.graph import fetch_resources
from pdchaosazure.vmss.records import Records
from pdchaosazure.webapp.constants import RES_TYPE_WEBAPP

__all__ = ["stop_webapp", "restart_webapp", "delete_webapp"]


def stop_webapp(filter: str = None,
                configuration: Configuration = None,
                secrets: Secrets = None):
    """
    Stop a web app at random.

    Parameters
    ----------
    filter : str
        Filter the web apps. If the filter is omitted all web apps in
        the subscription will be selected as potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug("Starting {}: configuration='{}', filter='{}'".format(stop_webapp.__name__, configuration, filter))

    client = init_client(secrets, configuration)
    webapps = __fetch_webapps(filter, configuration, secrets)
    webapps_records = Records()
    
    for webapp in webapps:
        logger.debug("Stopping web app: {}".format(webapp['name']))
        
        try:
            poller = client.web_apps.stop(webapp['resourceGroup'], webapp['name'])

        except azure_exceptions.CloudError as e:
            raise FailedActivity(e.message)
        poller.result(config.load_timeout(configuration))
        webapps_records.add(cleanse.machine(webapp))

    return webapps_records.output_as_dict('resources')


def restart_webapp(filter: str = None,
                   configuration: Configuration = None,
                   secrets: Secrets = None):
    """
    Restart a web app at random.

    Parameters
    ----------
    filter : str
        Filter the web apps. If the filter is omitted all web apps in
        the subscription will be selected as potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug("Starting {}: configuration='{}', filter='{}'".format(restart_webapp.__name__, configuration, filter))

    webapps = __fetch_webapps(filter, configuration, secrets)
    compute_client = init_client(secrets, configuration)
    webapps_records = Records()
    for webapp in webapps:
        logger.debug("Restarting web app: {}".format(webapp['name']))
        poller = compute_client.web_apps.restart(webapp['resourceGroup'], webapp['name'])
        poller.result(config.load_timeout(configuration))
        webapps_records.add(cleanse.machine(webapp))

    return webapps_records.output_as_dict('resources')


def delete_webapp(filter: str = None,
                  configuration: Configuration = None,
                  secrets: Secrets = None):
    """
    Delete a web app at random.

    ***Be aware**: Deleting a web app is an invasive action. You will not be
    able to recover the web app once you deleted it.

    Parameters
    ----------
    filter : str
        Filter the web apps. If the filter is omitted all web apps in
        the subscription will be selected as potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug("Starting {}: configuration='{}', filter='{}'".format(delete_webapp.__name__, configuration, filter))

    webapps = __fetch_webapps(filter, configuration, secrets)
    compute_client = init_client(secrets, configuration)
    webapps_records = Records()
    for webapp in webapps:
        logger.debug("Deleting web app: {}".format(webapp['name']))
        poller = compute_client.web_apps.delete(webapp['resourceGroup'], webapp['name'])
        poller.result(config.load_timeout(configuration))
        webapps_records.add(cleanse.machine(webapp))

    return webapps_records.output_as_dict('resources')


###############################################################################
# Private helper functions
###############################################################################
def __fetch_webapps(filter, configuration, secrets):
    result = fetch_resources(filter, RES_TYPE_WEBAPP, secrets, configuration)
    if not result:
        logger.warning("No web apps found")
        raise FailedActivity("No web apps found")
    return result
