from msrestazure import azure_cloud

from pdchaosazure.common import cloud


def auth_file():
    return {
        "clientId": "AZURE_CLIENT_ID",
        "clientSecret": "AZURE_CLIENT_SECRET",
        "tenantId": "AZURE_TENANT_ID",
        "subscriptionId": "AZURE_SUBSCRIPTION_ID",
        "resourceManagerEndpointUrl": "https://management.azure.com/"
    }


def provide_secrets_via_service_principal():
    return {
        "client_id": "***",
        "client_secret": "***",
        "tenant_id": "***"
    }


def provide_secrets_china():
    result = provide_secrets_via_service_principal()
    result["azure_cloud"] = cloud.AZURE_CHINA_CLOUD
    return result


def provide_secrets_germany():
    result = provide_secrets_via_service_principal()
    result["azure_cloud"] = cloud.AZURE_GERMAN_CLOUD
    return result


def provide_secrets_germany_small_letters():
    result = provide_secrets_via_service_principal()
    result["azure_cloud"] = "azure_german_cloud"
    return result


def provide_secrets_us_gov():
    result = provide_secrets_via_service_principal()
    result["azure_cloud"] = cloud.AZURE_US_GOV_CLOUD
    return result


def provide_secrets_public():
    result = provide_secrets_via_service_principal()
    result["azure_cloud"] = cloud.AZURE_PUBLIC_CLOUD
    return result


def provide_secrets_via_token():
    return {
        "access_token": "***",
        "client_id": "***",
        "tenant_id": "***",
    }


def provide_secrets_invalid_cloud():
    result = provide_secrets_via_service_principal()
    result["azure_cloud"] = "this_cloud_does_not_exist"
    return result


def provide_violating_secrets():
    return {
        "client_id": "***",
        "tenant_id": "***",
        "client_secret": "***",
        "cloud": azure_cloud.AZURE_PUBLIC_CLOUD
    }
