import csv
import json
from Lib.Logger import Logger



class Data():

    logger = Logger()
    test_data = {}

    def __init__(self):
        self.logger.Log("Initializing data parser...")

        # Read the test data from the CSV file
        with open('Data/test_data.csv') as csvfile:
            self.reader = csv.reader(csvfile)

            # Skip the first line (header)
            next(self.reader)

            for row in self.reader:
                self.add_test_data(row)

    def print_all_rows(self):
        """
        A method to log all CSV data rows. For internal use (debugging).

        :return: None
        """

        self.logger.Log(str(self.test_data))

    def add_test_data(self, row):
        """
        A method to fill the test_data dictionary.

        :param row: The row from the CSV test data file.
        :return: None
        """

        # Build the test data dictionary
        self.test_data[row[0]] = {"season": row[1], "format": row[2], "status_code": row[3]}

        # Status element in test data is either a dictionary, or an empty list, to go with the API response model.
        if (row[4]!= "" and row[5] != "" and row[6] != ""):
            self.test_data[row[0]]["Status"] = {"statusId": row[4], "count": row[5], "status": row [6]}
        else:
            self.test_data[row[0]]["Status"] = []

        # Constructors element in test data is either a dictionary, or an empty list, to go with the API response model.
        if (row[7]!= "" and row[8] != "" and row[9] != "" and row[10] != ""):
            self.test_data[row[0]]["Constructors"] = \
                {
                    "constructorId": row[7],
                    "url": row[8],
                    "name": row[9],
                    "nationality": row[10]
                }
        else:
            self.test_data[row[0]]["Constructors"] = []

    def get_test_data(self, test_case):
        """
        A method to return the test data for a specific test case.

        :param test_case: The identifier for the test case we're fetching data for. Should follow clear naming
        conventions.
        :return: The test data element corresponding to the test case, from the data object's test_data
        dictionary.
        """

        return self.test_data[test_case]

    def json_decode(self, json_data):
        """
        A method to parse json data and return a dictionary.

        :param json_data: data in the json format.
        :return: a parsed version of the json_data as a dictionary.
        """

        return json.loads(json_data)


"""
Given more time I would have made the CSV file format configurable, to allow for parsing different data files
with the same framework. Database support would also have been an interesting addition, to allow us to fetch 
test data from a database.

Adding a json decode method would also be a plus.

PS: we are not catching the exception in case the test_data.csv file is not present on purpose, we want the 
test run to fail and not execute in case test data is not available.
"""