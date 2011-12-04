class VirshConfig(dict):
    parsers = (
        (0, lambda column: [('id', column)]),
        (1, lambda column: [('name', column)]),
        (2, lambda column: [('state', column)]),
    )
    
    @classmethod
    def create(cls, connection):
        return cls(connection.execute('virsh list --all'))
    
    def __init__(self, content):
        self.content = content
        self.parsers_dict = dict(self.parsers)
        self.initialize()
    
    def initialize(self):
        map(lambda row: self.parse_row(row),
            filter(None,
                   map(lambda row: row.strip(), 
                       self.content.splitlines()) )[2:]
            )
    
    def parse_row(self, row):
        d = {}
        for i, column in enumerate(u" ".join(row.split()).split()):
            if i not in self.parsers_dict: continue
            d.update(self.parsers_dict[i](column))
        if 'name' not in d: return
        self[d['name']] = d