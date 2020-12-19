import concurrent.futures
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
    "burn_io", "deallocate", "delete", "fill_disk", "network_latency",
    "restart", "stop", "stress_cpu"
]


def delete(vmss_filter: str = None,
           instance_filter: str = None,
           configuration: Configuration = None,
           secrets: Secrets = None):
    """Delete instances from the VMSS.

    **Be aware**: Deleting a VMSS instance is an invasive action.
    You will not be able to recover the VMSS instance once you deleted it.

    Parameters
    ----------
    vmss_filter : str, optional
        Filter the virtual machine scale set(s). If omitted a random VMSS from your subscription is selected.

    instance_filter : str, optional
        KQLL: Filter the instances of the selected virtual machine scale set(s). If omitted
        a random instance from your VMSS is selected.
    """
    logger.debug(
        "Starting {}: configuration='{}', filter='{}'".format(delete.__name__, configuration, vmss_filter))

    client = init_client(secrets, configuration)
    vmss_list = fetch_vmss(vmss_filter, configuration, secrets)
    vmss_records = Records()

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, instance_filter, client)

        futures = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(instances)) as executor:
            for instance in instances:
                try:
                    poller = client.virtual_machine_scale_set_vms.delete(
                        vmss['resourceGroup'], vmss['name'], instance['instance_id'])
                except azure_exceptions.CloudError as e:
                    raise FailedActivity(e.message)

                # collect future results
                futures.append(
                    executor.submit(__long_poll, delete.__name__, instance, poller, configuration))

            # wait for results
            for future in concurrent.futures.as_completed(futures):
                affected_instance = future.result()
                instances_records.add(cleanse.vmss_instance(affected_instance))

        vmss['virtualMachines'] = instances_records.output()
        vmss_records.add(cleanse.vmss(vmss))

    return vmss_records.output_as_dict('resources')


def restart(vmss_filter: str = None,
            instance_filter: str = None,
            configuration: Configuration = None,
            secrets: Secrets = None):
    """Restart instances from the VMSS.

    Parameters
    ----------
    vmss_filter : str, optional
        Filter the virtual machine scale set(s). If omitted a random VMSS from your subscription is selected.

    instance_filter : str, optional
        KQLL: Filter the instances of the selected virtual machine scale set(s). If omitted
        a random instance from your VMSS is selected.
    """
    logger.debug(
        "Starting {}: configuration='{}', vmss_filter='{}', instance_filter='{}'".format(
            restart.__name__, configuration, vmss_filter, instance_filter))

    client = init_client(secrets, configuration)
    vmss_list = fetch_vmss(vmss_filter, configuration, secrets)
    vmss_records = Records()

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, instance_filter, client)

        futures = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(instances)) as executor:
            for instance in instances:
                try:
                    poller = client.virtual_machine_scale_set_vms.restart(
                        vmss['resourceGroup'], vmss['name'], instance['instance_id'])
                except azure_exceptions.CloudError as e:
                    raise FailedActivity(e.message)

                # collect future results
                futures.append(
                    executor.submit(__long_poll, restart.__name__, instance, poller, configuration))

            # wait for results
            for future in concurrent.futures.as_completed(futures):
                affected_instance = future.result()
                instances_records.add(cleanse.vmss_instance(affected_instance))

        vmss['virtualMachines'] = instances_records.output()
        vmss_records.add(cleanse.vmss(vmss))

    return vmss_records.output_as_dict('resources')


