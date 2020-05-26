from datetime import datetime
from typing import List

from azure.mgmt.resourcegraph.models import ErrorResponseException
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
    except ErrorResponseException as e:
        msg = e.inner_exception.error.code
        if e.inner_exception.error.details:
            for d in e.inner_exception.error.details:
                msg += ": " + str(d)
        raise InterruptExecution(msg)

    # prepare results
    results = __to_dicts(resources.data, client.api_version)

    if not results:
        raise FailedActivity("Could not find resources of type '{}' and filter '{}'".format(resource_type, user_query))

    return results


def __to_dicts(table, version) -> List[dict]:
    results = []
    version_date = datetime.strptime(version, '%Y-%m-%d').date()

    if version_date >= datetime.strptime('2019-04-01', '%Y-%m-%d').date():
        for row in table['rows']:
            result = {}
            for col_index in range(len(table['columns'])):
                result[table['columns'][col_index]['name']] = row[col_index]
            results.append(result)

    else:
        for row in table.rows:
            result = {}
            for col_index in range(len(table.columns)):
                result[table.columns[col_index].name] = row[col_index]
            results.append(result)

    return results
