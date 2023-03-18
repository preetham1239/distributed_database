# Run Instructions

* Before running, the database.yaml and config.yaml files should be set up with the correct host values, username and password
* And also, three databases and the database and table names should be set in the database.yaml file as created in the database
* First run, lock_manager.py 
* Then run, coordinator.py
* Later run, app.py
* Run get_test1.py and get_test2.py to test the GET requests
* Run put_test1.py and put_test2.py to test the PUT requests
* Any other queries can be run by changing the query in the test files
* A bug had been introduced due to the flask framework, so flag value in key.txt should be set to 0 before running anything. We were unable to resolve the bug, so we set this as a temporary solution