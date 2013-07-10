import redis
from redis.exceptions import ConnectionError


class Redis(object):

    def __init__(self, agentConfig, checksLogger, rawConfig):
        self.agentConfig = agentConfig
        self.checksLogger = checksLogger
        self.rawConfig = rawConfig

    def run(self):
        info = {'running': 0}

        try:
            host = self.rawConfig['Main']['redis_host']
        except (KeyError, TypeError):
            host = 'localhost'

        try:
            port = int(self.rawConfig['Main']['redis_port'])
        except (KeyError, TypeError):
            port = 6379

        r = redis.StrictRedis(host=host, port=port)

        try:
            info = r.info()
            info['running'] = 1
            info['keys_on_db0'] = r.info()['db0']['keys']
        except ConnectionError as e:
            self.checksLogger.error('Failed to collect data: {}'.format(e))

        return info
