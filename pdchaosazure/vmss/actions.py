from typing import Iterable, Mapping

from chaoslib import Configuration, Secrets
from chaoslib.exceptions import FailedActivity
from logzero import logger
from msrestazure import azure_exceptions

from pdchaosazure import init_client
from pdchaosazure.common import cleanse, config
from pdchaosazure.common.compute import command
from pdchaosazure.vmss.fetcher import fetch_vmss, fetch_instances
from pdchaosazure.vmss.records import Records

__all__ = [
    "delete_instance", "restart_instance", "stop_instance", "deallocate_instance",
    "burn_io", "fill_disk", "network_latency", "stress_cpu"
]


def delete_instance(filter: str = None,
                    instance_criteria: Iterable[Mapping[str, any]] = None,
                    configuration: Configuration = None,
                    secrets: Secrets = None):
    """
    Delete a virtual machine scale set instance at random.

    **Be aware**: Deleting a VMSS instance is an invasive action. You will not
    be able to recover the VMSS instance once you deleted it.

     Parameters
    ----------
    filter : str
        Filter the virtual machine scale set. If the filter is omitted all
        virtual machine scale sets in the subscription will be selected as
        potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Starting {}: configuration='{}', filter='{}'".format(delete_instance.__name__, configuration, filter))

    client = init_client(secrets, configuration)
    vmss_list = fetch_vmss(filter, configuration, secrets)
    vmss_records = Records()

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, instance_criteria, client)

        for instance in instances:
            logger.debug("Deleting instance: {}".format(instance['name']))

            try:
                poller = client.virtual_machine_scale_set_vms.delete(
                    vmss['resourceGroup'], vmss['name'], instance['instance_id'])

            except azure_exceptions.CloudError as e:
                raise FailedActivity(e.message)

            poller.result(config.load_timeout(configuration))
            instances_records.add(cleanse.vmss_instance(instance))

        vmss['virtualMachines'] = instances_records.output()
        vmss_records.add(cleanse.vmss(vmss))

    return vmss_records.output_as_dict('resources')


def restart_instance(filter: str = None,
                     instance_criteria: Iterable[Mapping[str, any]] = None,
                     configuration: Configuration = None,
                     secrets: Secrets = None):
    """
    Restart a virtual machine scale set instance at random.
     Parameters
    ----------
    filter : str
        Filter the virtual machine scale set. If the filter is omitted all
        virtual machine scale sets in the subscription will be selected as
        potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Starting {}: configuration='{}', filter='{}'".format(restart_instance.__name__, configuration, filter))

    client = init_client(secrets, configuration)
    vmss_list = fetch_vmss(filter, configuration, secrets)
    vmss_records = Records()

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, instance_criteria, client)

        for instance in instances:
            logger.debug("Restarting instance: {}".format(instance['name']))

            try:
                poller = client.virtual_machine_scale_set_vms.restart(vmss['resourceGroup'], vmss['name'],
                                                                      instance['instance_id'])

            except azure_exceptions.CloudError as e:
                raise FailedActivity(e.message)

            poller.result(config.load_timeout(configuration))
            instances_records.add(cleanse.vmss_instance(instance))

        vmss['virtualMachines'] = instances_records.output()
        vmss_records.add(cleanse.vmss(vmss))

    return vmss_records.output_as_dict('resources')


