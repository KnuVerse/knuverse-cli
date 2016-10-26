try:
    import configparser
except ImportError:
    # Called ConfigParser in Python 2
    import ConfigParser as configparser

try:
   input = raw_input
except NameError:
   pass
import os
import getpass
from knuverse.knufactor import Knufactor
from knuverse.knufactor import UnauthorizedException

KNUVERSE_CONFIG_DIR = os.path.expanduser("~/.knuverse")


def login():
    account_info = get_account_info()
    server = account_info.get("server_url")
    user = account_info.get("user")
    account_id = account_info.get("account_id")
    while True:
        password = getpass.getpass("%s's password: " % user)
        api = Knufactor(server, username=user, password=password, account=account_id)
        try:
            api.refresh_auth()
        except UnauthorizedException as e:
            print("Server error: %s. Please try again." % str(e))
        else:
            break
    return api


def configure():
    print("Please fill in your Knuverse cloud information(or register: https://cloud.knuverse.com): ")
    account_id = input("Account ID: ")
    user = input("Username: ")

    config = configparser.RawConfigParser()
    config.add_section("credentials")
    config.set("credentials", "server_url", "https://cloud.knuverse.com")
    config.set("credentials", "user", user)
    config.set("credentials", "account_id", account_id)
    if not os.path.exists(KNUVERSE_CONFIG_DIR):
        os.mkdir(KNUVERSE_CONFIG_DIR)
    with open(os.path.join(KNUVERSE_CONFIG_DIR, 'credentials'), 'w+') as configfile:
        config.write(configfile)
    print("Success!")


def get_account_info():
    if os.path.exists(os.path.join(KNUVERSE_CONFIG_DIR, 'credentials')):
        config = configparser.RawConfigParser()
        config.read(os.path.join(KNUVERSE_CONFIG_DIR, 'credentials'))
        user = config.get("credentials", "user")
        account_id = config.get("credentials", "account_id")
        server_url = config.get("credentials", "server_url")
        return {
            "user": user,
            "account_id": account_id,
            "server_url": server_url
        }
    else:
        configure()
        return get_account_info()
