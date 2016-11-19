import unittest
import glob
import logging


# Class to test all the tests
class TestTests():
    results = []
    def __init__(self):
        pass


    def run_all_tests(self):
        test_files = glob.glob('test*.py') #grabs all the test files to be used
        module_strings = [test_file[0:len(test_file) - 3] for test_file in test_files]
        suites = [unittest.defaultTestLoader.loadTestsFromName(test_file) for test_file in module_strings]
        test_suite = unittest.TestSuite(suites)
        test_result_obj = unittest.TextTestRunner().run(test_suite)
        logging.info("test results output :|||" )
        return self.results
