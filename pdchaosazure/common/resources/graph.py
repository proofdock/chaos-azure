from typing import List

from azure.core.exceptions import HttpResponseError
from chaoslib.exceptions import InterruptExecution, FailedActivity
from chaoslib.types import Secrets, Configuration

from pdchaosazure.common.resources import query, init_client


def fetch_resources(user_query: str, resource_type: str,
                    secrets: Secrets, configuration: Configuration):
    # prepare query
    query_request = query.create_request(resource_type, user_query, configuration)

    # prepare resource graph client
    try:
        client = init_client(secrets)
        resources = client.resources(query_request)
    except HttpResponseError as e:
        raise InterruptExecution(e.message)

    # prepare results
    results = __to_dicts(resources.data)

    if not results:
        raise FailedActivity("Could not find resources of type '{}' and filter '{}'".format(resource_type, user_query))

    return results


def __to_dicts(table) -> List[dict]:
    results = []

    for row in table['rows']:
        result = {}
        for col_index in range(len(table['columns'])):
            result[table['columns'][col_index]['name']] = row[col_index]
        results.append(result)

    return results
