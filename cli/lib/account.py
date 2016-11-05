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
    apikey = account_info.get("apikey")
    secret = account_info.get("secret")
    while True:
        api = Knufactor(apikey, secret, server=server)
        try:
            api.refresh_auth()
        except UnauthorizedException as e:
            print("Server error: %s. Please try again." % str(e))
        else:
            break
    return api


def configure():
    print("Please fill in your Knuverse cloud information(or register: https://cloud.knuverse.com): ")
    apikey = input("API Key: ")
    secret = input("Secret: ")

    config = configparser.RawConfigParser()
    config.add_section("credentials")
    config.set("credentials", "server_url", "https://cloud.knuverse.com")
    config.set("credentials", "apikey", apikey)
    config.set("credentials", "secret", secret)
    if not os.path.exists(KNUVERSE_CONFIG_DIR):
        os.mkdir(KNUVERSE_CONFIG_DIR)
    with open(os.path.join(KNUVERSE_CONFIG_DIR, 'credentials'), 'w+') as configfile:
        config.write(configfile)
    print("Success!")


def get_account_info():
    if os.path.exists(os.path.join(KNUVERSE_CONFIG_DIR, 'credentials')):
        config = configparser.RawConfigParser()
        config.read(os.path.join(KNUVERSE_CONFIG_DIR, 'credentials'))
        apikey = config.get("credentials", "apikey")
        secret = config.get("credentials", "secret")
        server_url = config.get("credentials", "server_url")
        return {
            "apikey": apikey,
            "secret": secret,
            "server_url": server_url
        }
    else:
        configure()
        return get_account_info()
