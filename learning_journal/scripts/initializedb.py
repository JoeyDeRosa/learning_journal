import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from ..models import Entry


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)

JOURNAL = [
    {'id': 1, 'title': 'Joey DeRosa Learning Journal Day12', 'date': '12/20/16', 'body': 'Today was a long day, after chasing errors and refactoring math formulas our heap was finally compleat. I wouldn\'t have thought two simple methods to be so time consuming. By the time I got to my Journal app the TAs had already left. Luckilly with the help of some class-mates the app you see before you has life.'},
    {'id': 2, 'title': 'Joey DeRosa Learning Journal Day11', 'date': '12/19/16', 'body': 'Today was The day we pitched our project ideas, A lot of good ones there but I think it is obvious that TrollPy is the way to go. The data structure today was called Deque and was basically a renamed doubly linked list. Really glad that pyramid was introduced and I no longer have to trouble shoot errors that seem to just create themselves in code that was previously working.'},
    {'id': 3, 'title': 'Joey DeRosa Learning Journal Day10', 'date': '12/16/16', 'body': 'Today\'s white boarding challenge proved frustrating due to the limitations of what we could use, however with most things in coding the answer seemed obvious after we solved it. As for the server the new addition s weren\'t difficult to implement and gevent is a handy new feature. Our server also has some nice new response codes to throw out.'},
    {'id': 4, 'title': 'Joey DeRosa Learning Journal Day9', 'date': '12/15/16', 'body': 'Today had a lot of data structure trouble. We were on a wild goose chase trying to fix errors for functionality that wasn\'t needed. I did learn a lot about requesting files from a server and how to return them. All in all an tiring but good day.'},
    {'id': 5, 'title': 'Joey DeRosa Learning Journal Day8', 'date': '12/14/16', 'body': 'Today\'s data structure assignment wasn\'t much of a challenge with the single link list to work from. The server was fairly easy too because we had accidentally worked ahead the day before, however we did run into an infinite loop error that appeared for seemingly no reason. The PuPPy meetup was awesome, unfortunately I had to leave early in order to get home at a decent hour. the Kit AI was totally a Knight Rider reference.'},
]


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        for i in JOURNAL:
            model = Entry(title=i['title'], body=i['body'], date=i['date'])
            dbsession.add(model)
