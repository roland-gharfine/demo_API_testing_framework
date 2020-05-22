import datetime


def get_timestamp():
    return datetime.datetime.now().strftime("%H:%M:%S")


def get_date():
    return datetime.date.today().strftime("%Y%m%d")


class Logger():

    def __init__(self):
        self.Log("Logger intiialized for class")

    def LogError(self, err_msg):
        """
        A method for error logging, logs the message in a separate file specific for errors. Writes the
        current date and time at the beginning of the line.

        :param err_msg: The error message to be logged in the error log file
        :return: None
        """

        timestamp = get_timestamp()
        date = get_date()
        fh = open("Logs/TAF_" + date + ".error.log", "a")
        fh.write(timestamp + "," + err_msg + "\n")
        fh.close()

    def Log(self, msg):
        """
        A method for regular logging, logs the message in a separate file specific for informational
        messages. Writes the current system time at the beginning of the line.

        :param msg: The message to log in the regular log file, generally of informational nature
        :return: None
        """

        timestamp = get_timestamp()
        date = get_date()
        fh = open("Logs/TAF_" + date + ".default.log", "a")
        fh.write(timestamp + "," + msg + "\n")
        fh.close()


"""
Given more time, I would have liked to make the following configurable parameters:
The log folder location, the log files date and time format, the carriage return, and the field delimiters.
Ideally some logs can be saved in a standard format as well, for later graphical use (XML or JSON).

Implementing the log levels which are already defined in the conf file would be a plus.
Suggested implementation:
trace =3 log everything, requests and responses, and errors
info =2 log only requests and status codes and errors
warn =1 log only requests and errors
error =0 only log pass or fail and errors
"""