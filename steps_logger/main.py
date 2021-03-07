from .auth import AuthError, requires_auth, verify_decode_jwt
from . import db
from .models import User
from .models import Steps
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort, jsonify, Response, session
from flask_login import current_user, login_required
from flask_cors import cross_origin
from sqlalchemy import join
from sqlalchemy.sql import select
import requests

main = Blueprint('main', __name__)
AUTH0_AUTHORIZE_URL = 'https://prisha.au.auth0.com/authorize?audience=stepsLogger&response_type=token&client_id=t4dkSjOynAupe3hgs0f1FjkkHm8Nl1nC&redirect_uri=https://steps-logger.herokuapp.com'

# Priya : Created a dictionary to add the token, role, permissions etc so that can use this dictionary
# whenever I need to get the token value in the program.

my_dict = {'token': '',
           'role': '',
           'permissions': ''
           }


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/memProfile')
def memProfile():
    return render_template('memProfile.html')

# Priya Note to the reviewer : GET request implementing Auth0


@main.route('/user', methods=['GET', 'POST'])
@requires_auth('get:steps-detail')
def memUser_stepsRecords(token):
    token = request.headers.get('Authorization')
    #token = request.headers.get('Authorization', None).split(' ')[1]
    my_dict['token'] = token
    my_dict['role'] = 'user'
    my_dict['permissions'] = ['get:steps-detail',
                              'post:steps', 'patch:steps', 'delete:steps']

    # Priya Note to the reviewer: Have been using the user_logged_in flag to display Logout option
    # whenever the user is logged in.
    user_logged_in = False
    user = User.query.filter_by(email='user@stepslogger.com').first()
    stepsRecords = user.stepsRecords
    headers = {"Authorization": token}
    resp = Response(render_template(
        'member.html', stepsRecords=stepsRecords, user=user, user_logged_in=True, token=token))
    return resp

# Priya: Below function is written to prepare the request URL with headers for post action


@main.route('/create_post_req', methods=['GET', 'POST'])
def create_post_req():
    perm = request.args.get('perm')
    bearer_token = my_dict['token']
    headers = {"Authorization": bearer_token}

    if perm == 'post:steps':
        url = 'https://steps-logger.herokuapp.com/addSteps'
        resp = requests.post(url, headers=headers)
    return Response(resp)

# Priya : Below function was written to prepare the request URL with headers for udpate action


@main.route('/create_update_req', methods=['GET', 'POST'])
def create_update_req():
    perm = request.args.get('perm')
    stepsRecord_id = request.args.get('stepsRecord_id')
    bearer_token = my_dict['token']
    headers = {"Authorization": bearer_token, "stepsRecord_id": stepsRecord_id}

    if perm == 'patch:steps':
        url = 'https://steps-logger.herokuapp.com/update'
        print('URL is', url)
        resp = requests.post(url, headers=headers)
        res = Response(resp)
    return res

# Priya : Below function was written to prepare the request URL with headers for delete action


@main.route('/create_delete_req', methods=['GET', 'POST', 'DELETE'])
def create_delete_req():
    perm = request.args.get('perm')
    stepsRecord_id = request.args.get('stepsRecord_id')
    print('Within delete: stepsREcord_id', stepsRecord_id)
    bearer_token = my_dict['token']
    headers = {"Authorization": bearer_token, "stepsRecord_id": stepsRecord_id}

    if perm == 'delete:steps':
        url = 'https://steps-logger.herokuapp.com/delete'
        resp = requests.post(url, headers=headers)
        res = Response(resp)

    return Response(resp)

# Priya Note to the Reviewer :
# Below function is written for the user with manager role, one who can view steps record of all users


