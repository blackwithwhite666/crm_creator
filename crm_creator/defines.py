COMMAND_TEMPLATE = """crm<<EOF
configure
%s
commit
EOF"""

DRBD_PRIMITIVE_NAME = "p_drbd_%s"
DRBD_MS_NAME = "ms_drbd_%s"
VIRT_PRIMITIVE_NAME = "p_virt_%s"
COLOCATION_ID = "c_%s"
ORDER_ID = "o_%s"

LIBVIRT_CONFIG_PATH = '/etc/vm/%s.xml'