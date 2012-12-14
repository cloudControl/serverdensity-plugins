import os.path


class SupervisordCheck(object):
    def __init__(self, agentConfig, checksLogger, rawConfig):
        self.agentConfig = agentConfig
        self.checksLogger = checksLogger
        self.rawConfig = rawConfig

    def run(self):
        result = {'Running': 0}
        socket_file = '/var/run/supervisor.sock'
        if os.path.exists(socket_file):
            result['Running'] = 1
        return result