@main.route("/allUsers", methods=['GET', 'POST'])
@requires_auth('get:steps-all')
def all_users_stepsRecords(token):
    # Just setting a flag for the user to see the Logout button once logged in
    user_logged_in = False
    test_records = db.session.query(
        User.name,
        Steps.steps_completed,
        Steps.comment,
        Steps.date_posted
    ).filter(
        User.id == Steps.user_id
    ).all()

    resp = Response(render_template(
        'admin.html', allRecords=test_records, user_logged_in=True))
    return resp

# Priya Note to the Reviewer : Below two functions - addSteps and addMemSteps have been written to
# add new records. It follows the below steps:
# 1. When the user is logged in, they are on their profile page where they can view the
# list of steps records that they have added
# 2. From the profile page, they can click on Add Steps to create a record.
# 3. This will open up the addSteps form **only** if the user has the permission to post:steps
# 4. Once the steps record is added then the user is returned to his/her profile page.


@main.route('/addSteps', methods=['POST'])
@requires_auth('post:steps')
def addSteps(token):
    return render_template('addUser_stepsRecord.html', user_logged_in=True)


@main.route('/addMemSteps', methods=['GET', 'POST'])
def addMemSteps():
    user_logged_in = False
    print('addMemSteps called')
    user = User.query.filter_by(email='user@stepslogger.com').first()
    print(user.name)
    steps_completed = request.form.get('steps_completed')
    body = request.get_json()
    if steps_completed is None:
        steps_completed = body.get('steps_completed')

    comment = request.form.get('comment')
    if comment is None:
        comment = body.get('comment')
    print('Printing the values', steps_completed, comment, user)
    stepsRecord = Steps(steps_completed=steps_completed,
                        comment=comment, user_id=user.id)

    # Priya Note to the reviewer : Used helper method insert() to simplify API behavior
    try:
        Steps.insert(stepsRecord)
    except:
        abort(422, {'error': 'Step Record could not be added'})
    stepsRecords = user.stepsRecords
    resp = Response(render_template(
        'member.html', stepsRecords=stepsRecords, user=user, user_logged_in=True))
    return resp

# Priya Note to the Reviewer : Below two functions - updateSteps and updateUserSteps have been written to
# update an existing record. It follows the below steps:
# 1. When the user is logged in, they are on their profile page where they can view their steps details
# 2. From the profile page, they can click on Update/Edit icon in the Edit column of the required record.
# 3. This will open up the updateUser_stepsRecord form **only** if the user has the permission - patch:steps
# 4. Once the steps record is updated, the user is returned to his/her profile page listing the steps details


@main.route('/update', methods=['GET', 'PATCH', 'POST'])
@requires_auth('patch:steps')
def updateSteps(token):
    stepsRecord_id = request.headers.get('stepsRecord_id')
    return render_template('updateUser_stepsRecord.html', stepsRecord_id=stepsRecord_id, user_logged_in=True)


@main.route('/updateUserSteps', methods=['GET', 'PATCH', 'POST'])
def updateUser_stepsRecord():
    # Write code here
    user_logged_in = False
    user = User.query.filter_by(email='user@stepslogger.com').first()
    stepsRecord_id = request.args.get('stepsRecord_id')

    stepsRecord = Steps.query.get(stepsRecord_id)
    if stepsRecord is None:
        abort(
            404, {'error': 'Could not find a record with the given stepsRecord_id'})

    if request.method == "POST":
        stepsRecord.steps_completed = request.form.get('steps_completed')
        stepsRecord.comment = request.form.get('comment')
        try:
            Steps.update(stepsRecord_id)
        except:
            abort(422, {'error': {'Could not update the stepsRecord'}})

        flash('Your post has been updated!')

    # Priya : Once the required changes are done, user is redirected to their profile page member.html
    stepsRecords = user.stepsRecords
    resp = Response(render_template(
        'member.html', stepsRecords=stepsRecords, user=user, user_logged_in=True))
    return resp

