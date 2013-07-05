import redis
import re


class HipacheBackends(object):

    def __init__(self, agentConfig, checksLogger, rawConfig):
        self.agentConfig = agentConfig
        self.checksLogger = checksLogger
        self.rawConfig = rawConfig

    def run(self):
        sum_dead_backends = 0
        sum_frontends_with_no_backends = 0
        sum_frontends_with_deadbackends = 0
        sum_locked_backends = 0
        try:
            try:
                host = self.rawConfig['Main']['redis_host']
            except (KeyError, TypeError):
                host = 'localhost'

            try:
                port = int(self.rawConfig['Main']['redis_port'])
            except (KeyError, TypeError):
                port = 6379

            r = redis.StrictRedis(host=host, port=port)

            # Get all frontends with dead backends
            frontends_with_deadbackends = r.keys('dead:*')
            sum_frontends_with_deadbackends = len(frontends_with_deadbackends)

            # Get all hchecker locked backends
            sum_locked_backends = len([lb for lb in r.hgetall('hchecker') if re.match('\S+:\d+;\S+#\d+', lb)])

            # For each frontend with dead backends
            for f in frontends_with_deadbackends:

                # Get frontend name
                frontend = re.search('^dead:(\S*)', f).group(1)

                # Count all backends for frontend
                backends = len(r.lrange('frontend:{0}'.format(frontend), 0, -1)) - 1

                # Count dead backends for frontend
                dead_backends = len(r.smembers(f))

                # Sum all dead backends
                sum_dead_backends = sum_dead_backends + dead_backends

                # Check if all backends are marked dead for given frontend
                if backends <= dead_backends:
                    sum_frontends_with_no_backends = sum_frontends_with_no_backends + 1

        except Exception as e:
            self.checksLogger.error('HipacheBackends failed to collect data: {}'.format(e))
            sum_dead_backends = -1
            sum_frontends_with_no_backends = -1
            sum_frontends_with_deadbackends = -1
            sum_locked_backends = -1

        result = {}
        result['Frontends_with_no_alive_backends'] = sum_frontends_with_no_backends
        result['Frontends_with_dead_backends'] = sum_frontends_with_deadbackends
        result['Dead_backends'] = sum_dead_backends
        result['Hchecker_locked_backends'] = sum_locked_backends

        return result
