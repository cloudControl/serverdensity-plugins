import redis
from redis.exceptions import ConnectionError


class Redis(object):

    def __init__(self, agentConfig, checksLogger, rawConfig):
        self.agentConfig = agentConfig
        self.checksLogger = checksLogger
        self.rawConfig = rawConfig

    def run(self):
        info = {}

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
        except ConnectionError as e:
            self.checksLogger.error('Failed to collect data: {}'.format(e))

        return info
