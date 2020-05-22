from pdchaosazure.common.resources import query
from tests.data import config_provider


def test_create_query_with_empty_user_query():
    config = config_provider.provide_default_config()
    resource_type = "virtualMachine"
    user_query = ""
    query_request = query.create_request(resource_type, user_query, config)

    assert query_request.query == "Resources | where type=~'{}' | sample 1".format(resource_type)


def test_create_query_with_filled_user_query():
    config = config_provider.provide_default_config()
    resource_type = "virtualMachine"
    user_query = "sample 2"
    query_request = query.create_request(resource_type, user_query, config)

    assert query_request.query == "Resources | where type=~'{}' | sample 2".format(resource_type)
