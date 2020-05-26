from pdchaosazure.machine.constants import RES_TYPE_VM


def default():
    return {
        'name': 'chaos-aks',
        'resourceGroup': 'rg',
        'properties': {
            'nodeResourceGroup': 'nrg'
        }
    }
