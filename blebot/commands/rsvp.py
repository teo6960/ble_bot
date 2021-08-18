import traceback

import parsedatetime
import datetime
import dateutil.parser
from pytz import timezone
import humanize

from ..schema.events import get_session, Event

EASTERN = timezone("US/Eastern")
allowed_actions = ["create", "delete", "list", "going", "maybe", "help", "details", "ditch"]

def handle_help():
    return """\n`rsvp` - allows:
    `create` - create an event `/rsvp create Raid @ 8:00pm on Saturday`
    `delete` - deletes an event `/rsvp delete [event number]`
    `list` - lists the upcoming events
    `going` - rsvp as going to an event `/rsvp going [event number]`
    `maybe` - rsvp as maybe going to an event `/rsvp maybe [event number]`
    `ditch` - remove your rsvp from the event `/rsvp ditch [event number]`
    """

def handle_action(action, args, message):
    if not action:
        return "\nPlease provide an action! See `/rsvp help`"
    if action not in allowed_actions:
        return "\n`{action}` is not one of {actions}".format(
            action = action,
            actions = ", ".join(list(map(lambda x: "`" + x + "`", allowed_actions)))
        )

    if action == "create":
        return _create(action, args, message)
    elif action == "delete":
        return _delete(action, args, message)
    elif action == "list":
        return _list(action, args, message)
    elif action == "details":
        return _details(action, args, message)
    elif action == "going":
        return _going(action, args, message)
    elif action == "maybe":
        return _maybe(action, args, message)
    elif action == "ditch":
        return _ditch(action, args, message)
    elif action == "help":
        return handle_help()
    return "\nSomething went wrong"

def _create(action, args, message):
    session = get_session()
    if not args or "@" not in args:
        return "\nPlease format your event description as [event name]@[date time]\n i.e. `/rsvp create Raid @ 4/16/2016 8:00pm EST`"
    name, time = args.split("@")
    try:
        cal = parsedatetime.Calender()
        date = cal.parse(time.strip())
    except:
        try:
            date = dateutil.parser.parse(time.strip())
        except:
            return "\n I couldn't understand that time."

    event = Event(name.strip().upper(), date, message.author.name)
    session.add(event)
    session.commit()
    return "\nYou created an event with event number {number}! **{name}** @ __{date}__".format(
        number=event.id,
        name=name,
        date=EASTERN.localize(date).strftime("%I:%M%p %Z on %a. %b %d"),

    )

def _delete(action, args, message):
    session = get_session()
    if not args:
        return "\nPlease provide the number of the event you wish to create! Check `/rsvp list`"
    try:
        session.query(Event).filter_by(id=int(args)).delete()
        session.commit()
        return "\nYou've deleted the event!"
    except:
        traceback.print_exc()
        return "\nCould not find event with number {number}".format(number=args)

def _list(action, args, message):
    session = get_session()
    events = session.query(Event).filter(Event.date >= datetime.datetime.now()).order_by(Event.date).all()
    if not events:
        return "\nThere are no upcoming events! :( \n\nMake one by using `/rsvp create`"
    return "\nHere are the upcoming events!\n\n{events}".format(
        events="\n".join(list(map(lambda x: x.format(), events)))
    )

def _details(action, args, message):
    if not args:
        return "\nPlease provide the number of the event you wish to see! Check `/rsvp list`"
    try:
        session = get_session()
        event = session.query(Event).get(int(args))
        return event.details()
    except:
        traceback.print_exc()
        return "\nCould not find event with number {number}".format(number=args)

def _going(action, args, message):
    if not args:
        return "\nPlease provide the number of the event you wish to go to! Check `/rsvp list`"
    try:
        session = get_session()
        event = session.query(Event).get(int(args))
        if message.author.name in event.maybe:
            event.maybe.remove(message.author.name)
        event.going.add(message.author.name)
        session.commit()
        return "\n{name} registered as going!".format(name=message.author.name)
    except:
        traceback.print_exc()
        return "\nCould not find event with number {number}".format(number=args)

def _maybe(action, args, message):
    if not args:
        return "\nPlease provide the number of the event you wish to maybe go to! Check `/rsvp list`"
    try:
        event = session.query(Event).get(int(args))
        if message.author.name in event.going:
            event.going.remove(message.author.name)
        event.maybe.add(message.author.name)
        session.commit()
        return "\n{name} registered as maybe attending!".format(name=message.author.name)
    except:
        traceback.print_exc()
        return "\nCould not find event with number {number}".format(number=args)

def _ditch(action, args, message):
    if not args:
        return "\nPlease provide the number of the event you wish to ditch! Check `/rsvp list`"
    try:
        event = session.query(Event).get(int(args))
        if message.author.name in event.maybe:
            event.maybe.remove(message.author.name)
        if message.author.name in event.going:
            event.going.remove(message.author.name)
        session.commit()
        return "\n{name} ditched this event!".format(name=message.author.name)
    except:
        return "\nCould not find event with number {number}".format(number=args)
