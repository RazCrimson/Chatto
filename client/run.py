from app import Client

if __name__ == '__main__':
    username = 'Raz'
    password = 'password@123'
    client = Client(username, password, do_register=True)
    client.run_interactive_session()
