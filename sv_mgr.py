#!/usr/bin/python3
import argparse
import os
import sys


LIGHT_BLUE = '\033[94m'
GREEN = '\033[32m'
LIGHT_RED = '\033[91m'
RED = '\033[31m'
LIGHT_WHITE = '\033[97m'
END = '\033[0m'
BAD_EXE_ERROR = "sv-mgr has been symlinked to as an unknown executable name!"
DESCRIPTION = "Disable or enable runit services"
EXE_LIST = ['sv-mgr', 'sv_mgr.py', 'sv-disable', 'sv-enable']
LOG_FILE = "/var/log/sv-mgr.log"
LOG_FMT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
OK_MSG = LIGHT_WHITE + '[  ' + GREEN + "OK" + LIGHT_WHITE + '  ]' + END
SV_DIR = "/etc/sv"
SERVICE_DIR = "/var/service"


# TODO:
# os.isatty() before using colors!


class BadExeError(Exception):
    """Raise when we're called as the wrong executable.'"""
    pass


class NeedSudoError(Exception):
    """Raise when we need sudo access."""
    pass


class NoSuchSvError(Exception):
    """Raise when a sv that does not exist has been requested."""
    pass


class SvAlreadyEnabledError(Exception):
    """Raise when a sv that's already enabled has been requested to be enabled.'"""
    pass


class SvNotEnabledError(Exception):
    """Raise when a sv that is not enabled has been requested to be disabled."""
    pass


def check_sv_path(path):
    """
    Check 'path', return True or raise NoSuchSvError if it's not an available service name.
    """
    if os.path.isdir(path):
        return True
    else:
        raise NoSuchSvError


def detect_executable(exe):
    """
    Check the name of the executable we're being called as,
    raise BadExeError if it's not something we expect.
    """
    for i in EXE_LIST:
        if i in exe:
            return i
    raise BadExeError


def disable_sv(sv, service_dir):
    """
    Disable the specified service, 'sv'.

    Assemble a 'service_path' from 'sv' and 'service_dir', then
    remove it and return True or bail out if we get an OSError.
    """
    service_path = os.path.join(service_dir, sv)
    try:
        os.remove(service_path)
        return True
    except OSError as e:
        if "Permission denied" in e.strerror:
            raise NeedSudoError
        else:
            raise SvNotEnabledError


def emit_error(error):
    """Write 'error' to STDOUT, then exit 1."""
    sys.stderr.write(LIGHT_WHITE + "[ " + RED + "FAIL" + LIGHT_WHITE + " ]" +
                     LIGHT_RED + "  {}".format(error) + END + "\n")
    sys.exit(1)


def enable_sv(sv, sv_dir, runsvdir):
    """
    Enable the specified service, 'sv'.

    Assemble 'sv_path' and 'service_path' from 'sv', 'sv_dir', and 'runsvdir'.
    Make a symlink from 'sv_path' to 'service_path' and bail if we get one
    of a couple different exceptions.
    """
    sv_path = os.path.join(sv_dir, sv)
    service_path = os.path.join(runsvdir, sv)
    try:
        check_sv_path(sv_path)
        os.symlink(sv_path, service_path)
        return True
    except NoSuchSvError:
        raise NoSuchSvError
    except PermissionError:
        raise NeedSudoError
    except FileExistsError:
        raise SvAlreadyEnabledError


def list_services(runsvdir):
    """Prints out the contents of 'runsvdir' in a nice format."""
    msg = LIGHT_WHITE + "Enabled services:" + LIGHT_BLUE
    services = os.listdir(runsvdir)
    services.sort()
    services.reverse()
    while services:
        msg += " "
        msg += services.pop()
    msg += END
    print(msg)


def setup_and_parse_args(exe, disable, enable, sv_mgr):
    """
    Set up args as needed based on what we're doing.
    """
    if sv_mgr:
        parser = argparse.ArgumentParser(
            description="Disable or enable services, list enabled ones", prog=exe)
        actions = parser.add_mutually_exclusive_group(required=True)
        actions.add_argument("-l", "--list", action="store_true", help="List enabled services")
        actions.add_argument("-d", "--disable", dest="service", metavar="SERVICE", nargs="?",
                             help="Disable the specified service")
        actions.add_argument("-e", "--enable", dest="service", metavar="SERVICE", nargs="?",
                             help="Enable the specified service")

    elif disable:
        parser = argparse.ArgumentParser(description="Disable a runit service", prog=exe)
        parser.add_argument("service", help="Service to be disabled", metavar="SERVICE")

    elif enable:
        parser = argparse.ArgumentParser(description="Enable a runit service", prog=exe)
        parser.add_argument("service", help="Service to be enabled", metavar="SERVICE")

    options = parser.add_argument_group("Configuration options")
    options.add_argument("-A", "--sv-dir", action="store", metavar="PATH",
                         help="Path to directory containing your service's run script. "
                         + LIGHT_WHITE + "Default: {}".format(SV_DIR) + END)
    options.add_argument("-B", "--runsvdir", action="store", metavar="PATH",
                         help="Path to your runsvdir. " + LIGHT_WHITE
                         + "Default: {}".format(SERVICE_DIR) + END)
    return parser


def okprnt(msg):
    """
    Print a message with a colored '[  OK  ]' message when we succeed at doing something.
    """
    print(OK_MSG + "  " + msg)


def main(args):
    """
    Do things!
    """
    e = detect_executable(args[0])

    disable = False
    enable = True
    sv_mgr = False

    sv_dir = SV_DIR
    runsvdir = SERVICE_DIR

    if (e == 'sv_mgr.py' or e == 'sv-mgr'):
        sv_mgr = True
    elif e == 'sv-disable':
        disable = True
    elif e == 'sv-enable':
        enable = True

    parser = setup_and_parse_args(e, disable, enable, sv_mgr)
    args = parser.parse_args()

    if args.sv_dir:
        sv_dir = args.sv_dir
    if args.runsvdir:
        runsvdir = args.runsvdir

    try:
        if sv_mgr:
            if args.disable:
                disable_sv(args.disable, runsvdir)
                okprnt("Disabling service: '{}'".format(args.disable))
            elif args.enable:
                enable_sv(args.enable, sv_dir, runsvdir)
                okprnt("Enabling service: '{}'".format(args.enable))
            elif args.list:
                list_services(runsvdir)
        elif disable:
            if args.service:
                disable_sv(args.service, runsvdir)
                okprnt("Disabling service: '{}'".format(args.service))
        elif enable:
            if args.service:
                enable_sv(args.service, sv_dir, runsvdir)
                okprnt("Enabling service: '{}'".format(args.service))
    except NeedSudoError:
        emit_error("Permission denied: please rerun with sudo")
    except NoSuchSvError:
        emit_error("There's no such service: '{}'".format(args.service))
    except SvAlreadyEnabledError:
        emit_error("'{}' is already enabled!".format(args.service))
    except SvNotEnabledError:
        emit_error("'{}' is not enabled!".format(args.service))


if __name__ == '__main__':
    try:
        main(sys.argv)
    except BadExeError:
        emit_error(BAD_EXE_ERROR)
