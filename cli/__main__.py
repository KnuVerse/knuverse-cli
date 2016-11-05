#!/usr/bin/env python

import sys
from inspect import classify_class_attrs
from inspect import getdoc
from knuverse.knufactor import HttpErrorException
from cli.knu import verification
from cli.lib.account import login
from cli.lib.account import configure


class InvalidCommandException(Exception):
    """
    Invalid command exception class
    """


def help_short():
    help_text = """Usage: knuverse [--help] <command> [args]

Commands:"""
    print(help_text)

    for f in classify_class_attrs(Knuverse):
        if f.name.startswith("__"):
           continue
        docstring = f.object.__doc__
        print("   {:15}{description}".format(f.name, description=next(s.lstrip() for s in docstring.split('\n') if s)))


class Knuverse(object):

    def __init__(self):
        pass

    def configure(self, args):
        """
        Configure Knuverse account credentials
        Usage: knuverse configure

        """
        if "--help" in args:
            raise InvalidCommandException
        configure()

    def verify(self, args):
        """
        Verify a user with either AudioPIN or AudioPass
        Usage: knuverse verify <NAME> [options]

        Options:
          --audiopin Specifies to do an AudioPIN verification

          --audiopass Specifies to do an AudioPass verification

        """
        if len(args) < 1 or "--help" in args:
            raise InvalidCommandException
        else:
            name = args[0]
            mode = None
            if "--audiopin" in args:
                mode = "audiopin"
            elif "--audiopass" in args:
                mode = "audiopass"
            api = login()
            verification(api, client_name=name, mode=mode)


def _main():

    if len(sys.argv) < 2:
        help_short()
    else:
        kv = Knuverse()
        function_mappings = {
            'verify': kv.verify,
            'configure': kv.configure
        }
        cmd = sys.argv[1]
        f = function_mappings.get(cmd)
        if f:
            try:
                f(sys.argv[2:])
            except InvalidCommandException:
                print(getdoc(f))
        else:
            help_short()


def main():
    try:
        _main()
    except HttpErrorException as e:
        print("Server error: %s." % str(e))
        sys.exit(1)
    except KeyboardInterrupt:
        print("Exiting.")
        sys.exit(0)

if __name__ == "__main__":
    main()
