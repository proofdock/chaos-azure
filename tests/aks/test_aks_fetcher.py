from unittest.mock import patch

import pytest
from chaoslib.exceptions import FailedActivity

from pdchaosazure.aks.fetcher import fetch_aks
from tests.data import aks_provider


@patch('pdchaosazure.aks.fetcher.fetch_resources', autospec=True)
def test_happy_fetch_aks(mocked_fetcher):
    aks = aks_provider.default()
    aks_list = [aks]
    mocked_fetcher.return_value = aks_list

    result = fetch_aks(None, None, None)

    assert len(result) == 1
    assert result[0].get('name') == 'chaos-aks'


@patch('pdchaosazure.aks.fetcher.fetch_resources', autospec=True)
def test_sad_empty_fetch_aks(mocked_fetcher):
    with pytest.raises(FailedActivity) as x:
        mocked_fetcher.return_value = []
        fetch_aks(None, None, None)

        assert "No AKS" in str(x.value)
