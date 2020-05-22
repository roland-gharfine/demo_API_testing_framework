
"""
Ideally I would have liked to implement a class for custom reporting below.
For the purposes of this project, I used pytest's html report capability.
This file is just an example showing that I would isolate this feature from the framework.
This separate reporting module could allow for isolated modification of pytest reporting.
For example, using this code below to change the title:

import pytest
from py.xml import html

def pytest_html_report_title(report)
   report.title = "API Regression Testing Suite Report"

"""

class Reporter():
    def __init__(self):
        raise Exception("Not implemented!!")