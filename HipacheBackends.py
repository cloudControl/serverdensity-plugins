import redis
import re


class HipacheBackends(object):

    def __init__(self, agentConfig, checksLogger, rawConfig):
        self.agentConfig = agentConfig
        self.checksLogger = checksLogger
        self.rawConfig = rawConfig

    def run(self):
        try:
            result = {}
            sum_of_all_dead_backends = 0
            frontends_with_no_backends = 0

            try:
                host = self.rawConfig['Main']['redis_host']
            except (KeyError, TypeError):
                host = 'localhost'

            try:
                port = self.rawConfig['Main']['redis_port']
            except (KeyError, TypeError):
                port = 6379

            r = redis.StrictRedis(host=host, port=port)

            # Get all frontends with dead backends
            frontends_with_deadbackends = r.keys('dead:*')

            # For each frontend with dead backends
            for f in frontends_with_deadbackends:

                # Get frontend name
                frontend = re.search('^dead:(\S*)', f).group(1)

                # Get all backends for frontend
                backends = r.lrange('frontend:{0}'.format(frontend), 0, -1)

                # Count dead backends
                dead_backends = len(r.smembers(f))

                # Sum all dead backends
                sum_of_all_dead_backends = sum_of_all_dead_backends + dead_backends

                # Check if all backends are marked dead
                if len(backends) - 1 <= dead_backends:
                    frontends_with_no_backends = frontends_with_no_backends + 1

            result['Frontends_with_no_alive_backends'] = frontends_with_no_backends
            result['Frontends_with_dead_backends'] = len(frontends_with_deadbackends)
            result['Dead_backends'] = sum_of_all_dead_backends
        except:
            result = {}
        return result
