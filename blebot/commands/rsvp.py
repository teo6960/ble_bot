import traceback

import parsedatetime
from pytz import timezone
import datetime
import dateutil.parser
from sqlalchemy import and_

from ..schema import get_session
from ..schema.events import Event
from ..utils.error import BlebotError

EASTERN = timezone("US/Eastern")
allowed_actions = ["create", "delete", "list", "going", "maybe", "help", "details", "ditch"]

def handle_help():
    return """\n`rsvp` - Organizes rsvp events\n
`create` - create an event
    `/rsvp create Raid @ 8:00pm on Saturday`
`delete` - deletes an event
    `/rsvp delete [event number]`
`list` - lists the upcoming events
    `/rssvp list`
`going` - rsvp as going to an event
    `/rsvp going [event number]`
`maybe` - rsvp as maybe going to an event
    `/rsvp maybe [event number]`
`ditch` - remove your rsvp from the event
    `/rsvp ditch [event number]`
"""

def handle_action(command, action, args, message, extras):
    if not action:
        return "\nPlease provide an action! See `/rsvp help`"

    if action not in allowed_actions:
        raise BlebotError("\n`{action}` is not one of {actions}".format(
            action = action,
            actions = ", ".join(list(map(lambda x: "`" + x + "`", allowed_actions)))
        ))

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
    session = get_session(message.server.id)
    if not args or "@" not in args:
        raise BlebotError("\nPlease format your event description as [event name]@[date time]\n i.e. `/rsvp create Raid @ 4/16/2016 8:00pm EST`")
    name, time = args.split("@")
    try:
        cal = parsedatetime.Calender()
        date = cal.parse(time.strip())
    except:
        try:
            date = dateutil.parser.parse(time.strip())
        except:
            raise BlebotError("I couldn't understand that time.")

    event = Event(name.strip().upper(), date, message.author.name, message.channel.id, message.server.id)
    session.add(event)
    session.commit()
    return "\nYou created an event!\nEvent Number: *{number}*!\n**{name}** @ __{date}__".format(
        number=event.id,
        name=name,
        date=EASTERN.localize(date).strftime("%I:%M%p %Z on %a. %b %d"),
    )

def _delete(action, args, message):
    session = get_session(message.server.id)
    if not args:
        raise BlebotError("Please provide the number of the event you wish to create! Check `/rsvp list`")
    try:
        session.query(Event).filter(and_(Event.id == int(args), Event.channel == message.channel.id)).first().delete()
        session.commit()
        return "\nYou've deleted the event!"
    except:
        traceback.print_exc()
        raise BlebotError("Could not find event with number {number}".format(number=args))

def _list(action, args, message):
    session = get_session(message.server.id)
    events = session.query(Event).filter(and_(Event.date >= datetime.datetime.now(), Event.channel == message.channel.id)).order_by(Event.date).all()
    if not events:
        return "\nThere are no upcoming events! :( \n\nMake one by using `/rsvp create`"
    return "\nHere are the upcoming events!\n\n{events}".format(
        events="\n".join(list(map(lambda x: x.format(), events)))
    )

def _details(action, args, message):
    if not args:
        raise BlebotError("Please provide the number of the event you wish to see! Check `/rsvp list`")
    session = get_session(message.server.id)
    event = session.query(Event).filter(and_(Event.id == int(args), Event.channel == message.channel.id)).first()
    if not event:
        raise BlebotError("Could not find event with number {number}".format(number=args))

    return event.details()

def _going(action, args, message):
    if not args:
        raise BlebotError("Please provide the number of the event you wish to go to! Check `/rsvp list`")

    session = get_session(message.server.id)
    event = session.query(Event).filter(and_(Event.id == int(args), Event.channel == message.channel.id)).first()
    if not event:
        raise BlebotError("Could not find event with number {number}".format(number=args))

    if message.author.name in event.maybe:
        event.maybe.remove(message.author.name)
    event.going.add(message.author.name)
    session.commit()
    return "\n{name} registered as going!".format(name=message.author.name)


def _maybe(action, args, message):
    if not args:
        raise BlebotError("Please provide the number of the event you wish to maybe go to! Check `/rsvp list`")

    session = get_session(message.server.id)

    event = session.query(Event).filter(and_(Event.id == int(args), Event.channel == message.channel.id)).first()
    if not event:
        raise BlebotError("Could not find event with number {number}".format(number=args))

    if message.author.name in event.going:
        event.going.remove(message.author.name)

    event.maybe.add(message.author.name)
    session.commit()
    return "\n{name} registered as maybe attending!".format(name=message.author.name)

def _ditch(action, args, message):
    if not args:
        raise BlebotError("Please provide the number of the event you wish to ditch! Check `/rsvp list`")

    session = get_session(message.server.id)

    event = session.query(Event).filter(and_(Event.id == int(args), Event.channel == message.channel.id)).first()
    if not event:
        raise BlebotError("Could not find event with number {number}".format(number=args))

    if message.author.name in event.maybe:
        event.maybe.remove(message.author.name)
    if message.author.name in event.going:
        event.going.remove(message.author.name)
    session.commit()
    return "\n{name} ditched this event!".format(name=message.author.name)
