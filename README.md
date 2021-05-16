# Chatto

Chatto is a simple chat application that allows one to one messaging with end-to-end encryption using [Elliptic-curve Diffie–Hellman](https://en.wikipedia.org/wiki/Elliptic-curve_Diffie%E2%80%93Hellman). 

* Server - a Flask based web application that uses [SocketIO](https://socket.io/) to send and receive message from the client. 
* Client - is just a simple CLI based interface to send, receive and view the messages from the server.

## Tools and technology used

* Database - MongoDB
* Cryptoraphic Algorithms - SHA256, AES 256-bit(CBC), bcrypt and ECDH with NIST521p curve.


## Setting up the Environment

### Cloning the Respository

1. SSH-styled :

```
git clone git@github.com:RazCrimson/Chatto.git
```

2. HTTPS-styled :

```
git clone https://github.com/RazCrimson/Chatto.git
```

### Installing Dependencies
Using [pip](https://pip.pypa.io/en/stable/). Creating a dedicated [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) for the project is advised. Recommended Python version `>=3.7`

```bash
# For server
cd Chatto/server
pip install -r requirements.txt

# For client
cd ../client
pip install -r requirements.txt
```

### Make `.env` configuration (only for server)
Create a copy of `server/.env.example` in the same directory and name it `.env`. Fill in the required environment variables. You can also have those environment variables set up in your shell.


## Execution
* **Server** : Inside the server directory.

```bash
# Script style
python run.py
```

```
# Flask App style
FLASK_APP=run:flask_app flask run
```

* **Client** 
```
python run.py [--localhost] [--register] <username>
```
`-l, --localhost` - flag for using the local server or the deployed server.

`-r, --register`  - flag for performing user registration

`username` - the name that you want to login or register as.


## Contributing
All contributions and pull requests are welcome. Open an issue if you find any bugs/faults or if you want to implement a change and would like to discuss the implementation.



## License
[MIT](https://choosealicense.com/licenses/mit/)

## Author
* Bharath Vignesh J K - [@RazCrimson](https://github.com/RazCrimson)
