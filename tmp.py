from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, List
import inspect
from functools import partial


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
    >>> divider = TeamMember(lambda x: x / 2, multiplier) # team member 4
    >>> divider.relay_calculate(4) # ((((4 + 1) + 2) * 5) / 2)
    17.5
    >>> divider.relay_history()
    [5, 7, 35, 17.5]
    >>> divider.relay_calculate(0) # ((((0 + 1) + 2) * 5) / 2)
    7.5
    >>> divider.relay_history()
    [1, 3, 15, 7.5]
    >>> divider2 = TeamMember(partial(lambda x, y: x / y, 10), divider) # team member 5
    >>> divider2.relay_calculate(4) # ((((((4 + 1) + 2) * 5) / 2) / 10)
    1.75
    >>> divider2.relay_history()
    [5, 7, 35, 17.5, 1.75]
    >>> divider2.relay_calculate(0) # ((((((0 + 1) + 2) * 5) / 2) / 10)
    0.75
    >>> divider2.relay_history()
    [1, 3, 15, 7.5, 0.75]
    >>> divider3 = TeamMember(lambda x: x / 0, divider2) # team member 6
    >>> divider3.relay_calculate(4) # (((((((4 + 1) + 2) * 5) / 2) / 10) / 0)
    Traceback (most recent call last):
    ...
    ZeroDivisionError: division by zero
    >>> divider3.relay_history()
    [5, 7, 35, 17.5, 1.75, 'ZeroDivisionError: division by zero']
    >>> divider2.relay_history()
    [17.5, 1.75, 'ZeroDivisionError: division by zero']
    >>> divider.relay_history()
    [35, 17.5, 'ZeroDivisionError: division by zero']
    >>> multiplier.relay_history()
    [7, 35, 'ZeroDivisionError: division by zero']
    >>> adder2.relay_history()
    [6, 'ZeroDivisionError: division by zero']
    >>> adder.relay_history()
    [5, 'ZeroDivisionError: division by zero']
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
        self.history = []  # clear the history list
        if self.prev_member is None:
            try:
                result = self.operation(x)
                self.history.append(result)
            except Exception as e:
                self.history.append(str(e))
                raise e
        else:
            try:
                result = self.operation(self.prev_member.relay_calculate(x))
                self.history.append(result)
            except Exception as e:
                self.history.append(str(e))
                raise e
        return result

    def relay_history(self) -> List[int]:
        """
        Returns a list of the answers given by each team member in the
        most recent relay the current TeamMember has participated in.
        """
        param_count = len(
            inspect.getfullargspec(self.operation).args
        )  # get the operation's parameter count
        return self.history[-param_count:]
