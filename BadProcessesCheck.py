from subprocess import Popen, PIPE


class BadProcessesCheck(object):
    def __init__(self, agentConfig, checksLogger, rawConfig):
        self.agentConfig = agentConfig
        self.checksLogger = checksLogger
        self.rawConfig = rawConfig

    def run(self):
        try:
            blacklist = self.rawConfig['Main']['blacklist'].split(' ')
        except (KeyError, TypeError):
            blacklist = ['miner']

        num = 0
        result = {'BadProcessesRunning': num}
        for p in blacklist:
            process = Popen(['pgrep', p], stdout=PIPE, stderr=PIPE)
            pids, notused = process.communicate()
            num += len(pids.split('\n')) - 1

        result['BadProcessesRunning'] = num
        return result
