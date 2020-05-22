class MockLROPoller(object):
    def result(self, timeout: None):
        pass


class MockVirtualMachineScaleSetVMsOperations(object):
    def power_off(self, resource_group_name, scale_set_name, instance_id):
        return MockLROPoller()

    def delete(self, resource_group_name, scale_set_name, instance_id):
        return MockLROPoller()

    def restart(self, resource_group_name, scale_set_name, instance_id):
        return MockLROPoller()

    def deallocate(self, resource_group_name, scale_set_name, instance_id):
        return MockLROPoller()


class MockComputeManagementClient(object):
    def __init__(self):
        self.operations = MockVirtualMachineScaleSetVMsOperations()

    @property
    def virtual_machine_scale_set_vms(self):
        return self.operations
