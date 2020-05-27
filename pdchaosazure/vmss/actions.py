import concurrent
from typing import Iterable, Mapping

from chaoslib import Configuration, Secrets
from chaoslib.exceptions import FailedActivity
from logzero import logger
from msrestazure import azure_exceptions

from pdchaosazure.common import cleanse, config
from pdchaosazure.common.compute import command, init_client
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
    """Delete instances from the VMSS.

    **Be aware**: Deleting a VMSS instance is an invasive action.
    You will not be able to recover the VMSS instance once you deleted it.

    Parameters
    ----------
    filter_vmss : str, optional
        Filter the virtual machine scale set(s). If omitted a random VMSS from your subscription is selected.

    filter_instances : str, optional
        KQLL: Filter the instances of the selected virtual machine scale set(s). If omitted
        a random instance from your VMSS is selected.
    """
    logger.debug(
        "Starting {}: configuration='{}', filter='{}'".format(delete_instance.__name__, configuration, filter_vmss))

    client = init_client(secrets, configuration)
    vmss_list = fetch_vmss(filter_vmss, configuration, secrets)
    vmss_records = Records()

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, filter_instances, client)

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(instances)) as executor:
            for instance in instances:
                try:
                    poller = client.virtual_machine_scale_set_vms.delete(
                        vmss['resourceGroup'], vmss['name'], instance['instance_id'])
                except azure_exceptions.CloudError as e:
                    raise FailedActivity(e.message)

                executor.submit(
                    __long_poll, delete_instance.__name__, instance, poller, instances_records, configuration)

        vmss['virtualMachines'] = instances_records.output()
        vmss_records.add(cleanse.vmss(vmss))

    return vmss_records.output_as_dict('resources')


def restart_instance(filter_vmss: str = None,
                     filter_instances: str = None,
                     configuration: Configuration = None,
                     secrets: Secrets = None):
    """Restart instances from the VMSS.

    Parameters
    ----------
    filter_vmss : str, optional
        Filter the virtual machine scale set(s). If omitted a random VMSS from your subscription is selected.

    filter_instances : str, optional
        KQLL: Filter the instances of the selected virtual machine scale set(s). If omitted
        a random instance from your VMSS is selected.
    """
    logger.debug(
        "Starting {}: configuration='{}', filter_vmss='{}', filter_instances='{}'".format(
            restart_instance.__name__, configuration, filter_vmss, filter_instances))

    client = init_client(secrets, configuration)
    vmss_list = fetch_vmss(filter_vmss, configuration, secrets)
    vmss_records = Records()

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, filter_instances, client)

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(instances)) as executor:
            for instance in instances:
                try:
                    poller = client.virtual_machine_scale_set_vms.restart(vmss['resourceGroup'], vmss['name'],
                                                                          instance['instance_id'])
                except azure_exceptions.CloudError as e:
                    raise FailedActivity(e.message)

                executor.submit(
                    __long_poll, restart_instance.__name__, instance, poller, instances_records, configuration)

        vmss['virtualMachines'] = instances_records.output()
        vmss_records.add(cleanse.vmss(vmss))

    return vmss_records.output_as_dict('resources')


def stop_instance(filter_vmss: str = None,
                  filter_instances: str = None,
                  configuration: Configuration = None,
                  secrets: Secrets = None):
    """Stop instances from the VMSS.

    Parameters
    ----------
    filter_vmss : str, optional
        Filter the virtual machine scale set(s). If omitted a random VMSS from your subscription is selected.

    filter_instances : str, optional
        KQLL: Filter the instances of the selected virtual machine scale set(s). If omitted
        a random instance from your VMSS is selected.
    """
    logger.debug(
        "Starting {}: configuration='{}', filter_vmss='{}', filter_instances='{}'".format(
            stop_instance.__name__, configuration, filter_vmss, filter_instances))

    client = init_client(secrets, configuration)
    vmss_list = fetch_vmss(filter_vmss, configuration, secrets)
    vmss_records = Records()

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, filter_instances, client)

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(instances)) as executor:
            for instance in instances:
                try:
                    poller = client.virtual_machine_scale_set_vms.power_off(
                        vmss['resourceGroup'], vmss['name'], instance['instance_id'])
                except azure_exceptions.CloudError as e:
                    raise FailedActivity(e.message)

                executor.submit(
                    __long_poll, stop_instance.__name__, instance, poller, instances_records, configuration)

        vmss['virtualMachines'] = instances_records.output()
        vmss_records.add(cleanse.vmss(vmss))

    return vmss_records.output_as_dict('resources')