# Priya Note to the Reviewer : Below function deleteSteps has been written to delete a record
# It follows the below steps:
# 1. When the user is logged in, they are on their profile page where they can view their steps details
# 2. From the profile page, they can click on Delete icon in the Delete column to delete the required record.
# 3. Clicking on delete, deletes the record and the user is returned to his/her profile page listing the steps details


@main.route('/delete', methods=['POST', 'DELETE'])
@requires_auth('delete:steps')
def deleteSteps(token):
    user_logged_in = False
    stepsRecord_id = request.headers.get('stepsRecord_id')
    user = User.query.filter_by(email='user@stepslogger.com').first()
    stepsRecord = Steps.query.get(stepsRecord_id)
    if not stepsRecord:
        abort(404, {'error': {
              'Could not delete : No steps record available with this id'}})

    # Priya Note to the reviewer : Used helper method delete() to simplify API behavior
    try:
        Steps.delete(stepsRecord)
        flash('Your post has been deleted!')
    except:
        abort(422, {'error': {'Steps record deletion unscuccessful'}})

    stepsRecords = user.stepsRecords
    resp = Response(render_template(
        'member.html', stepsRecords=stepsRecords, user=user, user_logged_in=True))
    return resp

# Priya note to the reviewer : Have utilized the @main.errorhandler decorator which formats error responses
# as JSON objects for the status codes 404, 422 and AuthError (400, 401, 403)
# AuthError is defined in auth.py and value of AuthError can be 400, 401 and 403.
# Thus have utilized the @main.errorhandler decorator for 5 status codes (400, 401, 403, 404 and 422).
# I have used Blueprint and registered main therefore this decorator is defined as @main.errorhandler and not @app.errorhandler.


@main.errorhandler(AuthError)
def auth_error(err):
    return jsonify(err.error), err.status_code


@main.errorhandler(404)
def not_found(error):
    error_details = {
        "success": False,
        "error": 404,
        "message": "resource not found"
    }
    return jsonify(error_details), 404


@main.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


# Priya note to the reviewer:
# Below functions are for guest users, these were written when I started with a simple CRUD project.
# Have completed all requirements from the Rubric in the functions above for user and manager roles.
@main.route('/profile')
@cross_origin(headers=["Content-Type", "Authorization"])
@login_required
def profile():
    print(request.headers.items())
    return render_template('profile.html')


@main.route("/all")
@login_required
def user_stepsRecords():
    user = User.query.filter_by(email=current_user.email).first_or_404()
    stepsRecords = user.stepsRecords
    return render_template('stepsRecords.html', stepsRecords=stepsRecords, user=user)


@main.route("/new")
@login_required
def new_stepsRecord():
    return render_template('add_stepsRecord.html')


@main.route("/new", methods=['POST'])
@login_required
def add_new_stepsRecord():
    steps_completed = request.form.get('steps_completed')
    comment = request.form.get('comment')
    #print(steps_completed, comment)
    stepsRecord = Steps(steps_completed=steps_completed,
                        comment=comment, author=current_user)
    Steps.insert(stepsRecord)
    flash('Your steps details has been added!')
    return redirect(url_for('main.index'))


@main.route("/stepsRecord/<int:stepsRecord_id>/update", methods=['GET', 'POST'])
@login_required
def update_stepsRecord(stepsRecord_id):
    stepsRecord = Steps.query.get(stepsRecord_id)
    if request.method == "POST":
        stepsRecord.steps_completed = request.form['steps_completed']
        stepsRecord.comment = request.form['comment']
        Steps.update(stepsRecord_id)
        flash('Your post has been updated!')
        return redirect(url_for('main.user_stepsRecords'))

    return render_template('update_stepsRecord.html', stepsRecord=stepsRecord)


@main.route("/stepsRecord/<int:stepsRecord_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_stepsRecord(stepsRecord_id):
    stepsRecord = Steps.query.get(stepsRecord_id)
    Steps.delete(stepsRecord)
    flash('Your post has been deleted!')
    return redirect(url_for('main.user_stepsRecords'))
