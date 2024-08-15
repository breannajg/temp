# Databricks notebook source
import unittest 
import sys, os
 
def main(): 
  # Create a test loader 
  loader = unittest.TestLoader() 

  # Set the test directory
  notebook_path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
  test_dir = '/Workspace' + os.path.dirname(notebook_path)
  
  # Create a test runner that will execute the tests 
  runner = unittest.TextTestRunner(verbosity=2)
  # Load tests from each test case class
  dummy_suite = loader.discover(start_dir=test_dir, pattern='test_dummy.py')
     
  # Create a test suite combining the remaining test cases 
  combined_suite = unittest.TestSuite([
    dummy_suite,
    # TODO: Add more tests here
  ])
   
  # Run the remaining tests 
  result = runner.run(combined_suite) 
  
  # Check if there were any failures or errors in the remaining tests 
  if not result.wasSuccessful(): 
    # Optionally, you can provide more detailed error messages based on the contents of result.failures and result.errors 
    raise Exception("One or more of the tests failed. View full Traceback in Job Run") 
 
if __name__ == "__main__":
  try: 
    main() 
  except Exception as e: 
    print(str(e)) 
    sys.exit(1) # Exit with a non-zero value to indicate an error 