def deallocate_instance(filter_vmss: str = None,
                        filter_instances: str = None,
                        configuration: Configuration = None,
                        secrets: Secrets = None):
    """Deallocate instances from the VMSS.

    Parameters
    ----------
    filter_vmss : str, optional
        Filter the virtual machine scale set(s). If omitted a random VMSS from your subscription is selected.

    filter_instances : str, optional
        KQLL: Filter the instances of the selected virtual machine scale set(s). If omitted
        a random instance from your VMSS is selected.
    """
    logger.debug(
        "Starting {}: configuration='{}', filter_vmss='{}', filter_instances='{}'".format(
            deallocate_instance.__name__, configuration, filter_vmss, filter_instances))

    client = init_client(secrets, configuration)
    vmss_list = fetch_vmss(filter_vmss, configuration, secrets)
    vmss_records = Records()

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, filter_instances, client)

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(instances)) as executor:
            for instance in instances:
                logger.debug("Deallocating instance: {}".format(instance['name']))

                try:
                    poller = client.virtual_machine_scale_set_vms.deallocate(vmss['resourceGroup'], vmss['name'],
                                                                             instance['instance_id'])
                except azure_exceptions.CloudError as e:
                    raise FailedActivity(e.message)

                executor.submit(
                    __long_poll, deallocate_instance.__name__, instance, poller, instances_records, configuration)

        vmss['virtualMachines'] = instances_records.output()
        vmss_records.add(cleanse.vmss(vmss))

    return vmss_records.output_as_dict('resources')


def stress_cpu(filter_vmss: str = None,
               filter_instances: str = None,
               duration: int = 120,
               configuration: Configuration = None,
               secrets: Secrets = None):
    """Stress CPU up to 100% for instances from the VMSS.

    Parameters
    ----------
    filter_vmss : str, optional
        Filter the virtual machine scale set(s). If omitted a random VMSS from your subscription is selected.

    filter_instances : str, optional
        KQLL: Filter the instances of the selected virtual machine scale set(s). If omitted
        a random instance from your VMSS is selected.

    duration : int, optional
        Duration of the stress test (in seconds) that generates high CPU usage. Defaults to 120 seconds.
    """
    logger.debug("Starting {}: configuration='{}', filter_vmss='{}', filter_instances='{}', duration='{}'".format(
        stress_cpu.__name__, configuration, filter_vmss, filter_instances, duration))

    vmss_list = fetch_vmss(filter_vmss, configuration, secrets)
    client = init_client(secrets, configuration)

    vmss_records = Records()

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, filter_instances, client)

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(instances)) as executor:
            for instance in instances:
                command_id, script_content = command.prepare(instance, 'cpu_stress_test')
                parameters = {
                    'command_id': command_id,
                    'script': [script_content],
                    'parameters': [
                        {'name': "duration", 'value': duration}
                    ]
                }

                executor.submit(
                    __long_poll_command, stress_cpu.__name__,
                    vmss['resourceGroup'], instance, duration, parameters, instances_records, configuration, client)

        vmss['virtualMachines'] = instances_records.output()
        vmss_records.add(cleanse.vmss(vmss))

    return vmss_records.output_as_dict('resources')


