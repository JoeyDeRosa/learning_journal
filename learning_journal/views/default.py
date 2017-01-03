from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import Entry


@view_config(route_name='create', renderer='../templates/new_entry.jinja2', permission='add')
def create_view(request):
    if request.method == "POST":
        new_title = request.POST["title"]
        new_body = request.POST["body"]
        new_date = request.POST["date"]
        new_model = Entry(title=new_title, body=new_body, date=new_date)

        request.dbsession.add(new_model)

        return {"data": {"name": "We made a new model!"}}

    return {"data": {"name": "A New Form"}}


@view_config(route_name='home', renderer='../templates/home.jinja2')
def my_view(request):
    try:
        entry = request.dbsession.query(Entry).all()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'title_list': entry}


@view_config(route_name='detail', renderer='../templates/entry.jinja2')
def detail_view(request):
    entry = request.dbsession.query(Entry)
    detail_entry = entry.filter(Entry.id == request.matchdict['id']).first()
    return {'title_list': detail_entry}


@view_config(route_name='update', renderer='../templates/edit_entry.jinja2', permission='add')
def update_view(request):
    entry = request.dbsession.query(Entry)
    detail_entry = entry.filter(Entry.id == request.matchdict['id']).first()
    return {'title_list': detail_entry}


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_learning_journal_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
