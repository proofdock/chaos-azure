# Chaos Toolkit Extension for Azure

[![Build Status](https://dev.azure.com/proofdockio/chaos/_apis/build/status/chaos-azure/chaos-azure%20-%20production?branchName=master)](https://dev.azure.com/proofdockio/chaos/_build/latest?definitionId=60&branchName=master)
[![Python versions](https://img.shields.io/pypi/pyversions/proofdock-chaos-azure.svg)](https://www.python.org/)

This project is a collection of [actions][activities] and [probes][activities], gathered as an
extension to the [Chaos Toolkit][chaostoolkit]. It targets the [Microsoft Azure][azure] platform.

[activities]: https://docs.proofdock.io/chaos/experiments/azure/
[chaostoolkit]: http://chaostoolkit.org
[azure]: https://azure.microsoft.com/en-us/

## Install

This package requires Python 3.5+

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

```
$ pip install -U proofdock-chaos-azure
```

## Usage

To use the probes and actions from this package, add the following to your
experiment file:

```json
{
  "type": "action",
  "name": "start-chaos",
  "provider": {
    "type": "python",
    "module": "pdchaosazure.vm.actions",
    "func": "stop_machines",
    "secrets": ["azure"],
    "config": ["azure_subscription_id"]
  }
}
```

That's it!

Please explore the code to see existing probes and actions.

## Configuration

This extension uses the [Azure SDK][sdk] libraries under the hood. The Azure SDK library expects that you have a tenant and client identifier, as well as a client secret and subscription, that allows you to authenticate with the Azure resource management API.

Configuration values for the Chaos Toolkit Extension for Azure can come from several sources:

- Experiment file
- Azure credential file

The extension will first try to load the configuration from the `experiment file`. If configuration is not provided in the `experiment file`, it will try to load it from the `Azure credential file`.

[creds]: https://docs.microsoft.com/en-us/azure/service-fabric/service-fabric-connect-to-secure-cluster
[requests]: http://docs.python-requests.org/en/master/
[sdk]: https://github.com/Azure/azure-sdk-for-python

### Credentials

- Secrets in the Experiment file

  ```json
  {
    "secrets": {
      "azure": {
        "client_id": "your-super-secret-client-id",
        "client_secret": "your-even-more-super-secret-client-secret",
        "tenant_id": "your-tenant-id"
      }
    }
  }
  ```

  You can retrieve secretes as well from [environment][env_secrets] or [HashiCorp vault][vault_secrets]. 

  
  If you are not working with Public Global Azure, e.g. China Cloud You can set the cloud environment.

  ```json
  {
    "client_id": "your-super-secret-client-id",
    "client_secret": "your-even-more-super-secret-client-secret",
    "tenant_id": "your-tenant-id",
    "azure_cloud": "AZURE_CHINA_CLOUD"
  }
  ```

  Available cloud names:

  - AZURE_CHINA_CLOUD
  - AZURE_GERMAN_CLOUD
  - AZURE_PUBLIC_CLOUD
  - AZURE_US_GOV_CLOUD

  [vault_secrets]: https://docs.chaostoolkit.org/reference/api/experiment/#vault-secrets
  [env_secrets]: https://docs.chaostoolkit.org/reference/api/experiment/#environment-secrets


- Secrets in the Azure credential file

  You can retrieve a credentials file with your subscription ID already in place by signing in to Azure using the az login command followed by the az ad sp create-for-rbac command

  ```bash
  az login
  az ad sp create-for-rbac --sdk-auth > credentials.json
  ```

  credentials.json:

  ```json
  {
    "subscriptionId": "<azure_aubscription_id>",
    "tenantId": "<tenant_id>",
    "clientId": "<application_id>",
    "clientSecret": "<application_secret>",
    "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
    "resourceManagerEndpointUrl": "https://management.azure.com/",
    "activeDirectoryGraphResourceId": "https://graph.windows.net/",
    "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
    "galleryEndpointUrl": "https://gallery.azure.com/",
    "managementEndpointUrl": "https://management.core.windows.net/"
  }
  ```

  Store the path to the file in an environment variable called **AZURE_AUTH_LOCATION** and make sure that your experiment does **NOT** contain `secrets` section. 

### Subscription

Additionally you need to provide the Azure subscription id.

- Subscription id in the experiment file

  ```json
  {
    "configuration": {
      "azure_subscription_id": "your-azure-subscription-id"
    }
  }
  ```

  Configuration may be as well retrieved from an [environment][env_configuration].

  An old, but deprecated way of doing it was as follows, this still works
  but should not be favoured over the previous approaches as it's not the
  Chaos Toolkit way to pass structured configurations.

  ```json
  {
    "configuration": {
      "azure": {
        "subscription_id": "your-azure-subscription-id"
      }
    }
  }
  ```

  [env_configuration]: https://docs.chaostoolkit.org/reference/api/experiment/#environment-configurations

- Subscription id in the Azure credential file

  Credential file described in the previous "Credential" section contains as well subscription id. If **AZURE_AUTH_LOCATION** is set and subscription id is **NOT** set in the experiment definition, extension will try to load it from the credential file.

  

### Putting it all together

Here is a full example for an experiment containing secrets and configuration: 

```json
{
  "version": "1.0.0",
  "title": "...",
  "description": "...",
  "tags": ["azure", "kubernetes", "aks", "node"],
  "configuration": {
    "azure_subscription_id": "xxx"
  },
  "secrets": {
    "azure": {
      "client_id": "xxx",
      "client_secret": "xxx",
      "tenant_id": "xxx"
    }
  },
  "steady-state-hypothesis": {
    "title": "Services are all available and healthy",
    "probes": [
      {
        "type": "probe",
        "name": "consumer-service-must-still-respond",
        "tolerance": 200,
        "provider": {
          "type": "http",
          "url": "https://some-url/"
        }
      }
    ]
  },
  "method": [
    {
      "type": "action",
      "name": "restart-node-at-random",
      "provider": {
        "type": "python",
        "module": "pdchaosazure.machine.actions",
        "func": "restart_machines",
        "secrets": ["azure"],
        "config": ["azure_subscription_id"]
      }
    }
  ],
  "rollbacks": []
}
```

## Filter arguments

This extension is making heavy use of the [Kusto query language][kusto] to filter those Azure resources that an experiment is targeting.

The Kusto query language in Azure is a read-only request to process data and return results. The request is stated in plain text, using a data-flow model designed to make the syntax easy to read.

Given that an Azure subscription contains the following Azure resources:

```json
[
    {
        "name": "machine_1",
        "resourceGroup": "my_resource_group",
        "type": "Microsoft.Compute/virtualMachines"
    },
    {
        "name": "machine_2",
        "resourceGroup": "my_resource_group",
        "type": "Microsoft.Compute/virtualMachines"
    },
    {
        "name": "machine_1",
        "resourceGroup": "another_resource_group",
        "type": "Microsoft.Compute/virtualMachines"
    }
]
```

With a filter you can ultimatively select the Azure resources that shall be attacked. For example:
* ``where resourceGroup=='my_resource_group''`` will select those machines for an attack
  ```json
  [
      {
        "name": "machine_1",
        "resourceGroup": "my_resource_group",
        "type": "Microsoft.Compute/virtualMachines"
      },
      {
        "name": "machine_2",
        "resourceGroup": "my_resource_group",
        "type": "Microsoft.Compute/virtualMachines"
      }
  ]
  ```
* ``where name=='machine_1''`` will select those machines for an attack
  ```json
  [
      {
        "name": "machine_1",
        "resourceGroup": "my_resource_group",
        "type": "Microsoft.Compute/virtualMachines"
      },
      {
        "name": "machine_1",
        "resourceGroup": "another_resource_group",
        "type": "Microsoft.Compute/virtualMachines"
      }
  ]
  ```
* ``where name=='machine_1' and resourceGroup='my_resource_group''`` will select
  ```json
  [
      {
        "name": "machine_1",
        "resourceGroup": "my_resource_group",
        "type": "Microsoft.Compute/virtualMachines"
      }
  ]
* If you want to randomly select one machine of your resource group you may do the following operation: ``where resourceGroup='my_resource_group'' | sample 1``. The ``sample`` operator is generating randomness to your selection.
  ```json
  [
      {
        "name": "<one of your machines in the 'my_resource_group'>",
        "resourceGroup": "my_resource_group",
        "type": "Microsoft.Compute/virtualMachines"
      }
  ]
  ```
* If you omit the filter entirely one machine out your subscription (if any) is taken.

[kusto]: https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/

### Kusto Query Language Light

At some places in the chaos experiment API some Azure resources are not supported by Azure to be filtered with the Kusto Query Language. A very prominent example are instances of a virtual machine set such as Virtual Machine Scale Sets.

We anyhow decided to support you with an easy way of filtering for those resources as well with a Kusto Query Language Light (KQLL) syntax. The KQLL defines a small subset of the KQL from Azure but should serve the daily purposes of the chaos experiments.

The small subset defines:
* ``where``-clauses with ``and`` and ``or`` expressions
* pipe ``|`` operators
* ``take``, ``top``, and ``sample`` commands
* Equality operators such as ``==``, ``>=``, ``<=``, ``>``, and ``<``
* If you omit the KQLL filter one resource of the cluster is selected at random.
* Those queries that provide the KQLL syntax will be marked as such in the activity's documentation.

## Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please, fork this project, make your changes following the
usual [PEP 8][pep8] code style, sprinkling with tests and submit a PR for
review.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/

The Chaos Toolkit projects require all contributors must sign a
[Developer Certificate of Origin][dco] on each commit they would like to merge
into the master branch of the repository. Please, make sure you can abide by
the rules of the DCO before submitting a PR.

[dco]: https://github.com/probot/dco#how-it-works

### Develop

If you wish to develop on this project, make sure to install the development
dependencies. But first, [create a virtual environment][venv] and then install
those dependencies.

[venv]: http://chaostoolkit.org/reference/usage/install/#create-a-virtual-environment

```console
$ pip install -r requirements-dev.txt -r requirements.txt
```

Then, point your environment to this directory:

```console
$ python setup.py develop
```

Now, you can edit the files and they will be automatically be seen by your
environment, even when running from the `chaos` command locally.

### Test

To run the tests for the project execute the following:

```
$ pytest
```
