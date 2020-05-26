# -*- coding: utf-8 -*-

from chaoslib.exceptions import FailedActivity
from chaoslib.types import Configuration, Secrets
from logzero import logger
from msrestazure import azure_exceptions

from pdchaosazure.common import cleanse, config
from pdchaosazure.common.compute import command, init_client
from pdchaosazure.machine.constants import RES_TYPE_VM
from pdchaosazure.common.resources.graph import fetch_resources

__all__ = ["delete_machines", "stop_machines", "restart_machines",
           "start_machines", "stress_cpu", "fill_disk", "network_latency",
           "burn_io"]

from pdchaosazure.vmss.records import Records


def delete_machines(filter: str = None,
                    configuration: Configuration = None,
                    secrets: Secrets = None):
    """
    Delete virtual machines at random.

    **Be aware**: Deleting a machine is an invasive action. You will not be
    able to recover the machine once you deleted it.

    Parameters
    ----------
    filter : str, optional
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.

    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/

    >>> delete_machines("where resourceGroup=='rg'", c, s)
    Delete all machines from the group 'rg'

    >>> delete_machines("where resourceGroup=='rg' and name='name'", c, s)
    Delete the machine from the group 'rg' having the name 'name'

    >>> delete_machines("where resourceGroup=='rg' | sample 2", c, s)
    Delete two machines at random from the group 'rg'
    """
    logger.debug(
        "Start delete_machines: "
        "configuration='{}', filter='{}'".format(configuration, filter))

    machines = __fetch_machines(filter, configuration, secrets)
    client = __compute_mgmt_client(secrets, configuration)
    machine_records = Records()
    for machine in machines:
        logger.debug("Deleting machine: {}".format(machine['name']))

        try:
            poller = client.virtual_machines.delete(machine['resourceGroup'], machine['name'])

        except azure_exceptions.CloudError as e:
            raise FailedActivity(e.message)

        poller.result(config.load_timeout(configuration))
        machine_records.add(cleanse.machine(machine))

    return machine_records.output_as_dict('resources')


def stop_machines(filter: str = None,
                  configuration: Configuration = None,
                  secrets: Secrets = None):
    """
    Stop virtual machines at random.

    Parameters
    ----------
    filter : str, optional
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.

    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/

    >>> stop_machines("where resourceGroup=='rg'", c, s)
    Stop all machines from the group 'rg'

    >>> stop_machines("where resourceGroup=='mygroup' and name='myname'", c, s)
    Stop the machine from the group 'mygroup' having the name 'myname'

    >>> stop_machines("where resourceGroup=='mygroup' | sample 2", c, s)
    Stop two machines at random from the group 'mygroup'
    """
    logger.debug("Starting {}: configuration='{}', filter='{}'".format(stop_machines.__name__, configuration, filter))

    machines = __fetch_machines(filter, configuration, secrets)
    client = __compute_mgmt_client(secrets, configuration)

    machine_records = Records()
    for machine in machines:
        logger.debug("Stopping machine '{}'".format(machine['name']))

        try:
            poller = client.virtual_machines.power_off(machine['resourceGroup'], machine['name'])

        except azure_exceptions.CloudError as e:
            raise FailedActivity(e.message)

        poller.result(config.load_timeout(configuration))
        machine_records.add(cleanse.machine(machine))

    return machine_records.output_as_dict('resources')


def restart_machines(filter: str = None,
                     configuration: Configuration = None,
                     secrets: Secrets = None):
    """
    Restart virtual machines at random.

    Parameters
    ----------
    filter : str, optional
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.

    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/

    >>> restart_machines("where resourceGroup=='rg'", c, s)
    Restart all machines from the group 'rg'

    >>> restart_machines("where resourceGroup=='rg' and name='name'", c, s)
    Restart the machine from the group 'rg' having the name 'name'

    >>> restart_machines("where resourceGroup=='rg' | sample 2", c, s)
    Restart two machines at random from the group 'rg'
    """
    logger.debug("Starting {}: configuration='{}', filter='{}'".format(
        restart_machines.__name__, configuration, filter))

    machines = __fetch_machines(filter, configuration, secrets)
    client = __compute_mgmt_client(secrets, configuration)
    machine_records = Records()
    for machine in machines:
        logger.debug("Restarting machine: {}".format(machine['name']))

        try:
            poller = client.virtual_machines.restart(machine['resourceGroup'], machine['name'])

        except azure_exceptions.CloudError as e:
            raise FailedActivity(e.message)

        poller.result(config.load_timeout(configuration))
        machine_records.add(cleanse.machine(machine))

    return machine_records.output_as_dict('resources')


