# Project Description
The project - Steps Logger  is a web based application with which one can track or keep a record of the number of steps that they have taken on a daily basis.
One can add as many records of steps taken on a particular day.
All CRUD operations - Create a record, Read or view the steps records, Update or edit the steps records and Delete their steps records is possilbe using the steps logger.

**Application URL :: https://steps-logger.herokuapp.com/**

### __Priya's note to the reviewer wr.r.t. the project:__
The application has two parts to it.
When you open up the main page : at the top left you would see three tabs : **Signup, User Login and Member Login**

##### Part 1 : Demo of Usage : Signup and User Login Tabs
Signup and User Login tabs lets you signup an account for yourself and demonstrates how you can login with the account created and  how you can use the application to record the steps taken and perform all the CRUD operations. This part **does not** have any RBAC auth0 authentication setup. This is purely for one to understand how to use the appliction. 
__Request the reviewer to please sign up 2 accounts user and admin with the credentials listed under '**Reviewer Needs to**' in order to test the application__

##### Part 2 : Member Login with Auth0 Authentication and RBAC implementation
There are two users created in Auth0 for this application : 
1. Admin :
    user name : admin@stepslogger.com, 
    role associated : admin, 
    permissions : get:steps-all (Lists steps record of **all users**)

2. User : 
    user name : user@stepslogger.com, 
    role associated : user, 
    permissions : **all CRUD operations**
        a. get:steps-detail(Lists all records of the **logged in** user)
        b. post:steps(Allows User to add their own record)
        c. patch:steps(Let's user edit the record)
        d. delete:steps(Lets user delete a record)

**The reviewer needs to**
1. **Sign up** with the listed email id and password below for the 2 accounts admin and user. Please use the exact credentials listed below since I have created the same users with the login credentials in Auth0 for my project.
2. Login to the each of the accounts by clicking the **Member Login** tab to check and verify auth0 authentication and RBAC implementation.


Login details:
1. admin :
    Login id : admin@stepslogger.com
    Password : Steps@1234

2. user :
    Login id : user@stepslogger.com
    Password : Steps@1234

    ###### __Priya's note to the reviewer__
    On clicking Member Login tab - you will see the Auth0 interface.
        a. Login as admin or user.
        b. On successful login, you will see the Member logged in page where the token that was generated would be in the text box. Have coded such that the token is captured from the browser and placed in the text box. 
        c. You can copy the token from the text box and open up jwt.io and  paste the token there to verify if the permissions have been set correctly or not. After you have verified, you can click on the Proceed button to review the project further i.e. test the endpoints.        
        d. **Only the admin** can view steps records of all users
        e. **Only the user** can perform **all CRUD operations** against their respective records.

## Motivation for the project
Because of Corona, we all have been restricted to stay at home. 
Lack of exercise has taken a toll on my health. Was asked by my doctor to ensure I walk 10,000 steps in a day and aim to reduce weight.
Instead of manually recording my steps on a daily basis, wanted to develop an application similar to pushups logger on Google play which will record the steps on a daily basis that I can review and take required measures for a healthy weight loss.
Wanted to do a pet project for myself from scatch therefore decided to develop this project and ensured that this project includes all requirements of the Capstone project. 

## Project dependencies, local development and hosting instructions
1. Reviewer needs to : first open the web application :  https://steps-logger.herokuapp.com/ and signup for the two accounts user and admin with the credentials provided below.
2. For reviewing the project locally:
    a. Comment the line : db_drop_and_create_all() in the file : __init__.py
    b. Replace all instances of https://steps-logger.herokuapp.com/ with 'http://localhost:5000/
    b. From the project folder (capstone), run 
        1. 'pip install -r requirements.txt'
        2. export FLASK_APP=steps_logger
        3. export FLASK_DEBUG=1
        4. flask run --host 0.0.0.0 --port 5000
        __Priya note to the reviewer : I give the host as '0.0.0.0' since am running my application on a Unix guest VM with a Windows host__     
 


## Detailed instructions for scripts to install any project dependencies, and to run the development server.
__Priya Note to the reviewer__
i. Used pipreqs to create the requirements.txt file
ii. For Testing :
    a. Please open the below link (twice for each of the two users - user and admin, giving a gap of 2 mins ) in the browser:
    https://prisha.au.auth0.com/authorize?audience=stepsLogger&response_type=token&client_id=qXot7M1Z3VlF5e3cHMg7IAXzDHDNYJdK&redirect_uri=https://steps-logger.herokuapp.com/memProfile
    Take the token from the browser url and add these tokens in bearer_token in config file for the keys user and admin.
    b. Another easier approach would be clicking on Member Login tab on the top right corner and logging in with the credentials provided 


## Documentation of API behavior and RBAC controls 
#### There are 2 roles for this application :
1. User - one who can perform all the CRUD operations w.r.t. the specific user
2. Admin - one who can view steps record of all users 

The two roles have separate permissions associated with them.
User : get:steps-detail, post-steps, patch-steps and delete-steps
Admin : get:steps-all

#### Endpoint Details:
User: 
    a. /user, permissions : get:steps-detail
    b. /addSteps, permissions : post:steps
    c. /update, permissions : update:steps
    d. /delete, permissions : delete:steps

Admin:
    a. /allUsers, permissions " get:steps-all

#### RBAC control:
An EP is called in the following example format:
@main.route("/allUsers", methods=['GET', 'POST'])
@requires_auth('get:steps-all')
def all_users_stepsRecords(token):

1. @main.route("/allUsers", methods=['GET', 'POST'])
    The bearer token is passed in the headers, so whenever a request is created for each of the endpoint listed above - headers is sent as well, actually headers have to be sent.
    For example : For the endpoint /allUsers for the role of Admin the request is created as below:
        url = 'http://localhost:5000/allUsers'
        headers = {"Authorization": **bearer_token**} #Bearer_token is the jwt token with Bearer word prefixed
        **resp = requests.post(url, headers=headers)** 
        res = Response(resp)

2. @requires_auth('get:steps-all)
    The requires_auth decorator is used for the EP /allUsers. This method in turn calls the following methods:
    a. get_token_auth_header() - This method takes the token from the header, if token is provided in the header, token has the prefix Bearer. The method returns the token without the Bearer prefix
    b. verify_decode_jwt(token) - This method decodes the token, retrieves the payload, verifies the token 
    to check for the validitiy,claims and expiry. Returns the payload.
    c. check_permissions(permission, payload) - This method will check if the permissions passed as argument to the @requires_auth exists in the payload and returns True or False, thus completing the authentication verification

#### Description of Endpoints
1. /allUsers -
    Request type : GET
    Permissions : 'get:steps-all'
    Role : Admin
    Requirement : Should send token in headers, token should contain the required permission
    Result : Details of Steps Record for all users
    Response : Status Code
        a. 200 - SUCCESS : the request was successful
        b. 401 - ERROR : Authroization Header is missing
        c. 403 - ERROR : Forbidden, doesn't have the required permissions
        d. 422 - ERROR : Request was unprocessable.

2. /user - 
    Request type : GET
    Permissions : 'get:steps-all'
    Role : User
    Requirement : Should send token in headers, token should contain the required permission
    Result : Details of Steps Record for the loged in user
    Response : Status Code
        a. 200 - SUCCESS : the request was successful
        b. 401 - ERROR : Authroization Header is missing
        c. 403 - ERROR : Forbidden, doesn't have the required permissions
        d. 422 - ERROR : Request was unprocessable.

3. /addSteps -
    Request type : POST
    Permissions : 'post:steps'
    Role : User
    Requirement : Should send token in headers, token should contain the required permission
    Result : New steps record is added for the logged in user
    Response : Status Code
        a. 200 - SUCCESS : the request was successful
        b. 401 - ERROR : Authroization Header is missing
        c. 403 - ERROR : Forbidden, doesn't have the required permissions
        d. 422 - ERROR : Request was unprocessable.

4. /update
    Request type : PATCH
    Permissions : 'update:steps'
    Role : User
    Requirement : Should send token in headers, token should contain the required permission
    Result : Existing steps Record is updated for the logged in user
    Response : Status Code
        a. 200 - SUCCESS : the request was successful
        b. 401 - ERROR : Authroization Header is missing
        c. 403 - ERROR : Forbidden, doesn't have the required permissions
        d. 422 - ERROR : Request was unprocessable.

5. /delete
    Request type : DELETE
    Permissions : 'update:steps'
    Role : User
    Requirement : Should send token in headers, token should contain the required permission
    Result : Existing steps Record is updated for the logged in user
    Response : Status Code
        a. 200 - SUCCESS : the request was successful
        b. 401 - ERROR : Authroization Header is missing
        c. 403 - ERROR : Forbidden, doesn't have the required permissions
        d. 422 - ERROR : Request was unprocessable.

#### Testing Endpoints : 
Priya Note to the Reviewer : 
    1. Have created the test_stepsLogger.py for testing the endpoints
    2. Before running this test, please replace the token in config file with the token that you get when running the application.
    3. In addition, it would be good if you commented out test for admin while testing for user and vice versa
    Have tested it to work even without commenting the tests, but sometimes it gives error, am guessing
    it is because of token expiring

##### TEST Results: Passed results
pv252n:capstone :~$ python test_stepsLogger.py
/home/pv252n/.local/lib/python3.5/site-packages/Crypto/Util/_raw_api.py:32: PendingDeprecationWarning: the imp module is deprecated in favour of importlib; see the module's documentation for alternative uses
  import imp
...........
----------------------------------------------------------------------
Ran 11 tests in 2.484s

OK
pv252n:capstone :~$



## Additional Details
Priya Note to the Reviwer:
In addition to the requirements in the Rubric, listing further details here
### **Links referred :**
    1. www.pushupslogger.com
	2. https://flask.palletsprojects.com/en/1.1.x/tutorial/
	3. For Flask's Blueprint : https://flask.palletsprojects.com/en/1.1.x/blueprints/
	4. render_template : https://flask.palletsprojects.com/en/1.1.x/quickstart/
	5. Template inheritance : https://flask.palletsprojects.com/en/1.1.x/patterns/templateinheritance/
	6. Function url_for : https://flask.palletsprojects.com/en/1.1.x/api/#flask.url_for
	7. SQLite3 : https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/#using-sqlite-3-with-flask
	8. For hashing the password during sign up and verifying the hashed password : 
		a. https://www.programcreek.com/python/example/82817/werkzeug.security.generate_password_hash
		b. https://www.programcreek.com/python/example/58659/werkzeug.security.check_password_hash
    9. README file creation : 
        https://medium.com/@saumya.ranjan/how-to-write-a-readme-md-file-markdown-file-20cb7cbcd6f

### **Questions asked in Udacity's knowledge centre:**
1. https://knowledge.udacity.com/questions/499406
2. https://knowledge.udacity.com/questions/501346

### Priya's diary of roadblocks, Challenges faced during development and the links referred to for solution
1. When I click on Member login tab, the link "https://prisha.au.auth0.com/authorize?audience=stepsLogger&response_type=token&client_id=t4dkSjOynAupe3hgs0f1FjkkHm8Nl1nC&redirect_uri=https://steps-logger.herokuapp.com" should be hit and the resulting token should be retrieved and added in the token text box provided in the memProfile.html file.
__Checked extensively and finally landed upon a stackoverflow solution which explained the use of window.location and document.getElementbyID functions, based on which wrote the below javascript function:__
        <script type="text/javascript">
          var token = new URL(window.location).hash.split('&').filter(function (el) { if (el.match('access_token') !== null) return true; })[0].split('=')[1];
          document.getElementById("token").setAttribute('value', token);  
        </script>

2. How to create a request to include token in the headers : read about requests, flask's request and many other modules and finally was able to create a request in the following format:
resp = requests.post(url, headers=headers)
An example :
    url = 'https://steps-logger.herokuapp.com/allUsers'
    headers = {"Authorization": bearer_token}
    resp = requests.post(url, headers=headers)
    res = Response(resp)
Links referred : https://stackoverflow.com/questions/10768522/python-send-post-with-header 

3. How to display the name of the user in the all users steps record report when you login as admin..
Steps table contained the foreign key user_id which was the primary key in the User table. I needed to write the query in SQLAlchemy to display the user name instead of id. 
Link referred : https://stackoverflow.com/questions/6044309/sqlalchemy-how-to-join-several-tables-by-one-query

**Priya Note to the Reviewer**
__Have listed only 3 challenges among the many challenges and roadblocks that I faced. These took atleast 2 days for me to find the solution :-) , therefore am adding them here__





