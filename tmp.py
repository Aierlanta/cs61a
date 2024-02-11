from typing import Dict


class Email:
    """
    Every email object has 3 instance attributes: the
    message, the sender name, and the recipient name.
    >>> email = Email('hello', 'Alice', 'Bob')
    >>> email.msg
    'hello'
    >>> email.sender_name
    'Alice'
    >>> email.recipient_name
    'Bob'
    """

    def __init__(self, msg: str, sender_name: str, recipient_name: str) -> None:
        self.msg = msg
        self.sender_name = sender_name
        self.recipient_name = recipient_name


class Server:
    """
    Each Server has one instance attribute: clients (which
    is a dictionary that associates client names with
    client objects).
    """

    def __init__(self):
        self.clients: Dict[str, "Client"] = {}

    def send(self, email: "Email"):
        """
        Take an email and put it in the inbox of the client
        it is addressed to.
        """
        # Get the recipient name from the email
        recipient_name = email.recipient_name
        # Check if the recipient is a registered client
        if recipient_name in self.clients:
            # Get the recipient client object
            recipient_client = self.clients[recipient_name]
            # Call the receive method of the recipient client with the email
            recipient_client.receive(email)
        else:
            # Print an error message
            print(f"Error: {recipient_name} is not a registered client.")

    def register_client(self, client, client_name: str):
        """
        Takes a client object and client_name and adds them
        to the clients instance attribute.
        """
        # Check if the client name is already taken
        if client_name in self.clients:
            # Print an error message
            print(f"Error: {client_name} is already taken.")
        else:
            # Add the client object and name to the clients dictionary
            self.clients[client_name] = client


class Client:
    """
    Every Client has three instance attributes: name (which is
    used for addressing emails to the client), server
    (which is used to send emails out to other clients), and
    inbox (a list of all emails the client has received).

    >>> s = Server()
    >>> a = Client(s, 'Alice')
    >>> b = Client(s, 'Bob')
    >>> a.compose('Hello, World!', 'Bob')
    >>> b.inbox[0].msg
    'Hello, World!'
    >>> a.compose('CS 61A Rocks!', 'Bob')
    >>> len(b.inbox)
    2
    >>> b.inbox[1].msg
    'CS 61A Rocks!'
    """

    def __init__(self, server: "Server", name: str):
        self.inbox: list["Email"] = []  # Change the type annotation to Email
        self.server = server
        self.name = name
        # Register the client to the server with the name
        server.register_client(
            self, name
        )  # Move this line to the end of the __init__ method

    def compose(self, msg: str, recipient_name: str):
        """Send an email with the given message msg to the given recipient client."""
        # Create an email object with the message, sender name, and recipient name
        email = Email(msg, self.name, recipient_name)
        # Call the send method of the server with the email
        self.server.send(email)

    def receive(self, email: "Email"):
        """Take an email and add it to the inbox of this client."""
        # Append the email object to the inbox list
        self.inbox.append(email)  # Change email.msg to email