def start_machines(filter: str = None,
                   configuration: Configuration = None,
                   secrets: Secrets = None):
    """
    Start virtual machines at random. Thought as a rollback action.

    Parameters
    ----------
    filter : str, optional
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.

    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/

    >>> start_machines("where resourceGroup=='rg'", c, s)
    Start all stopped machines from the group 'rg'

    >>> start_machines("where resourceGroup=='rg' and name='name'", c, s)
    Start the stopped machine from the group 'rg' having the name 'name'

    >>> start_machines("where resourceGroup=='rg' | sample 2", c, s)
    Start two stopped machines at random from the group 'rg'
    """

    logger.debug("Starting {}: configuration='{}', filter='{}'".format(start_machines.__name__, configuration, filter))

    machines = __fetch_machines(filter, configuration, secrets)
    client = __compute_mgmt_client(secrets, configuration)
    stopped_machines = __fetch_all_stopped_machines(client, machines)

    machine_records = Records()
    for machine in stopped_machines:
        logger.debug("Starting machine '{}'".format(machine['name']))

        try:
            poller = client.virtual_machines.start(machine['resourceGroup'], machine['name'])

        except azure_exceptions.CloudError as e:
            raise FailedActivity(e.message)

        poller.result(config.load_timeout(configuration))
        machine_records.add(cleanse.machine(machine))

    return machine_records.output_as_dict('resources')


def stress_cpu(filter: str = None,
               duration: int = 120,
               configuration: Configuration = None,
               secrets: Secrets = None):
    """
    Stress CPU up to 100% at virtual machines.

    Parameters
    ----------
    filter : str, optional
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.
    duration : int, optional
        Duration of the stress test (in seconds) that generates high CPU usage.
        Defaults to 120 seconds.

    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/

    >>> stress_cpu("where resourceGroup=='rg'", configuration=c, secrets=s)
    Stress all machines from the group 'rg'

    >>> stress_cpu("where resourceGroup=='rg' and name='name'",
                    configuration=c, secrets=s)
    Stress the machine from the group 'rg' having the name 'name'

    >>> stress_cpu("where resourceGroup=='rg' | sample 2",
                    configuration=c, secrets=s)
    Stress two machines at random from the group 'rg'
    """

    logger.debug(
        "Starting stress_cpu: configuration='{}', filter='{}', duration='{}'".format(configuration, filter, duration))

    machines = __fetch_machines(filter, configuration, secrets)

    machine_records = Records()
    for machine in machines:
        command_id, script_content = command.prepare(machine, 'cpu_stress_test')

        parameters = {
            'command_id': command_id,
            'script': [script_content],
            'parameters': [
                {'name': "duration", 'value': duration}
            ]
        }

        logger.debug("Executing operation '{}' on machine: '{}'".format(stress_cpu.__name__, machine['name']))
        command.run(machine['resourceGroup'], machine, duration, parameters, secrets, configuration)
        machine_records.add(cleanse.machine(machine))

    return machine_records.output_as_dict('resources')


def fill_disk(filter: str = None,
              duration: int = 120,
              size: int = 1000,
              path: str = None,
              configuration: Configuration = None,
              secrets: Secrets = None):
    """
    Fill the disk with random data.

    Parameters
    ----------
    filter : str, optional
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.
    duration : int, optional
        Lifetime of the file created. Defaults to 120 seconds.
    size : int
        Size of the file created on the disk. Defaults to 1GB.
    path : str, optional
        The absolute path to write the fill file into.
        Defaults: C:/burn for Windows clients, /root/burn for Linux clients.


    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/

    >>> fill_disk("where resourceGroup=='rg'", configuration=c, secrets=s)
    Fill all machines from the group 'rg'

    >>> fill_disk("where resourceGroup=='rg' and name='name'",
                    configuration=c, secrets=s)
    Fill the machine from the group 'rg' having the name 'name'

    >>> fill_disk("where resourceGroup=='rg' | sample 2",
                    configuration=c, secrets=s)
    Fill two machines at random from the group 'rg'
    """

    logger.debug("Starting fill_disk: configuration='{}', filter='{}', duration='{}', size='{}', path='{}'".format(
        configuration, filter, duration, size, path))

    machines = __fetch_machines(filter, configuration, secrets)

    machine_records = Records()
    for machine in machines:
        command_id, script_content = command.prepare(machine, 'fill_disk')
        fill_path = command.prepare_path(machine, path)

        parameters = {
            'command_id': command_id,
            'script': [script_content],
            'parameters': [
                {'name': "duration", 'value': duration},
                {'name': "size", 'value': size},
                {'name': "path", 'value': fill_path}
            ]
        }

        logger.debug("Executing operation '{}' on machine: '{}'".format(fill_disk.__name__, machine['name']))
        command.run(machine['resourceGroup'], machine, duration, parameters, secrets, configuration)
        machine_records.add(cleanse.machine(machine))

    return machine_records.output_as_dict('resources')


