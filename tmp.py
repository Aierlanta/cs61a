class TeamMember:
    """>>> adder = TeamMember(lambda x: x + 1) # team member at front
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
    def __init__(self, operation, prev_member=None):
        """
        A TeamMember object is instantiated by taking in an `operation`
        and a TeamMember object `prev_member`, which is the team member
        who "sits in front of" this current team member. A TeamMember also
        tracks a `history` list, which contains the answers given by
        each individual team member.
        """
        self.history = []
        self.operation = operation # Store the operation as an attribute
        self.prev_member = prev_member # Store the previous member as an attribute

    def relay_calculate(self, x):
        """
        The relay_calculate method takes in a number `x` and performs a
        relay by passing in `x` to the first team member's `operation`.
        Then, that answer is passed to the next member's operation, etc. until
        we get to the current TeamMember, in which case we return the
        final answer, `result`. 
        """
        if self.prev_member is None: # Check if this is the first member in the relay
            result = self.operation(x) # Apply the operation to x
        else:
            result = self.operation(self.prev_member.relay_calculate(x)) # Apply the operation to the result of the previous member
        self.history.append(result) # Append the result to the history list
        return result # Return the final result

    def relay_history(self):
        """
        Returns a list of the answers given by each team member in the
        most recent relay the current TeamMember has participated in.
        """
        if self.prev_member is None: # Check if this is the first member in the relay
            return self.history # Return the history list
        else:
            return self.prev_member.relay_history() + self.history # Return the history list of the previous member plus the current member
