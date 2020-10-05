import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
from . import __version__, plugin

class Swiatlowid(irc.bot.SingleServerIRCBot):
    version = __version__

    def __init__(self, server, channel, port=6667, nickname="Swiatlowid", password=None, prefix=None):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, password)], nickname, nickname)
        self.channel = channel
        self.prefix = prefix
        plugin.scan('swiatlowid.plugins')

    @staticmethod
    def get_version():
        return f"Swiatlowid {__version__}"
        
    # Event handlers

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        self.do_command(e, e.arguments[0])

    def on_pubmsg(self, c, e):
        if isinstance(self.prefix, str):
            if e.arguments[0].startswith(self.prefix):
                self.do_command(e, e.arguments[0][len(self.prefix):].strip())
        else:
            a = e.arguments[0].split(":", 1)
            if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(
                self.connection.get_nickname()
            ):
                self.do_command(e, a[1].strip())
        return

    def on_dccmsg(self, c, e):
        # non-chat DCC messages are raw bytes; decode as text
        text = e.arguments[0].decode('utf-8')
        c.privmsg("Napisałeś: " + text)

    def on_dccchat(self, c, e):
        if len(e.arguments) != 2:
            return
        args = e.arguments[1].split()
        if len(args) == 4:
            try:
                address = ip_numstr_to_quad(args[2])
                port = int(args[3])
            except ValueError:
                return
            self.dcc_connect(address, port)

    # Internal functions

    def do_command(self, e, cmdline):
        c = self.connection

        cmd_list = cmdline.split()
        cmd = cmd_list[0]

        if cmd in plugin.plugins.keys():
            cmd_func = plugin.plugins[cmd]
            cmd_func(self, c, e, cmd_list[1:])
        else:
            c.notice(e.source.nick, "Not understood: " + cmd)
