from Lib.Logger import Logger

class Config():

    # Logger object for log file operations
    logger = Logger()

    # Configuration values dictionary
    conf = {}

    # Default configuration values dictionary
    default = {}

    def __init__(self):
        self.logger.Log("Configuring framework...")

        # Dictionary of default configuration values
        self.default = {
            "auth_type": "None",
            "log_level": 1,
            "base_url": "http://ergast.com/api/f1"
        }

        # Dictionary of user defined configuration values, overrides the default value
        self.conf = self.load_config_file()

    def get_config_value(self, param):
        """
        A method to fetch from the conf dictionary

        :param param: The name of the config parameter's key in the conf dictionary
        :return: The value of the config parameter from the conf dictionary
        """

        try:
            for key in self.conf:
                if (param == key):
                    return self.conf[param]

        except TypeError as e:
            pass

        return self.default[param]

    def load_config_file(self):
        """
        A method to load the configuration parameters form the config file TAF.conf

        :return: A dictionary containing all the configuration values
        """

        conf = {}
        try:
            with open("Conf/TAF.conf", "r") as conf_file:
                for line in conf_file:
                    if (not line.startswith("#")):
                        temp_list = line.split("=")
                        if (len(temp_list) == 2):
                            conf[temp_list[0]] = temp_list[1][:-1]

            conf_file.close()
            return conf

        except OSError as e:
            self.logger.LogError("Error code: " + str(e.errno) + ", Error message:" + e.strerror)
            pass


"""
I don't think there's much room for improvement here, maybe some simple refactoring. Having default values saves
us from advanced error handling.
"""