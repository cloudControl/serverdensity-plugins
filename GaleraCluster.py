import MySQLdb


class GaleraCluster(object):
    def __init__(self, agentConfig, checksLogger, rawConfig):
        self.agentConfig = agentConfig
        self.checksLogger = checksLogger
        self.rawConfig = rawConfig

    def run(self):
        try:
            db = MySQLdb.connect(
                host=self.agentConfig['MySQLServer'],
                user=self.agentConfig['MySQLUser'],
                passwd=self.agentConfig['MySQLPass'])
            cursor = db.cursor(MySQLdb.cursors.DictCursor)

            cursor.execute("show status like 'wsrep%'")
            result = self.cursor_to_dict(cursor.fetchall()) or {}
        except:
            result = {'Running': 0}
        else:
            result['Running'] = 1

        return result

    def cursor_to_dict(self, rows):
        d = {}
        metrics = ['wsrep_cluster_size']
        for l in rows:
            if l.get('Variable_name') in metrics:
                d[l.get('Variable_name')] = int(l.get('Value'), -1)