def stop_instance(filter: str = None,
                  instance_criteria: Iterable[Mapping[str, any]] = None,
                  configuration: Configuration = None,
                  secrets: Secrets = None):
    """
    Stops instances from the filtered scale set either at random or by
     a defined instance criteria.
     Parameters
    ----------
    filter : str
        Filter the virtual machine scale set. If the filter is omitted all
        virtual machine scale sets in the subscription will be selected as
        potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    instance_criteria :  Iterable[Mapping[str, any]]
        Allows specification of criteria for selection of a given virtual
        machine scale set instance. If the instance_criteria is omitted,
        an instance will be chosen at random. All of the criteria within each
        item of the Iterable must match, i.e. AND logic is applied.
        The first item with all matching criterion will be used to select the
        instance.
        Criteria example:
        [
         {"name": "myVMSSInstance1"},
         {
          "name": "myVMSSInstance2",
          "instanceId": "2"
         }
         {"instanceId": "3"},
        ]
        If the instances include two items. One with name = myVMSSInstance4
        and instanceId = 2. The other with name = myVMSSInstance2 and
        instanceId = 3. The criteria {"instanceId": "3"} will be the first
        match since both the name and the instanceId did not match on the
        first criteria.
    """
    logger.debug(
        "Starting {}: configuration='{}', filter='{}'".format(stop_instance.__name__, configuration, filter))

    client = init_client(secrets, configuration)
    vmss_list = fetch_vmss(filter, configuration, secrets)
    vmss_records = Records()

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, instance_criteria, client)

        for instance in instances:
            logger.debug("Stopping instance: {}".format(instance['name']))
            try:
                poller = client.virtual_machine_scale_set_vms.power_off(vmss['resourceGroup'], vmss['name'],
                                                                        instance['instance_id'])

            except azure_exceptions.CloudError as e:
                raise FailedActivity(e.message)

            poller.result(config.load_timeout(configuration))
            instances_records.add(cleanse.vmss_instance(instance))

        vmss['virtualMachines'] = instances_records.output()
        vmss_records.add(cleanse.vmss(vmss))

    return vmss_records.output_as_dict('resources')


def deallocate_instance(filter: str = None,
                        instance_criteria: Iterable[Mapping[str, any]] = None,
                        configuration: Configuration = None,
                        secrets: Secrets = None):
    """
    Deallocate a virtual machine scale set instance at random.
     Parameters
    ----------
    filter : str
        Filter the virtual machine scale set. If the filter is omitted all
        virtual machine scale sets in the subscription will be selected as
        potential chaos candidates.
        Filtering example:
        'where resourceGroup=="myresourcegroup" and name="myresourcename"'
    """
    logger.debug(
        "Starting {}: configuration='{}', filter='{}'".format(deallocate_instance.__name__, configuration, filter))

    client = init_client(secrets, configuration)
    vmss_list = fetch_vmss(filter, configuration, secrets)
    vmss_records = Records()

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, instance_criteria, client)

        for instance in instances:
            logger.debug("Deallocating instance: {}".format(instance['name']))

            try:
                poller = client.virtual_machine_scale_set_vms.deallocate(vmss['resourceGroup'], vmss['name'],
                                                                         instance['instance_id'])

            except azure_exceptions.CloudError as e:
                raise FailedActivity(e.message)

            poller.result(config.load_timeout(configuration))
            instances_records.add(cleanse.vmss_instance(instance))

        vmss['virtualMachines'] = instances_records.output()
        vmss_records.add(cleanse.vmss(vmss))

    return vmss_records.output_as_dict('resources')


def stress_cpu(filter: str = None,
               duration: int = 120,
               instance_criteria: Iterable[Mapping[str, any]] = None,
               configuration: Configuration = None,
               secrets: Secrets = None):
    """
    Stresses the CPU of a random VMSS instances in your selected VMSS.
    Similar to the stress_cpu action of the machine.actions module.

    Parameters
    ----------
    filter : str, optional
        Filter the VMSS. If the filter is omitted all VMSS in
        the subscription will be selected as potential chaos candidates.
    duration : int, optional
        Duration of the stress test (in seconds) that generates high CPU usage.
        Defaults to 120 seconds.
    """
    logger.debug("Starting stress_vmss_instance_cpu: configuration='{}', filter='{}', duration='{}'".format(
        configuration, filter, duration))

    client = init_client(secrets, configuration)
    vmss_records = Records()
    vmss_list = fetch_vmss(filter, configuration, secrets)

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, instance_criteria, client)

        for instance in instances:
            command_id, script_content = command.prepare(instance, 'cpu_stress_test')
            parameters = {
                'command_id': command_id,
                'script': [script_content],
                'parameters': [
                    {'name': "duration", 'value': duration}
                ]
            }

            logger.debug("Executing operation '{}' on instance: '{}'".format(stress_cpu.__name__, instance['name']))
            command.run(vmss['resourceGroup'], instance, duration, parameters, secrets, configuration)
            instances_records.add(cleanse.vmss_instance(instance))

        vmss['virtualMachines'] = instances_records.output()
        vmss_records.add(cleanse.vmss(vmss))

    return vmss_records.output_as_dict('resources')


