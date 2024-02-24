from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, List


@dataclass
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

    msg: str
    sender_name: str
    recipient_name: str


@dataclass
class Server:
    """
    Each Server has one instance attribute: clients (which
    is a dictionary that associates client names with
    client objects).
    """

    clients: Dict[str, Client] = field(default_factory=dict)

    def send(self, email: Email):
        """
        Take an email and put it in the inbox of the client
        it is addressed to.
        """
        recipient_name = email.recipient_name
        recipient_client = self.clients[recipient_name]
        recipient_client.receive(email)  # 调用Client的receive方法

    def register_client(self, client: Client, client_name: str):
        """
        Takes a client object and client_name and adds them
        to the clients instance attribute.
        """
        self.clients[client_name] = client


@dataclass
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

    server: Server
    name: str
    inbox: list[Email] = field(default_factory=list)

    def __post_init__(self):
        self.server.register_client(self, self.name)

    def compose(self, msg: str, recipient_name: str):
        """Send an email with the given message msg to the given recipient client."""
        email = Email(msg, self.name, recipient_name)
        self.server.send(email)

    def receive(self, email: Email):
        """Take an email and add it to the inbox of this client."""
        self.inbox.append(email)


class Button:
    def __init__(self, pos: int, key: str):
        self.pos = pos
        self.key = key
        self.times_pressed = 0


class Keyboard:
    """A Keyboard stores an arbitrary number of Buttons in a dictionary.
    Each dictionary key is a Button's position, and each dictionary
    value is the corresponding Button.
    >>> b1, b2 = Button(5, "H"), Button(7, "I")
    >>> k = Keyboard(b1, b2)
    >>> k.buttons[5].key
    'H'
    >>> k.press(7)
    'I'
    >>> k.press(0) # No button at this position
    ''
    >>> k.typing([5, 7])
    'HI'
    >>> k.typing([7, 5])
    'IH'
    >>> b1.times_pressed
    2
    >>> b2.times_pressed
    3
    """

    def __init__(self, *args: Button):
        self.buttons: dict[int, Button] = {}
        for i in args:
            self.buttons[i.pos] = i

    def press(self, pos: int):
        """Takes in a position of the button pressed, and
        returns that button's output."""
        if pos in self.buttons:
            self.buttons[pos].times_pressed += 1
            key = self.buttons[pos].key
            return key
        return ""

    def typing(self, typing_input: list[int]):
        """Takes in a list of positions of buttons pressed, and
        returns the total output."""
        result = ""
        for pos in typing_input:
            result += self.press(pos)
        return result


class TeamMember:
    """
    >>> adder = TeamMember(lambda x: x + 1) # team member at front
    >>> adder2 = TeamMember(lambda x: x + 2, adder) # team member 2
    >>> multiplier = TeamMember(lambda x: x * 5, adder2) # team member 3
    >>> adder.relay_history() # relay history starts off as empty
    []
    >>> adder.relay_calculate(5) # 5 + 1
    6
    >>> adder2.relay_calculate(5) # (5 + 1) + 2
    8
    >>> multiplier.relay_calculate(5) # (((5 + 1) + 2) * 5)
    40
    >>> multiplier.relay_history() # history of answers from the most recent relay multiplier participated in
    [6, 8, 40]
    >>> adder.relay_history()
    [6]
    >>> multiplier.relay_calculate(4) # (((4 + 1) + 2) * 5)
    35
    >>> multiplier.relay_history()
    [5, 7, 35]
    >>> adder.relay_history() # adder participated most recently in multiplier.relay_calculate(4), where it gave the answer 5
    [5]
    >>> adder.relay_calculate(1)
    2
    >>> adder.relay_history() # adder participated most recently in adder.relay_calculate(1), where it gave the answer 2
    [2]
    >>> multiplier.relay_history() # but the most relay multiplier participated in is still multiplier.relay_calculate(4)
    [5, 7, 35]
    """

    def __init__(
        self, operation: Callable[[int], int], prev_member: TeamMember = None
    ) -> None:
        """
        A TeamMember object is instantiated by taking in an `operation`
        and a TeamMember object `prev_member`, which is the team member
        who "sits in front of" this current team member. A TeamMember also
        tracks a `history` list, which contains the answers given by
        each individual team member.
        """
        self.history: List[int] = []
        self.operation = operation
        self.prev_member = prev_member

    def relay_calculate(self, x: int) -> int:
        """
        The relay_calculate method takes in a number `x` and performs a
        relay by passing in `x` to the first team member's `operation`.
        Then, that answer is passed to the next member's operation, etc. until
        we get to the current TeamMember, in which case we return the
        final answer, `result`.
        """

        if self.prev_member is None:
            self.history = []
            result = self.operation(x)
            self.history += [result]

        else:
            self.history = []
            result = self.operation(self.prev_member.relay_calculate(x))
            self.history += [result]

        if self.prev_member:
            self.history = self.prev_member.history + self.history

        return result

    def relay_history(self) -> List[int]:
        """
        Returns a list of the answers given by each team member in the
        most recent relay the current TeamMember has participated in.
        """
        return self.history


class Cat:
    def __init__(self, name: str, owner: str, lives: int = 9):
        self.is_alive = True
        self.name = name
        self.owner = owner
        self.lives = lives

    def talk(self):
        return self.name + " says meow!"

    @classmethod
    def cat_creator(cls, owner: str):
        """
        Returns a new instance of a Cat.

        This instance's name is "[owner]'s Cat", with
        [owner] being the name of its owner.

        >>> cat1 = Cat.cat_creator("Bryce")
        >>> isinstance(cat1, Cat)
        True
        >>> cat1.owner
        'Bryce'
        >>> cat1.name
        "Bryce's Cat"
        >>> cat2 = Cat.cat_creator("Tyler")
        >>> cat2.owner
        'Tyler'
        >>> cat2.name
        "Tyler's Cat"
        """
        name = f"{owner}'s Cat"
        return cls(name, owner)
