import MySQLdb


class MySQLReplication(object):
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

            cursor.execute("show slave status")
            row = cursor.fetchone() or {}
        except:
            row = {}
            result = {'Running': 0}
        else:
            result = {'Running': 1}

        # convert flags to integer values 1/0
        for key in ['Slave_SQL_Running', 'Slave_IO_Running']:
            result[key] = int(row.get(key, 'No') == 'Yes')

        # if the slave is not running set the metric to -1
        key = 'Seconds_Behind_Master'
        try:
            result[key] = int(row.get(key, -1))
        except TypeError:
            result[key] = -1

        # integer values
        for key in [
                'Master_Port', 'Until_Log_Pos', 'Skip_Counter',
                'Relay_Log_Pos', 'Connect_Retry']:
            result[key] = row.get(key, -1)

        return result
