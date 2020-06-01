# -*- coding: utf-8 -*-
import concurrent.futures

from chaoslib.exceptions import FailedActivity
from chaoslib.types import Configuration, Secrets
from logzero import logger
from msrestazure import azure_exceptions

from pdchaosazure.common import cleanse, config
from pdchaosazure.common.compute import command, init_client

__all__ = ["burn_io", "delete_machines", "fill_disk", "network_latency",
           "restart_machines", "stop_machines", "stress_cpu"]

from pdchaosazure.machine.fetcher import fetch_machines

from pdchaosazure.vmss.records import Records


def delete_machines(filter: str = None,
                    configuration: Configuration = None,
                    secrets: Secrets = None):
    """Delete virtual machine instance(s).

    **Be aware**: Deleting a machine instance is an invasive action. You will not be
    able to recover the machine instance once you deleted it.

    Parameters
    ----------
    filter : str, optional
        Filter the virtual machine instance(s). If omitted a random instance from your subscription is selected.
    """
    logger.debug(
        "Starting {}: configuration='{}', filter='{}'".format(delete_machines.__name__, configuration, filter))

    machines = fetch_machines(filter, configuration, secrets)
    client = init_client(secrets, configuration)
    machine_records = Records()

    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(machines)) as executor:
        for machine in machines:
            logger.debug("Deleting machine: {}".format(machine['name']))

            try:
                poller = client.virtual_machines.delete(machine['resourceGroup'], machine['name'])
            except azure_exceptions.CloudError as e:
                raise FailedActivity(e.message)

            # collect future results
            futures.append(executor.submit(__long_poll, delete_machines.__name__, machine, poller, configuration))

        # wait for results
        for future in concurrent.futures.as_completed(futures):
            affected_machine = future.result()
            machine_records.add(cleanse.machine(affected_machine))

    return machine_records.output_as_dict('resources')


def stop_machines(filter: str = None,
                  configuration: Configuration = None,
                  secrets: Secrets = None):
    """Stop virtual machine instance(s).

    Parameters
    ----------
    filter : str, optional
        Filter the virtual machine instance(s). If omitted a random instance from your subscription is selected.
    """
    logger.debug("Starting {}: configuration='{}', filter='{}'".format(stop_machines.__name__, configuration, filter))

    machines = fetch_machines(filter, configuration, secrets)
    client = init_client(secrets, configuration)

    machine_records = Records()

    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(machines)) as executor:
        for machine in machines:
            logger.debug("Stopping machine '{}'".format(machine['name']))

            try:
                poller = client.virtual_machines.power_off(machine['resourceGroup'], machine['name'])
            except azure_exceptions.CloudError as e:
                raise FailedActivity(e.message)

            # collect future results
            futures.append(executor.submit(__long_poll, stop_machines.__name__, machine, poller, configuration))

        # wait for results
        for future in concurrent.futures.as_completed(futures):
            affected_machine = future.result()
            machine_records.add(cleanse.machine(affected_machine))

    return machine_records.output_as_dict('resources')


def restart_machines(filter: str = None,
                     configuration: Configuration = None,
                     secrets: Secrets = None):
    """Restart virtual machine instance(s).

    Parameters
    ----------
    filter : str, optional
        Filter the virtual machine instance(s). If omitted a random instance from your subscription is selected.
    """
    logger.debug("Starting {}: configuration='{}', filter='{}'".format(
        restart_machines.__name__, configuration, filter))

    machines = fetch_machines(filter, configuration, secrets)
    client = init_client(secrets, configuration)
    machine_records = Records()

    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(machines)) as executor:
        for machine in machines:
            logger.debug("Restarting machine: {}".format(machine['name']))

            try:
                poller = client.virtual_machines.restart(machine['resourceGroup'], machine['name'])
            except azure_exceptions.CloudError as e:
                raise FailedActivity(e.message)

            # collect future results
            futures.append(executor.submit(__long_poll, restart_machines.__name__, machine, poller, configuration))

        # wait for results
        for future in concurrent.futures.as_completed(futures):
            affected_machine = future.result()
            machine_records.add(cleanse.machine(affected_machine))

    return machine_records.output_as_dict('resources')


def stress_cpu(filter: str = None,
               duration: int = 120,
               configuration: Configuration = None,
               secrets: Secrets = None):
    """Stress CPU up to 100% at virtual machines.

    Parameters
    ----------
    filter : str, optional
        Filter the virtual machine instance(s). If omitted a random instance from your subscription is selected.

    duration : int, optional
        Duration of the stress test (in seconds) that generates high CPU usage. Defaults to 120 seconds.
    """

    operation_name = stress_cpu.__name__

    logger.debug(
        "Starting {}: configuration='{}', filter='{}', duration='{}'".format(
            operation_name, configuration, filter, duration))

    machines = fetch_machines(filter, configuration, secrets)
    client = init_client(secrets, configuration)

    machine_records = Records()
    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(machines)) as executor:
        for machine in machines:
            command_id, script_content = command.prepare(machine, operation_name)
            parameters = {
                'command_id': command_id,
                'script': [script_content],
                'parameters': [
                    {'name': "input_duration", 'value': duration}
                ]
            }

            # collect future results
            futures.append(
                executor.submit(
                    __long_poll_command, operation_name, machine, duration, parameters, configuration, client))

        # wait for results
        for future in concurrent.futures.as_completed(futures):
            affected_machine = future.result()
            machine_records.add(cleanse.machine(affected_machine))

    return machine_records.output_as_dict('resources')


