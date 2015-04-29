import ConfigParser
import xmlrpclib

from supervisor import xmlrpc


def get_supervisor_config():
    config = ConfigParser.ConfigParser()
    cfg = {'host': 'http://127.0.0.1'}
    try:
        config.read('/etc/supervisord.conf')
        cfg['socket'] = config.get('supervisorctl', 'serverurl')
        cfg['username'] = config.get('supervisorctl', 'username')
        cfg['password'] = config.get('supervisorctl', 'password')
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
        raise Exception('Failed to parse supervisor config')
    return cfg


class SupervisorProcessCheck(object):
    def __init__(self, agentConfig, checksLogger, rawConfig):
        self.agentConfig = agentConfig
        self.checksLogger = checksLogger
        self.rawConfig = rawConfig

    def run(self):
        cfg = get_supervisor_config()
        transport = xmlrpc.SupervisorTransport(
            cfg['username'], cfg['password'], cfg['socket'])
        proxy = xmlrpclib.ServerProxy(cfg['host'], transport=transport)

        result = {'all_running': True}
        for p in proxy.supervisor.getAllProcessInfo():
            if p['statename'] != 'RUNNING':
                result['all_running'] = False
                break

        return result


if __name__ == '__main__':
    spc = SupervisorProcessCheck(None, None, None)
    print(spc.run())