def network_latency(filter: str = None,
                    duration: int = 60,
                    delay: int = 200,
                    jitter: int = 50,
                    configuration: Configuration = None,
                    secrets: Secrets = None):
    """
    Increases the response time of the virtual machine.

    Parameters
    ----------
    filter : str, optional
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.
    duration : int, optional
        How long the latency lasts. Defaults to 60 seconds.
    delay : int
        Added delay in ms. Defaults to 200.
    jitter : int
        Variance of the delay in ms. Defaults to 50.


    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/

    >>> network_latency("where resourceGroup=='rg'", configuration=c,
                    secrets=s)
    Increase the latency of all machines from the group 'rg'

    >>> network_latency("where resourceGroup=='rg' and name='name'",
                    configuration=c, secrets=s)
    Increase the latecy of the machine from the group 'rg' having the name
    'name'

    >>> network_latency("where resourceGroup=='rg' | sample 2",
                    configuration=c, secrets=s)
    Increase the latency of two machines at random from the group 'rg'
    """

    logger.debug(
        "Starting network_latency: configuration='{}', filter='{}', duration='{}', delay='{}', jitter='{}'".format(
            configuration, filter, duration, delay, jitter))

    machines = __fetch_machines(filter, configuration, secrets)

    machine_records = Records()
    for machine in machines:
        command_id, script_content = command.prepare(machine, 'network_latency')

        logger.debug("Script content: {}".format(script_content))
        parameters = {
            'command_id': command_id,
            'script': [script_content],
            'parameters': [
                {'name': "duration", 'value': duration},
                {'name': "delay", 'value': delay},
                {'name': "jitter", 'value': jitter}
            ]
        }

        logger.debug("Executing operation '{}' on machine: '{}'".format(network_latency.__name__, machine['name']))
        command.run(machine['resourceGroup'], machine, duration, parameters, secrets, configuration)
        machine_records.add(cleanse.machine(machine))

    return machine_records.output_as_dict('resources')


def burn_io(filter: str = None,
            duration: int = 60,
            configuration: Configuration = None,
            secrets: Secrets = None):
    """
    Increases the Disk I/O operations per second of the virtual machine.

    Parameters
    ----------
    filter : str, optional
        Filter the virtual machines. If the filter is omitted all machines in
        the subscription will be selected as potential chaos candidates.
    duration : int, optional
        How long the burn lasts. Defaults to 60 seconds.


    Examples
    --------
    Some calling examples. Deep dive into the filter syntax:
    https://docs.microsoft.com/en-us/azure/kusto/query/

    >>> burn_io("where resourceGroup=='rg'", configuration=c, secrets=s)
    Increase the I/O operations per second of all machines from the group 'rg'

    >>> burn_io("where resourceGroup=='rg' and name='name'",
                    configuration=c, secrets=s)
    Increase the I/O operations per second of the machine from the group 'rg'
    having the name 'name'

    >>> burn_io("where resourceGroup=='rg' | sample 2",
                    configuration=c, secrets=s)
    Increase the I/O operations per second of two machines at random from
    the group 'rg'
    """

    logger.debug(
        "Starting burn_io: configuration='{}', filter='{}', duration='{}',".format(configuration, filter, duration))

    machines = __fetch_machines(filter, configuration, secrets)

    machine_records = Records()
    for machine in machines:
        command_id, script_content = command.prepare(machine, 'burn_io')

        parameters = {
            'command_id': command_id,
            'script': [script_content],
            'parameters': [
                {'name': "duration", 'value': duration}
            ]
        }

        logger.debug("Executing operation '{}' on machine: '{}'".format(burn_io.__name__, machine['name']))
        command.run(machine['resourceGroup'], machine, duration, parameters, secrets, configuration)
        machine_records.add(cleanse.machine(machine))

    return machine_records.output_as_dict('resources')


###############################################################################
# Private helper functions
###############################################################################
def __fetch_all_stopped_machines(client, machines) -> []:
    stopped_machines = []
    for m in machines:
        i = client.virtual_machines.instance_view(m['resourceGroup'],
                                                  m['name'])
        for s in i.statuses:
            status = s.code.lower().split('/')
            if status[0] == 'powerstate' and (
                    status[1] == 'deallocated' or status[1] == 'stopped'):
                stopped_machines.append(m)
                logger.debug("Found stopped machine: {}".format(m['name']))
    return stopped_machines


def __fetch_machines(filter, configuration, secrets) -> []:
    machines = fetch_resources(filter, RES_TYPE_VM, secrets, configuration)
    if not machines:
        logger.warning("No virtual machines found")
        raise FailedActivity("No virtual machines found")

    return machines


def __compute_mgmt_client(secrets, configuration):
    return init_client(secrets, configuration)