def fill_disk(filter: str = None,
              duration: int = 120,
              size: int = 1000,
              path: str = None,
              configuration: Configuration = None,
              secrets: Secrets = None):
    """Fill the disk with random data.

    Parameters
    ----------
    filter : str, optional
        Filter the virtual machine instance(s). If omitted a random instance from your subscription is selected.

    duration : int, optional
        Lifetime of the file created. Defaults to 120 seconds.

    size : int
        Size of the file in megabytes created on the disk. Defaults to 1000 MB.

    path : str, optional
        The absolute path to write the fill file into.
        Defaults to ``C:\burn`` for Windows clients and ``/root/burn`` for Linux clients.
    """

    logger.debug("Starting {}: configuration='{}', filter='{}', duration='{}', size='{}', path='{}'".format(
        fill_disk.__name__, configuration, filter, duration, size, path))

    machines = fetch_machines(filter, configuration, secrets)
    client = init_client(secrets, configuration)

    machine_records = Records()

    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(machines)) as executor:
        for machine in machines:
            command_id, script_content = command.prepare(machine, 'fill_disk')
            fill_path = command.prepare_path(machine, path)
            parameters = {
                'command_id': command_id,
                'script': [script_content],
                'parameters': [
                    {'name': "input_duration", 'value': duration},
                    {'name': "input_size", 'value': size},
                    {'name': "input_path", 'value': fill_path}
                ]
            }

            # collect future results
            futures.append(
                executor.submit(
                    __long_poll_command, fill_disk.__name__, machine, duration, parameters, configuration, client))

        # wait for results
        for future in concurrent.futures.as_completed(futures):
            affected_machine = future.result()
            machine_records.add(cleanse.machine(affected_machine))

    return machine_records.output_as_dict('resources')


def network_latency(filter: str = None,
                    duration: int = 60,
                    delay: int = 200,
                    jitter: int = 50,
                    network_interface: str = "eth0",
                    configuration: Configuration = None,
                    secrets: Secrets = None):
    """Increases the response time of the virtual machine.

    **Please note**: This action is available only for Linux-based systems.

    Parameters
    ----------
    filter : str, optional
        Filter the virtual machine instance(s). If omitted a random instance from your subscription is selected.

    duration : int, optional
        How long the latency lasts. Defaults to 60 seconds.

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

    machines = fetch_machines(filter, configuration, secrets)
    client = init_client(secrets, configuration)

    machine_records = Records()

    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(machines)) as executor:
        for machine in machines:
            command_id, script_content = command.prepare(machine, operation_name)
            logger.debug("Script content: {}".format(script_content))
            parameters = {
                'command_id': command_id,
                'script': [script_content],
                'parameters': [
                    {'name': "input_duration", 'value': duration},
                    {'name': "input_delay", 'value': delay},
                    {'name': "input_jitter", 'value': jitter},
                    {'name': "input_network_interface", 'value': network_interface}
                ]
            }

            # collect future results
            futures.append(
                executor.submit(
                    __long_poll_command, operation_name, machine, duration, parameters, configuration,
                    client))

        # wait for results
        for future in concurrent.futures.as_completed(futures):
            affected_machine = future.result()
            machine_records.add(cleanse.machine(affected_machine))

    return machine_records.output_as_dict('resources')


def burn_io(filter: str = None,
            duration: int = 60,
            path: str = None,
            configuration: Configuration = None,
            secrets: Secrets = None):
    """Simulate heavy disk I/O operations.

    Parameters
    ----------
    filter : str, optional
        Filter the virtual machines. If omitted a random instance from your subscription is selected.

    duration : int, optional
        How long the burn lasts. Defaults to 60 seconds.

    path : str, optional
        The absolute path to write the stress file into. Defaults to ``C:\burn`` for Windows
        clients and ``/root/burn`` for Linux clients.
    """

    logger.debug(
        "Starting {}: configuration='{}', filter='{}', duration='{}',".format(
            burn_io.__name__, configuration, filter, duration))

    machines = fetch_machines(filter, configuration, secrets)
    client = init_client(secrets, configuration)

    machine_records = Records()

    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(machines)) as executor:
        for machine in machines:
            command_id, script_content = command.prepare(machine, 'burn_io')
            fill_path = command.prepare_path(machine, path)
            parameters = {
                'command_id': command_id,
                'script': [script_content],
                'parameters': [
                    {'name': "input_duration", 'value': duration},
                    {'name': "input_path", 'value': fill_path}
                ]
            }

            # collect future results
            futures.append(
                executor.submit(
                    __long_poll_command, burn_io.__name__, machine, duration, parameters, configuration, client))

        # wait for results
        for future in concurrent.futures.as_completed(futures):
            affected_machine = future.result()
            machine_records.add(cleanse.machine(affected_machine))

    return machine_records.output_as_dict('resources')


###########################
#  PRIVATE HELPER FUNCTIONS
###########################
def __long_poll(activity, machine, poller, configuration):
    logger.debug("Waiting for operation '{}' on machine '{}' to finish. Giving priority to other operations.".format(
        activity, machine['name']))
    poller.result(config.load_timeout(configuration))
    logger.debug("Finished operation '{}' on machine '{}'.".format(activity, machine['name']))

    return machine


def __long_poll_command(activity, machine, duration, parameters, configuration, client):
    logger.debug("Waiting for operation '{}' on machine '{}' to finish. Giving priority to other operations.".format(
        activity, machine['name']))
    timeout = config.load_timeout(configuration) + duration
    command.run(machine['resourceGroup'], machine, timeout, parameters, client)
    logger.debug("Finished operation '{}' on machine '{}'.".format(activity, machine['name']))

    return machine
