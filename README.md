# serverdensity-plugins

### MySQLReplication
MySQLReplication plugin is useful for the monitoring of MySQL databases which
use Master-Slave (or Master-Master) replication.

Following metrices (keys) are exposed by the plugin:
* Flags (0 or 1):
    + Running
    + Slave_SQL_Running
    + Slave_IO_Running
* Integer metrices:
    + Master_Port
    + Until_Log_Pos
    + Skip_Counter
    + Relay_Log_Pos
    + Connect_Retry
* Special integer metric:
    + Seconds_Behind_Master

Serverdensity provides a few comparison methods that can be employed on plugin
keys, but (in)equality is not provided. For that reason, even when checking
'flag' metrices, one should just use 'less then 1' instead of 'not equal to 1'.
Alerts on 'integer' metrices are created normally with the threshold checks.

There is also one 'special integer metric', namely 'Seconds_Behind_Master'.
This metric has a value of nonnegative integer if the slave is running, but the
value of -1 if the slave is not running. Here one could in just have an alert
to check if the value is greater then chosen threshold value. But one can also
have a 'less then 0' alert to catch the occurances of -1 value.

All the metrices are generate via 'show slave status' MySQL command and have
the same meaning. The 'Running' flags shows if the database is reachable at
all.

#### Requirements
The plugin requires the following fields to be set in the
'/etc/sd-agent/config.cfg' file:
* mysql_server
* mysql_user
* mysql_pass

Those are the same fields that are used by the Serverdensity's built-in MySQL
monitoring alerts.


### SupervisordCheck
SupervisordCheck plugin checks if the supervisord is running. This is done by
checking if the socket file ('/var/run/supervisor.sock') exists.

The metric exposed, 'Running', can have values of either 0 or 1.
