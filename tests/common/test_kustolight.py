import jmespath
import pytest

from pdchaosazure.common import kustolight
from tests.data import vmss_provider


def test_filter_successful_one_instance():
    instance_0 = vmss_provider.provide_instance_real_sample()
    instance_1 = vmss_provider.provide_instance_real_sample()
    instance_1['instance_id'] = '1'

    instances = [instance_0, instance_1]
    input_filter = "where instance_id=='0'"

    result = kustolight.filter_resources(instances, input_filter)

    assert len(result) == 1


def test_filter_successful_two_instances():
    instance_0 = vmss_provider.provide_instance_real_sample()
    instance_1 = vmss_provider.provide_instance_real_sample()
    instance_1['instance_id'] = '1'

    instances = [instance_0, instance_1]
    input_filter = "where instance_id=='0' or instance_id=='1'"

    result = kustolight.filter_resources(instances, input_filter)

    assert len(result) == 2


def test_filter_successful_one_instance_with_where_clause_and_sample_operator():
    instance_0 = vmss_provider.provide_instance_real_sample()
    instance_1 = vmss_provider.provide_instance_real_sample()
    instance_1['instance_id'] = '1'

    instances = [instance_0, instance_1]
    input_filter = "where instance_id=='0' or instance_id=='1' | sample 1"

    result = kustolight.filter_resources(instances, input_filter)

    assert len(result) == 1


def test_filter_successful_one_instance_with_sample_one():
    instance_0 = vmss_provider.provide_instance_real_sample()
    instance_1 = vmss_provider.provide_instance_real_sample()
    instance_1['instance_id'] = '1'

    instances = [instance_0, instance_1]
    input_filter = "sample 1"

    result = kustolight.filter_resources(instances, input_filter)

    assert len(result) == 1


def test_filter_violate_with_invalid_filter():
    instance_0 = vmss_provider.provide_instance_real_sample()
    instance_1 = vmss_provider.provide_instance_real_sample()
    instance_1['instance_id'] = '1'

    instances = [instance_0, instance_1]
    input_filter = "sam 1"

    with pytest.raises(jmespath.exceptions.ParseError):
        kustolight.filter_resources(instances, input_filter)
