from pdchaosazure.vm.constants import RES_TYPE_VM


def default(os_type: str = 'Linux'):
    return {
        'name': 'chaos-machine',
        'resourceGroup': 'rg',
        'type': RES_TYPE_VM,
        'properties': {
            'storageProfile': {
                'osDisk': {
                    'osType': os_type
                }
            }}
    }
