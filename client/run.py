from argparse import ArgumentParser
from getpass import getpass
from app import Client, constants

parser = ArgumentParser(description='Simple CLI based client for Chatt-o.',
                        epilog='Enjoy the CLI client! :)',
                        allow_abbrev=False)
parser.add_argument('host', metavar='host', type=str, help='The server to connect to.')
parser.add_argument('username', metavar='username', type=str, help='The user name to login as')
parser.add_argument('-i', '--insecure', action='store_true', help='Run without TLS.')
parser.add_argument('-r', '--register', action='store_true', help='Perform user registration.')

if __name__ == '__main__':
    args = parser.parse_args()
    host = args.host
    insecure = args.insecure
    username = args.username
    do_register = args.register

    constants.set_config(host, insecure)

    password = getpass()
    client = Client(username, password, do_register=do_register)
    client.run_interactive_session()
