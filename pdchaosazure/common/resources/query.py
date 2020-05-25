from azure.mgmt.resourcegraph.models import QueryRequest
from chaoslib import Configuration

from pdchaosazure.common.config import load_subscription_id


def create_request(
        resource_type: str, user_query: str, experiment_configuration: Configuration) -> QueryRequest:

    prepared_query = __prepare(resource_type, user_query)
    configuration = load_subscription_id(experiment_configuration)

    result = QueryRequest(
        query=prepared_query,
        subscriptions=[configuration.get('subscription_id')]
    )
    return result


def __prepare(resource_type: str, user_query: str) -> str:
    result = ["Resources", "where type=~'{}'".format(resource_type)]

    if user_query:
        result.append(user_query)
    else:
        result.append("sample 1")

    return " | ".join(result)
