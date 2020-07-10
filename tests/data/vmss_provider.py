from pdchaosazure.vmss.constants import RES_TYPE_VMSS_VM, RES_TYPE_VMSS


def provide_instance(os_type: str = 'Linux'):
    return {
        'name': 'chaos-pool_0',
        'instance_id': '0',
        'type': RES_TYPE_VMSS_VM,
        'storage_profile': {
            'os_disk': {
                'os_type': os_type
            }
        }
    }


def provide_instance_real_sample():
    return {
        "id": "/subscriptions/054aa9fa-aa51/resourceGroups/mc_vmss-stress_cpu_stress-aks_westeurope/providers"
              "/Microsoft.Compute/virtualMachineScaleSets/aks-nodepool1-97aaaa41-vmss/virtualMachines/0",
        "name": "aks-nodepool1-97aaaa41-vmss_0",
        "type": "Microsoft.Compute/virtualMachineScaleSets/virtualMachines",
        "location": "westeurope",
        "tags": {
            "aksEngineVersion": "aks-release-v0.47.0-1-aks",
            "creationSource": "aks-aks-nodepool1-97aaaa41-vmss",
            "orchestrator": "Kubernetes:1.15.10",
            "poolName": "nodepool1",
            "resourceNameSuffix": "97aaaa41"
        },
        "instance_id": "0",
        "sku": {
            "name": "Standard_B2s",
            "tier": "Standard"
        },
        "latest_model_applied": True,
        "vm_id": "0b7f3917-f384-4cce-99a2-57aa90cd618f",
        "hardware_profile": {

        },
        "storage_profile": {
            "image_reference": {
                "publisher": "microsoft-aks",
                "offer": "aks",
                "sku": "aks-ubuntu-1604-202005",
                "version": "2020.05.06",
                "exact_version": "2020.05.06"
            },
            "os_disk": {
                "os_type": "Linux",
                "name": "aks-nodepool1-971532aks-nodepool1-9715324OS__1_b29b25b45092421e868aad174d081d35",
                "caching": "ReadWrite",
                "create_option": "FromImage",
                "disk_size_gb": 100,
                "managed_disk": {
                    "id": "/subscriptions/054aa9fa-aa51/resourceGroups/MC_VMSS-STRESS_CPU_STRESS-AKS_WESTEUROPE"
                          "/providers/Microsoft.Compute/disks/aks-nodepool1-971532aks-nodepool1"
                          "-9715324OS__1_b29b25b45092421e868aad174d081d35",
                    "storage_account_type": "Premium_LRS"
                }
            },
            "data_disks": [

            ]
        },
        "os_profile": {
            "computer_name": "aks-nodepool1-97aaaa41-vmss000000",
            "admin_username": "azureuser",
            "linux_configuration": {
                "disable_password_authentication": True,
                "ssh": {
                    "public_keys": [
                        {
                            "path": "/home/azureuser/.ssh/authorized_keys",
                            "key_data": "ssh-rsa AAAAB3NzaC1yc2EAAAAD...36DUMk723yUAbzf+f5"
                        }
                    ]
                },
                "provision_vm_agent": True
            },
            "secrets": [

            ],
            "allow_extension_operations": True,
            "require_guest_provision_signal": True
        },
        "network_profile": {
            "network_interfaces": [
                {
                    "id": "/subscriptions/054aa9fa-aa51/resourceGroups/MC_vmss-stress_cpu_stress-aks_westeurope"
                          "/providers/Microsoft.Compute/virtualMachineScaleSets/aks-nodepool1-97aaaa41-vmss"
                          "/virtualMachines/0/networkInterfaces/aks-nodepool1-97aaaa41-vmss "
                }
            ]
        },
        "network_profile_configuration": {
            "network_interface_configurations": [
                {
                    "name": "aks-nodepool1-97aaaa41-vmss",
                    "primary": True,
                    "enable_accelerated_networking": False,
                    "dns_settings": {
                        "dns_servers": [

                        ]
                    },
                    "ip_configurations": [
                        {
                            "name": "ipconfig1",
                            "subnet": {
                                "id": "/subscriptions/054aa9fa-aa51/resourceGroups/MC_vmss-stress_cpu_stress"
                                      "-aks_westeurope/providers/Microsoft.Network/virtualNetworks/aks-vnet-97aaaa41"
                                      "/subnets/aks-subnet "
                            },
                            "primary": True,
                            "private_ip_address_version": "IPv4",
                            "load_balancer_backend_address_pools": [
                                {
                                    "id": "/subscriptions/054aa9fa-aa51/resourceGroups/MC_vmss-stress_cpu_stress"
                                          "-aks_westeurope/providers/Microsoft.Network/loadBalancers/kubernetes"
                                          "/backendAddressPools/aksOutboundBackendPool "
                                },
                                {
                                    "id": "/subscriptions/054aa9fa-aa51/resourceGroups/MC_vmss-stress_cpu_stress"
                                          "-aks_westeurope/providers/Microsoft.Network/loadBalancers/kubernetes"
                                          "/backendAddressPools/kubernetes "
                                }
                            ]
                        }
                    ],
                    "enable_ip_forwarding": True
                }
            ]
        },
        "provisioning_state": "Succeeded",
        "model_definition_applied": "VirtualMachineScaleSet",
        "resources": [
            {
                "id": "/subscriptions/054aa9fa-aa51/resourceGroups/mc_vmss-stress_cpu_stress-aks_westeurope/providers"
                      "/Microsoft.Compute/virtualMachines/aks-nodepool1-97aaaa41-vmss_0/extensions/vmssCSE",
                "name": "vmssCSE",
                "type": "Microsoft.Compute/virtualMachines/extensions",
                "location": "westeurope",
                "publisher": "Microsoft.Azure.Extensions",
                "virtual_machine_extension_type": "CustomScript",
                "type_handler_version": "2.0",
                "auto_upgrade_minor_version": True,
                "settings": {

                },
                "provisioning_state": "Succeeded"
            },
            {
                "id": "/subscriptions/054aa9fa-aa51/resourceGroups/mc_vmss-stress_cpu_stress-aks_westeurope/providers"
                      "/Microsoft.Compute/virtualMachines/aks-nodepool1-97aaaa41-vmss_0/extensions/aks-nodepool1"
                      "-97aaaa41-vmss-AKSLinuxBilling",
                "name": "aks-nodepool1-97aaaa41-vmss-AKSLinuxBilling",
                "type": "Microsoft.Compute/virtualMachines/extensions",
                "location": "westeurope",
                "publisher": "Microsoft.AKS",
                "virtual_machine_extension_type": "Compute.AKS.Linux.Billing",
                "type_handler_version": "1.0",
                "auto_upgrade_minor_version": True,
                "settings": {

                },
                "provisioning_state": "Succeeded"
            }
        ],
        "scale_set": "aks-nodepool1-97aaaa41-vmss"
    }


def provide_scale_set():
    return {
        'name': 'chaos-pool',
        'resourceGroup': 'rg',
        'type': RES_TYPE_VMSS,
    }
