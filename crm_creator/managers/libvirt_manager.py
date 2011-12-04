from crm_creator.defines import LIBVIRT_CONFIG_PATH
from crm_creator.utils import cached_property
from crm_creator.parsers import VirshConfig
from crm_creator.exceptions import RunException
from .base_manager import BaseManager


class LibvirtManager(BaseManager):
    @cached_property()
    def config(self):
        return VirshConfig.create(self.connection)
    
    def config_exist(self, name):
        return name in self.config
    
    def config_file_exist(self, name):
        path = self.get_config_path(name)
        return self.file_exist(path)
        
    def file_exist(self, path):
        try:
            self.connection.execute('test -e %s' % path)
            return True
        except RunException, e:
            return False
    
    def get_config_path(self, name):
        return LIBVIRT_CONFIG_PATH % name