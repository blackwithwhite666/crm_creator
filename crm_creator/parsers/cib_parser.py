import libxml2

def encode(s): return unicode(s).encode("UTF-8")

class CibConfig(object):
    
    @classmethod
    def create(cls, connection):
        return cls(connection.execute('cibadmin --query'))
    
    def __init__(self, content):
        self._doc = libxml2.parseDoc(encode(content))
        self._ctxt = self._doc.xpathNewContext()
    
    def __del__(self):
        self._doc.freeDoc()
        self._ctxt.xpathFreeContext()
    
    def _x(self, path):
        return self._ctxt.xpathEval(path)
    
    def get(self, query, **kwargs):
        return self._x('%s%s' % (
                            query,
                            ''.join(
                                map(
                                    lambda (attribute, value):
                                        '[@%(attribute)s="%(value)s"]'
                                            % {'attribute': encode(attribute),
                                               'value': encode(value)},
                                    kwargs.items()
                                )
                            )
                        ))
    
    def get_primitives(self, **kwargs):
        return self.get('/cib/configuration/resources/descendant::primitive', **kwargs)
    
    def has_primitive(self, id, **kwargs):
        return len(self.get_primitives(id=id, **kwargs)) > 0
    
    def get_master(self, id):
        return self.get('/cib/configuration/resources/master', id=id)
    
    def has_master(self, id):
        return len(self.get_master(id)) > 0