def stop(vmss_filter: str = None,
         instance_filter: str = None,
         configuration: Configuration = None,
         secrets: Secrets = None):
    """Stop instances from the VMSS.

    Parameters
    ----------
    vmss_filter : str, optional
        Filter the virtual machine scale set(s). If omitted a random VMSS from your subscription is selected.

    instance_filter : str, optional
        KQLL: Filter the instances of the selected virtual machine scale set(s). If omitted
        a random instance from your VMSS is selected.
    """
    logger.debug(
        "Starting {}: configuration='{}', vmss_filter='{}', instance_filter='{}'".format(
            stop.__name__, configuration, vmss_filter, instance_filter))

    client = init_client(secrets, configuration)
    vmss_list = fetch_vmss(vmss_filter, configuration, secrets)
    vmss_records = Records()

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, instance_filter, client)

        futures = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(instances)) as executor:
            for instance in instances:
                try:
                    poller = client.virtual_machine_scale_set_vms.power_off(
                        vmss['resourceGroup'], vmss['name'], instance['instance_id'])
                except azure_exceptions.CloudError as e:
                    raise FailedActivity(e.message)

                # collect future results
                futures.append(
                    executor.submit(__long_poll, stop.__name__, instance, poller, configuration))

            # wait for results
            for future in concurrent.futures.as_completed(futures):
                affected_instance = future.result()
                instances_records.add(cleanse.vmss_instance(affected_instance))

        vmss['virtualMachines'] = instances_records.output()
        vmss_records.add(cleanse.vmss(vmss))

    return vmss_records.output_as_dict('resources')


def deallocate(vmss_filter: str = None,
               instance_filter: str = None,
               configuration: Configuration = None,
               secrets: Secrets = None):
    """Deallocate instances from the VMSS.

    Parameters
    ----------
    vmss_filter : str, optional
        Filter the virtual machine scale set(s). If omitted a random VMSS from your subscription is selected.

    instance_filter : str, optional
        KQLL: Filter the instances of the selected virtual machine scale set(s). If omitted
        a random instance from your VMSS is selected.
    """
    logger.debug(
        "Starting {}: configuration='{}', vmss_filter='{}', instance_filter='{}'".format(
            deallocate.__name__, configuration, vmss_filter, instance_filter))

    client = init_client(secrets, configuration)
    vmss_list = fetch_vmss(vmss_filter, configuration, secrets)
    vmss_records = Records()

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, instance_filter, client)

        futures = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(instances)) as executor:
            for instance in instances:
                logger.debug("Deallocating instance: {}".format(instance['name']))

                try:
                    poller = client.virtual_machine_scale_set_vms.deallocate(
                        vmss['resourceGroup'], vmss['name'], instance['instance_id'])
                except azure_exceptions.CloudError as e:
                    raise FailedActivity(e.message)

                # collect future results
                futures.append(
                    executor.submit(
                        __long_poll, deallocate.__name__, instance, poller, configuration))

            # wait for results
            for future in concurrent.futures.as_completed(futures):
                affected_instance = future.result()
                instances_records.add(cleanse.vmss_instance(affected_instance))

        vmss['virtualMachines'] = instances_records.output()
        vmss_records.add(cleanse.vmss(vmss))

    return vmss_records.output_as_dict('resources')


def stress_cpu(vmss_filter: str = None,
               instance_filter: str = None,
               duration: int = 120,
               configuration: Configuration = None,
               secrets: Secrets = None):
    """Stress CPU up to 100% for instances from the VMSS.

    Parameters
    ----------
    vmss_filter : str, optional
        Filter the virtual machine scale set(s). If omitted a random VMSS from your subscription is selected.

    instance_filter : str, optional
        KQLL: Filter the instances of the selected virtual machine scale set(s). If omitted
        a random instance from your VMSS is selected.

    duration : int, optional
        Duration of the stress test (in seconds) that generates high CPU usage. Defaults to 120 seconds.
    """

    operation_name = stress_cpu.__name__

    logger.debug("Starting {}: configuration='{}', vmss_filter='{}', instance_filter='{}', duration='{}'".format(
        operation_name, configuration, vmss_filter, instance_filter, duration))

    vmss_list = fetch_vmss(vmss_filter, configuration, secrets)
    client = init_client(secrets, configuration)

    vmss_records = Records()

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, instance_filter, client)

        futures = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(instances)) as executor:
            for instance in instances:
                command_id, script_content = command.prepare(instance, operation_name)
                parameters = command.fill_parameters(command_id, script_content, duration=duration)

                # collect future results
                futures.append(
                    executor.submit(
                        __long_poll_command, operation_name, vmss['resourceGroup'], instance, duration, parameters,
                        configuration, client))

            # wait for future results
            for future in concurrent.futures.as_completed(futures):
                affected_instance = future.result()
                instances_records.add(cleanse.vmss_instance(affected_instance))

        vmss['virtualMachines'] = instances_records.output()
        vmss_records.add(cleanse.vmss(vmss))

    return vmss_records.output_as_dict('resources')


