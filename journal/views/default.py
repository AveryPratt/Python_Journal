import os
from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import MyModel


HERE = os.path.dirname(__file__)

ENTRIES = [
    {"title": "LJ - Day 10", "date": "Aug 19, 2016", "id": 10, "body": "Sample body text."},
    {"title": "LJ - Day 11", "date": "Aug 22, 2016", "id": 11, "body": "Sample body text."},
    {"title": "LJ - Day 12", "date": "Aug 23, 2016", "id": 12, "body": "Sample body text."},
]


@view_config(route_name='home', renderer='templates/home.jinja2')
def home(request):
    # imported_text = open(os.path.join(HERE, 'data/home.html')).read()
    # return imported_text
    return {"entries": ENTRIES}


@view_config(route_name='detail', renderer='templates/detail.jinja2')
def detail(request):
    # imported_text = open(os.path.join(HERE, 'data/detail.html')).read()
    # return imported_text
    return {"entry": ENTRIES[0]}


@view_config(route_name='create', renderer='templates/create.jinja2')
def create(request):
    # imported_text = open(os.path.join(HERE, 'data/create.html')).read()
    # return imported_text
    return {}


@view_config(route_name='update', renderer='templates/update.jinja2')
def update(request):
    # imported_text = open(os.path.join(HERE, 'data/update.html')).read()
    # return imported_text
    return {"entry": ENTRIES[0]}


# @view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
# def my_view(request):
#     try:
#         query = request.dbsession.query(MyModel)
#         one = query.filter(MyModel.name == 'one').first()
#     except DBAPIError:
#         return Response(db_err_msg, content_type='text/plain', status=500)
#     return {'one': one, 'project': 'journal'}


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
