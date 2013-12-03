from cmd import Cmd
from base import BaseCli
from ssh import SshProvider
from vagrant import VagrantProvider

class SshCli(BaseCli):
    provider = SshProvider()

    def __init__(self, *args, **kwargs):
        Cmd.__init__(self, *args, **kwargs)
        self.prompt = '(Prudentia > Ssh) '


class VagrantCli(BaseCli):
    provider = VagrantProvider()

    def __init__(self, *args, **kwargs):
        Cmd.__init__(self, *args, **kwargs)
        self.prompt = '(Prudentia > Vagrant) '


class CLI(Cmd):
    cli = None

    environments = {
        'ssh': SshCli,
        'vagrant': VagrantCli
    }

    def __init__(self, *args, **kwargs):
        Cmd.__init__(self, *args, **kwargs)
        self.prompt = '(Prudentia) '

    def cmdloop(self, *args, **kwargs):
        print '\nTo start `use` one of those providers: %s.\n' % self.environments.keys()
        return Cmd.cmdloop(self, *args, **kwargs)


    def complete_use(self, text, line, begidx, endidx):
        if not text:
            return self.environments.keys()
        else:
            return [e for e in self.environments.keys() if e.startswith(text)]

    def do_use(self, env):
        cli = self.environments[env]
        if cli:
            self.cli = cli()
        else:
            print 'No provider for environment: %s' % env
            return False
        self.cli.cmdloop()

    def do_EOF(self, line):
        print "\n\nBye!"
        return True

    def emptyline(self, *args, **kwargs):
        return ""