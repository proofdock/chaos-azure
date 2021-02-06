import pytest
from chaoslib.exceptions import InterruptExecution

from pdchaosazure.auth import auth
from tests.data import secrets_provider


def test_violate_authentication_type():
    secrets = secrets_provider.provide_violating_secrets()

    with pytest.raises(InterruptExecution) as _:
        with auth(secrets) as _:
            pass