def burn_io(vmss_filter: str = None,
            instance_filter: str = None,
            duration: int = 60,
            path: str = None,
            configuration: Configuration = None,
            secrets: Secrets = None):
    """Simulate heavy disk I/O operations.

    Parameters
    ----------
    vmss_filter : str, optional
        Filter the virtual machine scale set(s). If omitted a random VMSS from your subscription is selected.

    instance_filter : str, optional
        KQLL: Filter the instances of the selected virtual machine scale set(s). If omitted
        a random instance from your VMSS is selected.

    duration : int, optional
        Duration of the stress test (in seconds) that generates high disk I/O operations. Defaults to 60 seconds.

    path : str, optional
        The absolute path to write the stress file into. Defaults to ``C:\\burn`` for Windows
        clients and ``/root/burn`` for Linux clients.
    """
    operation_name = burn_io.__name__
    logger.debug(
        "Starting {}: configuration='{}', vmss_filter='{}', instance_filter='{}', duration='{}',".format(
            operation_name, configuration, vmss_filter, instance_filter, duration))

    client = init_client(secrets, configuration)
    vmss_list = fetch_vmss(vmss_filter, configuration, secrets)
    vmss_records = Records()

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, instance_filter, client)

        futures = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(instances)) as executor:
            for instance in instances:
                command_id, script_content = command.prepare(instance, operation_name)
                fill_path = command.prepare_path(instance, path)
                parameters = command.fill_parameters(command_id, script_content, duration=duration, path=fill_path)

                # collect future results
                futures.append(
                    executor.submit(
                        __long_poll_command, operation_name, vmss['resourceGroup'], instance, duration, parameters,
                        configuration, client))

            # wait for the results
            for future in concurrent.futures.as_completed(futures):
                affected_instance = future.result()
                instances_records.add(cleanse.vmss_instance(affected_instance))

        vmss['virtualMachines'] = instances_records.output()
        vmss_records.add(cleanse.vmss(vmss))

    return vmss_records.output_as_dict('resources')


def fill_disk(vmss_filter: str = None,
              instance_filter: Iterable[Mapping[str, any]] = None,
              duration: int = 120,
              size: int = 1000,
              path: str = None,
              configuration: Configuration = None,
              secrets: Secrets = None):
    """Fill the disk with random data.

    Parameters
    ----------
    vmss_filter : str, optional
        Filter the virtual machine scale set(s). If omitted a random VMSS from your subscription is selected.

    instance_filter : str, optional
        KQLL: Filter the instances of the selected virtual machine scale set(s). If omitted
        a random instance from your VMSS is selected.

    duration : int, optional
        Duration of the stress test (in seconds) that generates random data on disk. Defaults to 120 seconds.

    size : int, optional
        Size of the stressing file that is generated in Megabytes. Defaults to 1000 MB.

    path : str, optional
        Location of the stressing file where it is generated. Defaults to ``/root/burn`` on Linux systems
        and ``C:\\burn`` on Windows machines.
    """
    operation_name = fill_disk.__name__

    logger.debug(
        "Starting {}: configuration='{}', vmss_filter='{}', instance_filter='{}', "
        "duration='{}', size='{}', path='{}'".format(
            operation_name, configuration, vmss_filter, instance_filter, duration, size, path))

    vmss_list = fetch_vmss(vmss_filter, configuration, secrets)
    client = init_client(secrets, configuration)

    vmss_records = Records()

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, instance_filter, client)

        futures = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(instances)) as executor:
            for instance in instances:
                command_id, script_content = command.prepare(instance, operation_name)
                fill_path = command.prepare_path(instance, path)
                parameters = command.fill_parameters(
                    command_id, script_content, duration=duration, size=size, path=fill_path)

                # collect the future results
                futures.append(
                    executor.submit(
                        __long_poll_command, operation_name, vmss['resourceGroup'], instance, duration, parameters,
                        configuration, client))

            # wait for the results
            for future in concurrent.futures.as_completed(futures):
                affected_instance = future.result()
                instances_records.add(cleanse.vmss_instance(affected_instance))

        vmss['virtualMachines'] = instances_records.output()
        vmss_records.add(cleanse.vmss(vmss))

    return vmss_records.output_as_dict('resources')


