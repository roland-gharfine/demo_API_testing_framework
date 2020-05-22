import requests
from requests.auth import *
import urllib.parse
import inspect
from Lib.Data import Data
from Lib.Config import Config
from Lib.Logger import Logger
import json

def get_test_case_name():
    # Get the name of the function that called the previous function from the stack. Contrived, but it works...
    return inspect.stack()[2].function.replace("test_", "")

class Framework_API():

    # Logger object for log file operations
    logger = Logger()

    # Data object to handle test data
    data = Data()

    # Config object to configure the framework from a file and a set of default values
    config = Config()

    # Authentication type for the API to be called
    auth_type = ""

    # Base URL to be called
    base_url = ""

    def __init__(self):
        self.logger.Log("Starting framework...")
        self.auth_type = self.config.get_config_value("auth_type")
        self.base_url = self.config.get_config_value("base_url")

    def call_api(self, method, route, args=None, auth_type=None):
        argsURL = ""
        if (route is None):
            self.logger.LogError("API route cannot be empty!!")
        if (args is not None):
            if (method == "get"):
                argsURL = "?"
                argsTab = args.split("|")
                for arg in argsTab:
                    argsURL += urllib.parse.quote_plus(arg, safe="=")
                    argsURL += "&"
                argsURL = argsURL[:-1]  # Trim trailing &
        else:
            args = ""
            argsURL = ""

        auth = None
        if(auth_type is not None):
            if(auth_type == "basic"):
                auth = HTTPBasicAuth('', '')
                # TODO: Implement OAuth and API key

        response = ""
        if (method == "get"):
            response = requests.get(self.base_url + route + argsURL,
                                    auth=auth)
            self.data.print_all_rows()

        elif (method == "post"):
            response = requests.post(self.base_url + route, auth=HTTPBasicAuth('', ''),
                                     data=args)
        elif (method == "put"):
            response = requests.put(self.base_url + route, auth=HTTPBasicAuth('', ''),
                                    data=args)
        elif (method == "del" or method == "delete"):
            response = requests.delete(self.base_url + route, auth=HTTPBasicAuth('', ''),
                                    data=args)
        else:
            self.logger.LogError("Unknown or unsupported HTTP method!!")

        self.logger.Log("Executing API Call: " + method.upper() + " " + response.url)
        self.logger.Log("Result: status_code=" + str(response.status_code) + ", response_body=" + response.text)

        return response

    def call_status_by_year_api(self, year):
        """
        A keyword for abstraction of test cases. Corresponding test suite tag is "StatusCountBySeason".

        :param year: The year to include in the API call.
        :return: the response returned by the API caller in this class.
        """

        self.logger.Log("Executing test case " + get_test_case_name())
        return self.call_api("get", "/" + year + "/status.json")

    def call_constructors_api(self, constructor):
        """
        A keyword to call the constructors API.

        :param constructor: The name of the constructor to fetch info for.
        :return: the response returned by the API caller in this class.
        """

        self.logger.Log("Executing test case " + get_test_case_name())
        return self.call_api("get", "/constructors/" + constructor + ".json")

    def verify_response_code(self, response):
        """
        A keyword to verify response status code corresponds to expected results from the test data CSV file.

        :param response: The response object from the API call.
        :return: True for passing tests, False for failing tests.
        """

        test_case = get_test_case_name()
        assert response.status_code == int(self.data.get_test_data(test_case)["status_code"])

    def verify_status_element(self, response):
        """
        A keyword to verify the status element returned by the status API call corresponds to the expected results
        from the test data CSV file.

        :param response: The response object from the API call.
        :return: True for passing tests, False for failing tests.
        """

        # Get the test case name
        test_case = get_test_case_name()

        # Get the status element from the API response
        status_element_from_response = self.data.json_decode(response.text)["MRData"]["StatusTable"]["Status"]

        # Get the status element from the test data
        status_element_from_test_data = self.data.get_test_data(test_case)["Status"]

        # Either the status we're testing for is contained in the response, or both are empty.
        # Otherwise fail the test.
        assert (status_element_from_test_data in status_element_from_response) \
            or (status_element_from_test_data == status_element_from_response)

    def verify_constructor_element(self, response):
        """
        A keyword to verify the constructor element returned by the status API call corresponds to the expected results
        from the test data CSV file.

        :param response: The response object from the API call.
        :return: True for passing tests, False for failing tests.
        """

        # Get the test case name
        test_case = get_test_case_name()

        # Get the constructors element from the API response
        constructors_element_from_response = self.data.json_decode\
            (response.text)["MRData"]["ConstructorTable"]["Constructors"]

        # Get the constructors element from the test data
        constructors_element_from_test_data = self.data.get_test_data(test_case)["Constructors"]

        # Either the constructors element we're testing for is contained in the response, or both are empty.
        # Otherwise fail the test.
        assert (constructors_element_from_test_data in constructors_element_from_response) \
            or (constructors_element_from_test_data == constructors_element_from_response)

    def verify_season(self, response):
        """
        A keyword to verify the season returned by the API call corresponds to the expected result from the test data
        CSV file.

        :param response: The response object from the API call.
        :return: True for passing tests, False for failing tests.
        """

        # Get the test case name
        test_case = get_test_case_name()

        # Get the season from the APi response
        season_from_response = self.data.json_decode(response.text)["MRData"]["StatusTable"]["season"]

        # Get the season from test data
        season_from_test_data = self.data.get_test_data(test_case)["season"]

        assert season_from_test_data == season_from_response


"""
Given more time I would ideally add support for all possible formats without having to specify the exact
URL in the test case. A configuration parameter or the test data can specify the format.

For example instead of adding ".json" to the end of the URL we could just add format=JSON in TAF.conf, or read 
it from the test data field.

Finally, some refactoring is always a good idea. Especially the part where I'm fetching the json data
from response and from test data, I feel it could use some optimization.
"""
