# -*- coding: utf-8 -*-
from azure.mgmt.monitor.models import (MetricAlertStatus,
                                       MetricAlertStatusProperties)
from chaoslib.types import Configuration, Secrets
from logzero import logger
from pdchaosazure.common.monitor import init_client

__all__ = ["is_alert_healthy"]


def is_alert_healthy(
        resource_group: str = None,
        alert_rule: str = None,
        configuration: Configuration = None,
        secrets: Secrets = None) -> bool:
    """
    Check if alert metric is healthy.

    Parameters
    ----------
    resource_group : str, required
        Name of the resource group the alert belongs to.
    alert_rule : str, required
        Name of the alert rule for which check will be performed.
    """
    logger.debug(
        "Starting {}: resource_group='{}', alert_rule='{}', configuration='{}'"
        .format(is_alert_healthy.__name__, resource_group, alert_rule, configuration))

    client = init_client(secrets, configuration)
    collection = client.metric_alerts_status.list(resource_group_name=resource_group, rule_name=alert_rule)
    for status in collection.value:
        status = MetricAlertStatus(status)
        properties = MetricAlertStatusProperties(status.properties)
        if str(properties.status).lower() != 'healthy':
            return False

    return True
