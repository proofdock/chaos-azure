def default():
    return {
        'columns': [
            {'name': 'id', 'type': 'string'},
            {'name': 'sku', 'type': 'object'},
            {'name': 'name', 'type': 'string'},
            {'name': 'type', 'type': 'string'},
            {'name': 'kind', 'type': 'string'},
            {'name': 'plan', 'type': 'object'},
            {'name': 'tags', 'type': 'object'},
            {'name': 'location', 'type': 'string'},
            {'name': 'properties', 'type': 'object'},
            {'name': 'resourceGroup', 'type': 'string'},
            {'name': 'subscriptionId', 'type': 'string'},
            {'name': 'managedBy', 'type': 'string'},
            {'name': 'identity', 'type': 'object'},
            {'name': 'zones', 'type': 'object'},
            {'name': 'tenantId', 'type': 'string'}
        ],
        'rows': [
            [
                '/subscriptions/05aaaafa-6aa1/resourceGroups/vmachine/providers/Microsoft.Compute/virtualMachines/vmachine1',
                None, 'vmachine1',
                'microsoft.compute/virtualmachines', '',
                None, None, 'westeurope',
                {
                    'provisioningState': 'Succeeded',
                    'networkProfile': {
                        'networkInterfaces': [
                            {
                                'id': '/subscriptions/05aaaafa-6aa1/resourceGroups/vmachine/providers/Microsoft.Network/networkInterfaces/vmachine1960'
                            }
                        ]
                    },
                    'storageProfile': {
                        'imageReference': {
                            'publisher': 'Canonical',
                            'exactVersion': '18.04.202004290',
                            'version': 'latest',
                            'sku': '18.04-LTS',
                            'offer': 'UbuntuServer'
                        },
                        'dataDisks': [],
                        'osDisk': {
                            'name': 'vmachine1_disk1_300a88dc334643b187532d00957f5736',
                            'createOption': 'FromImage',
                            'diskSizeGB': 30,
                            'managedDisk': {
                                'id': '/subscriptions/05aaaafa-6aa1/resourceGroups/VMACHINE/providers/Microsoft.Compute/disks/vmachine1_disk1_300a88dc334643b187532d00957f5736',
                                'storageAccountType': 'Premium_LRS'},
                            'caching': 'ReadWrite',
                            'osType': 'Linux'}
                    },
                    'hardwareProfile': {
                        'vmSize': 'Standard_B1ls'},
                    'osProfile': {
                        'allowExtensionOperations': True,
                        'secrets': [],
                        'requireGuestProvisionSignal': True,
                        'adminUsername': 'buderre',
                        'linuxConfiguration': {
                            'disablePasswordAuthentication': False,
                            'provisionVMAgent': True},
                        'computerName': 'vmachine1'},
                    'vmId': 'e267230d-b84a-45cd-a212-ca1c26decaf8',
                    'diagnosticsProfile': {
                        'bootDiagnostics': {
                            'enabled': True,
                            'storageUri': 'https://vmachinediag754.blob.core.windows.net/'}
                    }
                },
                'vmachine',
                '05aaaafa-6aa1',
                '', None, None,
                'fead2b37-53d7-4cd9-ad12-d2b6c0751f29']
        ]
    }


def simple():
    return {
        'columns': [
            {'name': 'id', 'type': 'string'},
            {'name': 'name', 'type': 'string'},
            {'name': 'type', 'type': 'string'},
        ],
        'rows': [
            [
                '/subscriptions/05aaaafa-6aa1/resourceGroups/vmachine/providers/Microsoft.Compute/virtualMachines/vmachine1',
                'vmachine1',
                'microsoft.compute/virtualmachines'
            ]
        ]
    }


def empty():
    return {
        'columns': [],
        'rows': []
    }
