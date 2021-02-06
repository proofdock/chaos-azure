class MockLROPoller(object):
    def result(self, timeout: None):
        pass


class MockVirtualMachineScaleSetVMsOperations(object):
    def begin_power_off(self, resource_group_name, scale_set_name, instance_id):
        return MockLROPoller()

    def begin_delete(self, resource_group_name, scale_set_name, instance_id):
        return MockLROPoller()

    def begin_restart(self, resource_group_name, scale_set_name, instance_id):
        return MockLROPoller()

    def begin_deallocate(self, resource_group_name, scale_set_name, instance_id):
        return MockLROPoller()


class MockComputeManagementClient(object):
    def __init__(self):
        self.operations = MockVirtualMachineScaleSetVMsOperations()

    @property
    def virtual_machine_scale_set_vms(self):
        return self.operations
