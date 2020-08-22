from swiatlowid import plugin
from time import sleep

@plugin.command('pomoc')
def help(bot, client, event, args):
    """Właśnie ją czytasz"""
    if len(args) == 1:
        if args[0] in plugin.plugins.keys():
            client.notice(event.source.nick, "{}: {}".format(args[0], plugin.plugins[args[0]].__doc__))
        else:
            client.notice(event.source.nick, "help: nieznana komenda")
    else:
        for cmd in plugin.plugins:
            client.notice(event.source.nick, "{}: {}".format(cmd, plugin.plugins[cmd].__doc__))
            sleep(1.2)

@plugin.command('jeszczejak')
def ofcourse(bot, client, event, args):
    """A jak pan Jezus powiedział?"""
    client.privmsg(bot.channel, "Jeszcze jak!".format(event.source.nick))

@plugin.command('elementy')
def elements(bot, client, event, args):
    """Listuje argumenty podane funkcji"""
    client.privmsg(bot.channel, "{}: {}".format(event.source.nick, str(args).strip('[]')))

@plugin.command('rozlacz')
def disconnect(bot, client, event, args):
    """Rozłącza bota z serwerem"""
    bot.disconnect()

@plugin.command('padnij')
def die(bot, client, event, args):
    """Wyłącza bota"""
    bot.die()

@plugin.command('statystyki')
def stats(bot, client, event, args):
    """Zwraca statystyki kanału"""
    for chname, chobj in bot.channels.items():
        client.notice(nick, "Kanał: " + chname)
        users = sorted(chobj.users())
        client.notice(nick, "Użytkownicy: " + ", ".join(users))
        opers = sorted(chobj.opers())
        client.notice(nick, "Operatorzy: " + ", ".join(opers))
        voiced = sorted(chobj.voiced())
        client.notice(nick, "Z prawem głosu: " + ", ".join(voiced))

@plugin.command('dcc')
def dcc(bot, client, event, args):
    """Robi echo na DCC (hostowanie plików w planach)"""
    dcc = bot.dcc_listen()
    client.ctcp(
        "DCC",
        event.source.nick,
        "CHAT chat %s %d"
        % (ip_quad_to_numstr(dcc.localaddress), dcc.localport),
    )
