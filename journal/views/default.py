import os
import datetime
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import MyModel


# HERE = os.path.dirname(__file__)

# ENTRIES = [
#     {"title": "LJ - Day 10", "date": "Aug 19, 2016", "id": 10, "body": "Sample body text."},
#     {"title": "LJ - Day 11", "date": "Aug 22, 2016", "id": 11, "body": "Sample body text."},
#     {"title": "LJ - Day 12", "date": "Aug 23, 2016", "id": 12, "body": "Sample body text."},
# ]


@view_config(route_name='home', renderer='templates/home.jinja2')
def home(request):
    try:
        query = request.dbsession.query(MyModel)
        entries = query.all()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {"entries": entries}


@view_config(route_name='detail', renderer='templates/detail.jinja2')
def detail(request):
    try:
        query = request.dbsession.query(MyModel)
        entry = query.filter(MyModel.id == request.matchdict["id"]).first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {"entry": entry}


@view_config(route_name='create', renderer='templates/create.jinja2', permission='secret')
def create(request):
    if request.method == "POST":
        new_title = request.POST["title"]
        new_body = request.POST["body"]
        new_model = MyModel(title=new_title, body=new_body, date=datetime.datetime.now())
        request.dbsession.add(new_model)
        return HTTPFound(location=request.route_url("home"))
    return {}


@view_config(route_name='update', renderer='templates/update.jinja2', permission='secret')
def update(request):
    try:
        query = request.dbsession.query(MyModel)
        entry = query.filter(MyModel.id == request.matchdict["id"]).first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    if request.method == "POST":
        new_title = request.POST["title"]
        new_body = request.POST["body"]
        new_model = MyModel(title=new_title, body=new_body, date=datetime.datetime.now())
        request.dbsession.add(new_model)
        return HTTPFound(location=request.route_url("home"))
    return {"entry": entry}


@view_config(route_name='login', renderer='templates/login.jinja2')
def login(request):
    if request.method == 'POST':
        username = request.params.get('username', '')
        password = request.params.get('password', '')
        if check_credentials(username, password):
            headers = remember(request, username)
            return HTTPFound(location=request.route_url('home'), headers=headers)
    return {}


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(request.route_url('home'), headers=headers)


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_journal_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