def burn_io(filter_vmss: str = None,
            filter_instances: str = None,
            duration: int = 60,
            configuration: Configuration = None,
            secrets: Secrets = None):
    """Simulate heavy disk I/O operations.

    Parameters
    ----------
    filter_vmss : str, optional
        Filter the virtual machine scale set(s). If omitted a random VMSS from your subscription is selected.

    filter_instances : str, optional
        KQLL: Filter the instances of the selected virtual machine scale set(s). If omitted
        a random instance from your VMSS is selected.

    duration : int, optional
        Duration of the stress test (in seconds) that generates high disk I/O operations. Defaults to 60 seconds.
    """
    logger.debug(
        "Starting {}: configuration='{}', filter_vmss='{}', filter_instances='{}', duration='{}',".format(
            burn_io.__name__, configuration, filter_vmss, filter_instances, duration))

    client = init_client(secrets, configuration)
    vmss_list = fetch_vmss(filter_vmss, configuration, secrets)
    vmss_records = Records()

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, filter_instances, client)

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(instances)) as executor:
            for instance in instances:
                command_id, script_content = command.prepare(instance, 'burn_io')
                parameters = {
                    'command_id': command_id,
                    'script': [script_content],
                    'parameters': [
                        {'name': "duration", 'value': duration}
                    ]
                }

                executor.submit(
                    __long_poll_command, burn_io.__name__,
                    vmss['resourceGroup'], instance, duration, parameters, instances_records, configuration, client)

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
    """Fill the disk with random data.

    Parameters
    ----------
    filter_vmss : str, optional
        Filter the virtual machine scale set(s). If omitted a random VMSS from your subscription is selected.

    filter_instances : str, optional
        KQLL: Filter the instances of the selected virtual machine scale set(s). If omitted
        a random instance from your VMSS is selected.

    duration : int, optional
        Duration of the stress test (in seconds) that generates random data on disk. Defaults to 120 seconds.

    size : int, optional
        Size of the stressing file that is generated in Megabytes. Defaults to 1000 MB.

    path : str, optional
        Location of the stressing file where it is generated. Defaults to ``/root/burn`` on Linux systems
        and ``C:/burn`` on Windows machines.
    """
    logger.debug(
        "Starting {}: configuration='{}', filter_vmss='{}', filter_instances='{}', "
        "duration='{}', size='{}', path='{}'".format(
            fill_disk.__name__, configuration, filter_vmss, filter_instances, duration, size, path))

    vmss_list = fetch_vmss(filter_vmss, configuration, secrets)
    client = init_client(secrets, configuration)

    vmss_records = Records()

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, filter_instances, client)

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(instances)) as executor:
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

                executor.submit(
                    __long_poll_command, fill_disk.__name__,
                    vmss['resourceGroup'], instance, duration, parameters, instances_records, configuration, client)

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
    """Increase the response time on instances.

    Parameters
    ----------
    filter_vmss : str, optional
        Filter the virtual machine scale set(s). If omitted a random VMSS from your subscription is selected.

    filter_instances : str, optional
        KQLL: Filter the instances of the selected virtual machine scale set(s). If omitted
        a random instance from your VMSS is selected.

    duration : int, optional
        Duration of the stress test (in seconds) that generates network latency. Defaults to 60 seconds.

    delay : int, optional
        Applied delay of the response time in milliseconds. Defaults to 200 milliseconds.

    jitter : int, optional
        Applied +/- jitter to the delay of the response time in milliseconds. Defaults to 50 milliseconds.
    """
    logger.debug(
        "Starting {}: configuration='{}', filter_vmss='{}', filter_instances='{}', "
        "duration='{}', delay='{}', jitter='{}'".format(
            network_latency.__name__, configuration, filter_vmss, filter_instances, duration, delay, jitter))

    vmss_list = fetch_vmss(filter_vmss, configuration, secrets)
    client = init_client(secrets, configuration)

    vmss_records = Records()

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, filter_instances, client)

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(instances)) as executor:
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

                command.run(vmss['resourceGroup'], instance, duration, parameters, client)
                instances_records.add(cleanse.vmss_instance(instance))

                executor.submit(
                    __long_poll_command, network_latency.__name__,
                    vmss['resourceGroup'], instance, duration, parameters, instances_records, configuration, client)

        vmss['virtualMachines'] = instances_records.output()
        vmss_records.add(cleanse.vmss(vmss))

    return vmss_records.output_as_dict('resources')


###########################
#  PRIVATE HELPER FUNCTIONS
###########################
def __long_poll(activity, instance, poller, records, configuration):
    logger.debug("Waiting for operation '{}' on instance '{}' to finish. Giving priority to other operations.".format(
        activity, instance['name']))
    poller.result(config.load_timeout(configuration))
    records.add(cleanse.vmss_instance(instance))
    logger.debug("Finished operation '{}' on instance '{}'.".format(activity, instance['name']))


def __long_poll_command(activity, group, instance, duration, parameters, records, configuration, client):
    logger.debug("Waiting for operation '{}' on instance '{}' to finish. Giving priority to other operations.".format(
        activity, instance['name']))
    timeout = config.load_timeout(configuration) + duration
    command.run(group, instance, timeout, parameters, client)
    records.add(cleanse.vmss_instance(instance))
    logger.debug("Finished operation '{}' on instance '{}'.".format(activity, instance['name']))
