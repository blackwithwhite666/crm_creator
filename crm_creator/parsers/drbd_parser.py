class DrbdConfig(dict):
    parsers = (
        (0, lambda column: zip(('minor', 'name'), column.split(':'))),
        (1, lambda column: [('state', column)]),
        (2, lambda column: zip(('first_node_state', 'second_node_state'), column.split('/'))),
        (3, lambda column: zip(('first_node_disk_state', 'second_node_disk_state'), column.split('/'))),
        (4, lambda column: [('protocol', column)]),
        (5, lambda column: [('flags', column)]),
        (6, lambda column: [('guest_state', True if column[0] == '*' else False), ('guest_name', column[1:])]),
        (7, lambda column: [('guest_dev', column)]),
        (8, lambda column: [('guest_driver', column)]),
    )
    
    @classmethod
    def create(cls, connection):
        return cls(connection.execute('drbd-overview'))
    
    def __init__(self, content):
        self.content = unicode(content)
        self.parsers_dict = dict(self.parsers) 
        self.initialize()
        
    def initialize(self):
        map(lambda row: self.parse_line(row.strip()), self.content.splitlines())
    
    def parse_line(self, row):
        if row.startswith('['): return
        d = {}
        for i, column in enumerate(u" ".join(row.split()).split()):
            if i not in self.parsers_dict: continue
            d.update(self.parsers_dict[i](column))
        if 'name' not in d: return
        self[d['name']] = d