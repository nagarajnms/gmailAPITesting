# gmailAPITesting
 Automated test cases to verify the gmail REST APIs.    
 Test cases are currently validating the GET/POST/DELETE methods and include positive and negative scenarios.   
 The tests have been automated as per pytest framework.  
 The python libraries mentioned in the requirements.txt will need to be installed.  
 A CI/CD implementation has been done via Jenkins.  
 
 Files include:  
 1. test_gmail_rest_api.py -- The test script containing the tests adhering to the pytest framework.  
 2. pytest_report.html -- The html report of the execution.
 3. requirements.txt -- Includes the Python libraries to be installed.  
 4. Logs_screenshots/  
    &emsp; complete_jenkins_logs.pdf -- Complete console logs of a Jenkins execution.  
    &emsp; Jenkins_execution.JPG -- Sample Console output.  
 5. credentials.json and token.json -- Need for authentication. I have created a test gmail account for this project and created the creds for the same. I have added these files to the gitguardian and in order to use the same by any external person, will need my permission.
  
 **Command to execute the test:**  
  pytest --capture=sys -rP .\test_gmail_rest_api.py --junitxml=.\output.xml --html=pytest_report.html  
  
  **PS:** To access the gmail APIs, we will need OAUTH2 credentials which in turn needs the clientID and clientSecret for the account.  
