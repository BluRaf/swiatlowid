from swiatlowid import plugin
from time import sleep
import platform
import importlib.metadata

@plugin.command('pomoc')
def help(bot, client, event, args):
    """Właśnie ją czytasz"""
    if len(args) == 1:
        if args[0] in plugin.plugins.keys():
            summary = plugin.plugins[args[0]].__doc__.splitlines()[0]
            client.notice(event.source.nick,
                          "{}: {}".format(args[0], summary))
        else:
            client.notice(event.source.nick, "Nieznana komenda!")
    else:
        for cmd in plugin.plugins:
            client.notice(event.source.nick,
                          "{}: {}".format(cmd, plugin.plugins[cmd].__doc__))
            sleep(1.2) # delay to fit in floodlimits

@plugin.command('wersja')
def about(bot, client, event, args):
    """Listuje informacje o bocie"""
    client.privmsg(bot.channel,
                   "Światłowid {}, jaraco/irc {}, Python {}".format(
                   bot.version,
                   importlib.metadata.version("irc"),
                   platform.python_version()))

@plugin.command('elementy')
def elements(bot, client, event, args):
    """Listuje argumenty podane komendzie"""
    client.privmsg(bot.channel, "{}: {}".format(event.source.nick,
                                                str(args).strip('[]')))

@plugin.command('rozlacz')
def disconnect(bot, client, event, args):
    """Rozłącza bota z serwerem"""
    bot.disconnect("Zaraz wracam")

@plugin.command('zamilcz')
def die(bot, client, event, args):
    """Wyłącza bota"""
    bot.die("To ja uciekam")

@plugin.command('wolaj')
def everyone(bot, client, event, args):
    """Woła wszystkich dostępnych na kanale"""
    client.privmsg(bot.channel, ", ".join(bot.channels[bot.channel].users()))

@plugin.command('statystyki')
def stats(bot, client, event, args):
    """Zwraca statystyki kanałów, do których jest podłączony bot"""
    nick = event.source.nick
    for chname, chobj in bot.channels.items():
        client.notice(nick, "--- Kanał: " + chname)
        users = sorted(chobj.users())
        client.notice(nick, "Użytkownicy: " + ", ".join(users))
        opers = sorted(chobj.opers())
        client.notice(nick, "Operatorzy: " + ", ".join(opers))
        voiced = sorted(chobj.voiced())
        client.notice(nick, "Z prawem głosu: " + ", ".join(voiced))

# @plugin.command('dcc')
# def dcc(bot, client, event, args):
#     """Robi echo na DCC (hostowanie plików w planach)"""
#     dcc = bot.dcc_listen()
#     client.ctcp(
#         "DCC",
#         event.source.nick,
#         "CHAT chat %s %d"
#         % (ip_quad_to_numstr(dcc.localaddress), dcc.localport),
#     )
