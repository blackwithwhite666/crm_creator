from .managers import ManagerRegistry
from .exceptions import DispatcherException


class Dispatcher(object):
    def __init__(self, connection, dry_run, name, template):
        self.name = name
        self.template = template
        self.managers = ManagerRegistry(connection=connection, dry_run=dry_run)
    
    def check_drb_state(self, node_states, desired_states):
        '''
        Compare actual and desired state and throw exception if they are different
        @param node_states: actual resource states
        @param desired_states: desired resource states
        '''
        
        unique_state = set(node_states)
        desired_states = set(desired_states)
        
        result_states = unique_state - desired_states
        if result_states:
            raise DispatcherException("DRBD resource `%s' in bad state: %s" % (self.name, ', '.join(result_states)))
    
    def check_drbd_resource(self):
        '''
        Check DRBD resource state
        '''
        # check resource existence
        if not self.managers.drbd.resource_exist(self.name):
            raise DispatcherException("DRBD resource `%s' not exist" % self.name)
        
        # check resource state
        resource_state = self.managers.drbd.get_resource_state(self.name)
        disk_state = self.managers.drbd.get_disk_state(self.name)
        
        self.check_drb_state(resource_state, (u'Primary', u'Secondary'))
        self.check_drb_state(disk_state, (u'UpToDate', ))
        
        # check that no vm use this resource
        vm_name = self.managers.drbd.get_vm_uses_resource(self.name)
        if vm_name != self.name and vm_name is not None:
            raise DispatcherException("VM `%s' use DRBD resource `%s'" % (vm_name, self.name))
    
    def check_libvirt_config(self):
        '''
        Check that vm config exist
        '''
        if not self.managers.libvirt.config_exist(self.name):
            raise DispatcherException("Config for VM `%s' not exist" % self.name)
        
        if not self.managers.libvirt.config_file_exist(self.name):
            raise DispatcherException("Config file for VM `%s' not exist" % self.name)
        
    def check_pacemaker_config(self):
        '''
        Check that pacemaker primitives not exist
        '''
        
        if self.managers.pacemaker.drbd_primitive_exist(self.name):
            raise DispatcherException("DRBD primitive for `%s' already exist" % self.name)
        
        if self.managers.pacemaker.drbd_ms_exist(self.name):
            raise DispatcherException("DRBD ms for `%s' already exist" % self.name)
        
        if self.managers.pacemaker.vm_exist(self.name):
            raise DispatcherException("VM primitive for `%s' already exist" % self.name)
    
    def generate_pacemaker_config(self):
        virt_config = self.managers.libvirt.get_config_path(self.name)
        return self.managers.pacemaker.generate_config(name=self.name, virt_config=virt_config, template=self.template)
    
    def apply_pacemaker_config(self):
        # generate pacemaker config
        config = self.generate_pacemaker_config()
        
        # commit config
        self.managers.pacemaker.commit_config(config)
        
    def process(self):
        # check drbd resource
        self.check_drbd_resource()
        
        # check that vm config exist
        self.check_libvirt_config()
        
        # check pacemaker config
        self.check_pacemaker_config()
        
        # apply pacemaker config
        self.apply_pacemaker_config()
        