def network_latency(vmss_filter: str = None,
                    instance_filter: str = None,
                    duration: int = 60,
                    delay: int = 200,
                    jitter: int = 50,
                    network_interface: str = "eth0",
                    configuration: Configuration = None,
                    secrets: Secrets = None):
    """Increase the response time on instances.

    **Please note**: This action is available only for Linux-based systems.

    Parameters
    ----------
    vmss_filter : str, optional
        Filter the virtual machine scale set(s). If omitted a random VMSS from your subscription is selected.

    instance_filter : str, optional
        KQLL: Filter the instances of the selected virtual machine scale set(s). If omitted
        a random instance from your VMSS is selected.

    duration : int, optional
        Duration of the stress test (in seconds) that generates network latency. Defaults to 60 seconds.

    delay : int, optional
        Applied delay of the response time in milliseconds. Defaults to 200 milliseconds.

    jitter : int, optional
        Applied variance of +/- jitter to the delay of the response time in milliseconds. Defaults to 50 milliseconds.

    network_interface : str, optional
        The network interface where the network latency is applied to. Defaults to local ethernet eth0.
    """
    operation_name = network_latency.__name__
    logger.debug(
        "Starting {}: configuration='{}', filter='{}', duration='{}',"
        " delay='{}', jitter='{}', network_interface='{}'".format(
            operation_name, configuration, filter, duration, delay, jitter, network_interface))

    vmss_list = fetch_vmss(vmss_filter, configuration, secrets)
    client = init_client(secrets, configuration)

    vmss_records = Records()

    for vmss in vmss_list:
        instances_records = Records()
        instances = fetch_instances(vmss, instance_filter, client)

        futures = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(instances)) as executor:
            for instance in instances:
                command_id, script_content = command.prepare(instance, operation_name)
                parameters = command.fill_parameters(
                    command_id, script_content, duration=duration, delay=delay, jitter=jitter,
                    network_interface=network_interface)

                # collect the future results
                futures.append(
                    executor.submit(
                        __long_poll_command, operation_name, vmss['resourceGroup'], instance, duration,
                        parameters, configuration, client))

            # wait for the results
            for future in concurrent.futures.as_completed(futures):
                affected_instance = future.result()
                instances_records.add(cleanse.vmss_instance(affected_instance))

        vmss['virtualMachines'] = instances_records.output()
        vmss_records.add(cleanse.vmss(vmss))

    return vmss_records.output_as_dict('resources')


###########################
#  PRIVATE HELPER FUNCTIONS
###########################
def __long_poll(activity, instance, poller, configuration):
    logger.debug("Waiting for operation '{}' on instance '{}' to finish. Giving priority to other operations.".format(
        activity, instance['name']))
    poller.result(config.load_timeout(configuration))
    logger.debug("Finished operation '{}' on instance '{}'.".format(activity, instance['name']))

    return instance


def __long_poll_command(activity, group, instance, duration, parameters, configuration, client):
    logger.debug("Waiting for operation '{}' on instance '{}' to finish. Giving priority to other operations.".format(
        activity, instance['name']))
    timeout = config.load_timeout(configuration) + duration
    command.run(group, instance, timeout, parameters, client)
    logger.debug("Finished operation '{}' on instance '{}'.".format(activity, instance['name']))

    return instance
