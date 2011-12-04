from crm_creator.utils import cached_property
from crm_creator.parsers import DrbdConfig
from .base_manager import BaseManager


class DrbdManager(BaseManager):
    @cached_property()
    def config(self):
        return DrbdConfig.create(self.connection)
    
    def resource_exist(self, name):
        return name in self.config
    
    def get_resource_state(self, name):
        state = self.config[name]
        return (state['first_node_state'], state['second_node_state'])
    
    def get_disk_state(self, name):
        state = self.config[name]
        return (state['first_node_disk_state'], state['second_node_disk_state'])
    
    def get_vm_uses_resource(self, name):
        return self.config[name].get('guest_name', None)