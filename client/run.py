from argparse import ArgumentParser
from getpass import getpass
from app import Client, constants


parser = ArgumentParser(description='Simple CLI based client for Chatt-o.',
                        epilog='Enjoy the CLI client! :)',
                        allow_abbrev=False)
parser.add_argument('username', metavar='username', type=str, help='The user name to login as')
parser.add_argument('-l', '--localhost', action='store_true', help='Connect to the localhost development server')
parser.add_argument('-r', '--register', action='store_true', help='Connect to the localhost development server')

if __name__ == '__main__':
    args = parser.parse_args()
    username = args.username
    do_register = args.register
    use_localhost = args.localhost

    constants.set_config(localhost=use_localhost)

    password = getpass()
    client = Client(username, password, do_register=do_register)
    client.run_interactive_session()