def burn_io(filter: str = None,
            duration: int = 60,
            instance_criteria: Iterable[Mapping[str, any]] = None,
            configuration: Configuration = None,
            secrets: Secrets = None):
    """
    Increases the Disk I/O operations per second of the VMSS machine.
    Similar to the burn_io action of the machine.actions module.
    """
    logger.debug(
        "Starting burn_io: configuration='{}', filter='{}', duration='{}',".format(configuration, filter, duration))

    client = init_client(secrets, configuration)
    vmss_list = fetch_vmss(filter, configuration, secrets)
    vmss_records = Records()

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, instance_criteria, client)

        for instance in instances:
            command_id, script_content = command.prepare(instance, 'burn_io')
            parameters = {
                'command_id': command_id,
                'script': [script_content],
                'parameters': [
                    {'name': "duration", 'value': duration}
                ]
            }

            logger.debug("Executing operation '{}' on instance: '{}'".format(burn_io.__name__, instance['name']))
            command.run(vmss['resourceGroup'], instance, duration, parameters, secrets, configuration)
            instances_records.add(cleanse.vmss_instance(instance))

        vmss['virtualMachines'] = instances_records.output()
        vmss_records.add(cleanse.vmss(vmss))

    return vmss_records.output_as_dict('resources')


def fill_disk(filter: str = None,
              duration: int = 120,
              size: int = 1000,
              path: str = None,
              instance_criteria: Iterable[Mapping[str, any]] = None,
              configuration: Configuration = None,
              secrets: Secrets = None):
    """
    Fill the VMSS machine disk with random data. Similar to
    the fill_disk action of the machine.actions module.
    """
    logger.debug(
        "Starting fill_disk: configuration='{}', filter='{}', duration='{}', size='{}', path='{}'".format(
            configuration, filter, duration, size, path))

    client = init_client(secrets, configuration)
    vmss_list = fetch_vmss(filter, configuration, secrets)
    vmss_records = Records()

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, instance_criteria, client)

        for instance in instances:
            command_id, script_content = command.prepare(instance, 'fill_disk')
            fill_path = command.prepare_path(instance, path)

            parameters = {
                'command_id': command_id,
                'script': [script_content],
                'parameters': [
                    {'name': "duration", 'value': duration},
                    {'name': "size", 'value': size},
                    {'name': "path", 'value': fill_path}
                ]
            }

            logger.debug("Executing operation '{}' on instance: '{}'".format(fill_disk.__name__, instance['name']))
            command.run(vmss['resourceGroup'], instance, duration, parameters, secrets, configuration)
            instances_records.add(cleanse.vmss_instance(instance))

        vmss['virtualMachines'] = instances_records.output()
        vmss_records.add(cleanse.vmss(vmss))

    return vmss_records.output_as_dict('resources')


def network_latency(filter: str = None,
                    duration: int = 60,
                    delay: int = 200,
                    jitter: int = 50,
                    instance_criteria: Iterable[Mapping[str, any]] = None,
                    configuration: Configuration = None,
                    secrets: Secrets = None):
    """
    Increases the response time of the virtual machine. Similar to
    the network_latency action of the machine.actions module.
    """
    logger.debug(
        "Starting network_latency: configuration='{}', filter='{}', duration='{}', delay='{}', jitter='{}'".format(
            configuration, filter, duration, delay, jitter))

    client = init_client(secrets, configuration)
    vmss_list = fetch_vmss(filter, configuration, secrets)
    vmss_records = Records()

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, instance_criteria, client)

        for instance in instances:
            command_id, script_content = command.prepare(instance, 'network_latency')
            parameters = {
                'command_id': command_id,
                'script': [script_content],
                'parameters': [
                    {'name': "duration", 'value': duration},
                    {'name': "delay", 'value': delay},
                    {'name': "jitter", 'value': jitter}
                ]
            }

            logger.debug(
                "Executing operation '{}' on instance: '{}'".format(network_latency.__name__, instance['name']))
            command.run(vmss['resourceGroup'], instance, duration, parameters, secrets, configuration)
            instances_records.add(cleanse.vmss_instance(instance))

        vmss['virtualMachines'] = instances_records.output()
        vmss_records.add(cleanse.vmss(vmss))

    return vmss_records.output_as_dict('resources')
