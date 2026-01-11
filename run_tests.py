import unittest
import sys
import os
from modules import logger

def run_tests():
    # Configure logging for tests
    test_log = "tests/test_run.log"
    if os.path.exists(test_log):
        os.remove(test_log)
    
    # Initialize the logger with the test log file
    logger.setup_logger("ACRD", log_file=test_log)
    
    loader = unittest.TestLoader()
    suite = loader.discover('tests')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if not result.wasSuccessful():
        sys.exit(1)

if __name__ == '__main__':
    run_tests()
