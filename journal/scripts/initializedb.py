import os
import sys
import transaction
import datetime

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
from ..models import MyModel


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


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

        entries = [
            MyModel(title="Learning Journal - Day 12", date=datetime.date(2016, 12, 21), body="I woke up feeling nauseous today and decided to take the safe route and miss class. The good news is that by noon I was feeling normal again, so whatever it was is probably gone now. Also, I found it a lot easier to concentrate at home than on campus, and didn't get too far behind. Of course, it does mean that I needed to rewatch the lecture and read the class notes more thoroughly before doing the learning journal assignment."),
            MyModel(title="Learning Journal - Day 13", date=datetime.date(2016, 12, 22), body="I realized today that even though I've got a lot to do to catch up on assignments, the concepts are sticking in my mind rather well. Normally I avoid rewriting code at all costs and try to edit what I have, because restarting would mean swapping out one set of bugs for another. However, after working on the binary heap with Amos for most of yesterday, I decided to do a complete re-write, just because I understood exactly how it was supposed to work, but couldn't find out why it didn't. Surprisingly, it passed all the tests on the second try, and I was done in less than half an hour after the re-write. That being said, I'm not going to resort to a full re-write in every situation from now on, but in some circumstances, it's a better option than I originally thought."),
            MyModel(title="Learning Journal - Day 14", date=datetime.date(2016, 12, 23), body="Aside from making up work over the break, I'm also going to be thinking a lot about GerryPy, and how we're going to implement an algorithm and connect with an interface. We've already met once as a group, and gone over some ideas, for which technologies we want to pull our data from, as well as how to implement the algorithm. There still is a lot left to be decided, hopefully by the end of break, so we're going to stay in touch and do some more research."),
            MyModel(title="Learning Journal - Day 15", date=datetime.date(2017, 1, 2), body="The graph traversal was pretty straightforward, although I didn't catch up in the learning journal nearly as much as I had hoped to. That will probably be the biggest struggle this week. GerryPy is going well. We had a meeting to divide up and assign tasks to do before the project week officially starts. Our primary goal is to get everything set up and in place except for the actually algorithm that determines the shape of the districts."),
            MyModel(title="Learning Journal - Day 16", date=datetime.date(2017, 1, 3), body="This week it feels like I've set up a nice steady pace. I've still got more to catch up on, like usual, but the data structures are going smoothly, giving me more energy to put towards the learning journal. Our GerryPy group is also heading in an optimistic direction, and we have a solid plan on what to do before project week starts, as well as during.")
        ]

        dbsession.add_all(entries)
