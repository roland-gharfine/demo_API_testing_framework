import unittest
import pytest
from Lib.Framework_API import Framework_API
from Lib.Logger import Logger


class APITests(unittest.TestCase):
    # Load the framework object
    global framework
    framework = Framework_API()

    # Load the logger object
    global logger
    logger = Logger()

    @classmethod
    def setUpClass(cls):
        logger.Log("Setting up test suite...")

    @classmethod
    def tearDownClass(cls):
        logger.Log("Tearing down test suite...")

    @pytest.mark.StatusCountBySeason
    def test_Req01_TC01(self):
        """
        An unauthenticated user calling the API with a valid year (2005) should the receive the
        correct data for status "Finished".
        """

        response = framework.call_status_by_year_api("2005")
        framework.verify_response_code(response)
        framework.verify_season(response)
        framework.verify_status_element(response)

    @pytest.mark.StatusCountBySeason
    def test_Req01_TC02(self):
        """
        An unauthenticated user calling the API with a year that precedes 1950 (example: 1949)
        should receive an empty "Status" element.
        """

        response = framework.call_status_by_year_api("1949")
        framework.verify_response_code(response)
        framework.verify_season(response)
        framework.verify_status_element(response)

    @pytest.mark.Constructors
    def test_Req02_TC01(self):
        """
        An unauthenticated user should receive constructor information correctly for a valid constructor
        name they supply.
        """

        response = framework.call_constructors_api("Mercedes")
        framework.verify_response_code(response)
        framework.verify_constructor_element(response)

    @pytest.mark.Constructors
    def test_Req02_TC02(self):
        """
        An unauthenticated user should receive an empty "Constructors" element for a constructor that has
        never been in F1.
        """

        response = framework.call_constructors_api("RolandF1Team")
        framework.verify_response_code(response)
        framework.verify_constructor_element(response)

