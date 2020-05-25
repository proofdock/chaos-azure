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
    "burn_io", "deallocate_instance", "delete_instance", "fill_disk", "network_latency",
    "restart_instance", "stop_instance", "stress_cpu"
]


def delete_instance(filter_vmss: str = None,
                    filter_instances: str = None,
                    configuration: Configuration = None,
                    secrets: Secrets = None):
    """
    Delete instances from the filtered scale sets either at random or by a defined instance filter.

    **Be aware**: Deleting a VMSS instance is an invasive action.
    You will not be able to recover the VMSS instance once you deleted it.

    Parameters
    ----------
    filter_vmss : str, optional
        Filter the virtual machine scale set(s).

    filter_instances : str, optional
        Filter the instances of the selected virtual machine scale set(s).
    """
    logger.debug(
        "Starting {}: configuration='{}', filter='{}'".format(delete_instance.__name__, configuration, filter_vmss))

    client = init_client(secrets, configuration)
    vmss_list = fetch_vmss(filter_vmss, configuration, secrets)
    vmss_records = Records()

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, filter_instances, client)

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


def restart_instance(filter_vmss: str = None,
                     filter_instances: str = None,
                     configuration: Configuration = None,
                     secrets: Secrets = None):
    """
    Restart instances from the filtered scale sets either at random or by a defined instance filter.

    Parameters
    ----------
    filter_vmss : str, optional
        Filter the virtual machine scale set(s).

    filter_instances : str, optional
        Filter the instances of the selected virtual machine scale set(s).
    """
    logger.debug(
        "Starting {}: configuration='{}', filter='{}'".format(restart_instance.__name__, configuration, filter_vmss))

    client = init_client(secrets, configuration)
    vmss_list = fetch_vmss(filter_vmss, configuration, secrets)
    vmss_records = Records()

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, filter_instances, client)

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


def stop_instance(filter_vmss: str = None,
                  filter_instances: str = None,
                  configuration: Configuration = None,
                  secrets: Secrets = None):
    """
    Stops instances from the filtered scale sets either at random or by a defined instance filter.

    Parameters
    ----------
    filter_vmss : str, optional
        Filter the virtual machine scale set(s).

    filter_instances : str, optional
        Filter the instances of the selected virtual machine scale set(s).
    """
    logger.debug(
        "Starting {}: configuration='{}', filter='{}'".format(stop_instance.__name__, configuration, filter_vmss))

    client = init_client(secrets, configuration)
    vmss_list = fetch_vmss(filter_vmss, configuration, secrets)
    vmss_records = Records()

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, filter_instances, client)

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


def deallocate_instance(filter_vmss: str = None,
                        filter_instances: str = None,
                        configuration: Configuration = None,
                        secrets: Secrets = None):
    """
    Deallocate instances from the filtered scale sets either at random or by a defined instance filter.

    Parameters
    ----------
    filter_vmss : str, optional
        Filter the virtual machine scale set(s).

    filter_instances : str, optional
        Filter the instances of the selected virtual machine scale set(s).
    """
    logger.debug(
        "Starting {}: configuration='{}', filter='{}'".format(deallocate_instance.__name__, configuration, filter_vmss))

    client = init_client(secrets, configuration)
    vmss_list = fetch_vmss(filter_vmss, configuration, secrets)
    vmss_records = Records()

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, filter_instances, client)

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


def stress_cpu(filter_vmss: str = None,
               filter_instances: str = None,
               duration: int = 120,
               configuration: Configuration = None,
               secrets: Secrets = None):
    """
    CPU stressing for instances from the filtered scale sets either at random or by a defined instance filter.

    Parameters
    ----------
    filter_vmss : str, optional
        Filter the virtual machine scale set(s).

    filter_instances : str, optional
        Filter the instances of the selected virtual machine scale set(s).

    duration : int, optional
        Duration of the stress test (in seconds) that generates high CPU usage. Defaults to 120 seconds.
    """
    logger.debug("Starting stress_vmss_instance_cpu: configuration='{}', filter='{}', duration='{}'".format(
        configuration, filter_vmss, duration))

    client = init_client(secrets, configuration)
    vmss_records = Records()
    vmss_list = fetch_vmss(filter_vmss, configuration, secrets)

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, filter_instances, client)

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


def burn_io(filter_vmss: str = None,
            filter_instances: str = None,
            duration: int = 60,
            configuration: Configuration = None,
            secrets: Secrets = None):
    """
    Simulate heavy disk I/O operations on instances from the filtered scale sets
    either at random or by a defined instance filter.

    Parameters
    ----------
    filter_vmss : str, optional
        Filter the virtual machine scale set(s).

    filter_instances : str, optional
        Filter the instances of the selected virtual machine scale set(s).

    duration : int, optional
        Duration of the stress test (in seconds) that generates high disk I/O operations. Defaults to 60 seconds.
    """
    logger.debug(
        "Starting burn_io: configuration='{}', filter='{}', duration='{}',".format(
            configuration, filter_vmss, duration))

    client = init_client(secrets, configuration)
    vmss_list = fetch_vmss(filter_vmss, configuration, secrets)
    vmss_records = Records()

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, filter_instances, client)

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


def fill_disk(filter_vmss: str = None,
              filter_instances: Iterable[Mapping[str, any]] = None,
              duration: int = 120,
              size: int = 1000,
              path: str = None,
              configuration: Configuration = None,
              secrets: Secrets = None):
    """
    Fill the disk with random data on instances from the filtered scale sets
    either at random or by a defined instance filter.

    Parameters
    ----------
    filter_vmss : str, optional
        Filter the virtual machine scale set(s).

    filter_instances : str, optional
        Filter the instances of the selected virtual machine scale set(s).

    duration : int, optional
        Duration of the stress test (in seconds) that generates random data on disk. Defaults to 120 seconds.

    size : int, optional
        Size of the stressing file that is generated in Megabytes. Defaults to 1000 MB.

    path : str, optional
        Location of the stressing file where it is generated. Defaults to ``/root/burn`` on Linux systems
        and ``C:/burn`` on Windows machines.
    """
    logger.debug(
        "Starting fill_disk: configuration='{}', filter='{}', duration='{}', size='{}', path='{}'".format(
            configuration, filter_vmss, duration, size, path))

    client = init_client(secrets, configuration)
    vmss_list = fetch_vmss(filter_vmss, configuration, secrets)
    vmss_records = Records()

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, filter_instances, client)

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


def network_latency(filter_vmss: str = None,
                    filter_instances: str = None,
                    duration: int = 60,
                    delay: int = 200,
                    jitter: int = 50,
                    configuration: Configuration = None,
                    secrets: Secrets = None):
    """
    Increases the response time on instances from the filtered scale sets
    either at random or by a defined instance filter.

    Parameters
    ----------
    filter_vmss : str, optional
        Filter the virtual machine scale set(s).

    filter_instances : str, optional
        Filter the instances of the selected virtual machine scale set(s).

    duration : int, optional
        Duration of the stress test (in seconds) that generates network latency. Defaults to 60 seconds.

    delay : int, optional
        Applied delay of the response time in milliseconds. Defaults to 200 milliseconds.

    jitter : int, optional
        Applied +/- jitter to the delay of the response time in milliseconds. Defaults to 50 milliseconds.
    """
    logger.debug(
        "Starting network_latency: configuration='{}', filter='{}', duration='{}', delay='{}', jitter='{}'".format(
            configuration, filter_vmss, duration, delay, jitter))

    client = init_client(secrets, configuration)
    vmss_list = fetch_vmss(filter_vmss, configuration, secrets)
    vmss_records = Records()

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, filter_instances, client)

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
