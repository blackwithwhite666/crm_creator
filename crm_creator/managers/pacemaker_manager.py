import logging

from crm_creator.utils import cached_property
from crm_creator.parsers import CibConfig
from crm_creator.defines import (COMMAND_TEMPLATE, DRBD_PRIMITIVE_NAME, DRBD_MS_NAME,
                                 VIRT_PRIMITIVE_NAME, COLOCATION_ID, ORDER_ID)
from .base_manager import BaseManager

logger = logging.getLogger('managers.pacemaker')


class PacemakerManager(BaseManager):
    @cached_property()
    def config(self):
        return CibConfig.create(self.connection)
    
    def get_drbd_primitive_name(self, name):
        return DRBD_PRIMITIVE_NAME % name
    
    def get_drbd_ms_name(self, name):
        return DRBD_MS_NAME % name
    
    def drbd_primitive_exist(self, name):
        return self.config.has_primitive(self.get_drbd_primitive_name(name))
    
    def drbd_ms_exist(self, name):
        return self.config.has_master(self.get_drbd_ms_name(name))
    
    def get_vm_primitive_name(self, name):
        return VIRT_PRIMITIVE_NAME % name
    
    def vm_exist(self, name):
        return self.config.has_primitive(self.get_vm_primitive_name(name))
    
    def get_colocation_id(self, name):
        return COLOCATION_ID % name
    
    def get_order_id(self, name):
        return ORDER_ID % name
    
    def generate_config(self, name, virt_config, template):
        kwargs = {
                  'drbd_primitive_id': self.get_drbd_primitive_name(name),
                  'drbd_resource': name,
                  'virt_primitive_id': self.get_vm_primitive_name(name),
                  'virt_config': virt_config,
                  'drbd_ms_id': self.get_drbd_ms_name(name),
                  'colocation_id': self.get_colocation_id(name),
                  'order_id': self.get_order_id(name),
                  }
        return template % kwargs
    
    def commit_config(self, config):
        command = COMMAND_TEMPLATE % config
        logging.debug('Run: %s' % command)
        if not self.dry_run:
            self.connection.execute(command)
