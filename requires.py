from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes


class RequiresRedis(RelationBase):
    scope = scopes.GLOBAL

    auto_accessors = ['hostname', 'port', 'password']

    @hook('{requires:redis}-relation-{joined,changed}')
    def changed(self):
        self.set_state('{relation_name}.connected')
        if self.connection_string():
            self.set_state('{relation_name}.available')

    @hook('{requires:redis}-relation-{broken,departed}')
    def departed(self):
        self.remove_state('{relation_name}.connected')
        self.remove_state('{relation_name}.available')

    def connection_string(self):
        """
        Get the connection string, if available, or None.
        """
        data = {
            'hostname': self.hostname(),
            'port': self.port(),
            'password': self.password(),
        }

        if all(data.values()):
            return str.format('redis://{hostname}:{port}', **data)

        return None
