import unittest
import glob
import logging
import StringIO


# Class to test all the tests
class TestTests():
    results = []

    def __init__(self):
        pass


    def run_all_tests(self):
        my_stream = StringIO.StringIO()

        test_files = glob.glob('test*.py') #grabs all the test files to be used
        module_strings = [test_file[0:len(test_file) - 3] for test_file in test_files]
        print test_files
        logging.info(test_files)
        suites = [unittest.defaultTestLoader.loadTestsFromName(test_file) for test_file in module_strings]
        test_suite = unittest.TestSuite(suites)
        test_results = unittest.TextTestRunner(stream=my_stream).run(test_suite)

        print "FILE"
        print my_stream.getvalue()
        print
        print test_suite
        print "RESULTS"
        print test_results.errors
        print test_results.failures
        print test_results.testsRun


        #self.results = test_result_obj.test
        logging.info( test_results.testsRun)
        return self.results


if  __name__ =='__main__':
    TestTests().run_all_tests()
