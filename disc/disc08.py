import math

pi = math.pi


class Shape:
    """All geometric shapes will inherit from this Shape class."""

    def __init__(self, name: str):
        self.name = name

    def area(self):
        """Returns the area of a shape"""
        print("Override this method in ", type(self))

    def perimeter(self):
        """Returns the perimeter of a shape"""
        print("Override this function in ", type(self))


class Circle(Shape):
    """A circle is characterized by its radii"""

    def __init__(self, name: str, radius: float):
        super().__init__(name)
        self.radius = radius

    def perimeter(self):
        """Returns the perimeter of a circle (2πr)"""
        return 2 * pi * self.radius

    def area(self):
        """Returns the area of a circle (πr^2)"""
        return pi * self.radius**2


class RegPolygon(Shape):
    """A regular polygon is defined as a shape whose angles and side lengths are all the same.
    This means the perimeter is easy to calculate. The area can also be done, but it's more inconvenient."""

    def __init__(self, name: str, num_sides: int, side_length: float):
        super().__init__(name)
        self.side_num = num_sides
        self.side_len = side_length

    def perimeter(self):
        """Returns the perimeter of a regular polygon (the number of sides multiplied by side length)"""
        return self.side_num * self.side_len


class Square(RegPolygon):
    def __init__(self, name: str, side_length: float):
        super().__init__(name, 4, side_length)

    def area(self):
        """Returns the area of a square (squared side length)"""
        return self.side_len**2


class Triangle(RegPolygon):
    """An equilateral triangle"""

    def __init__(self, name: str, side_length: float):
        super().__init__(name, 3, side_length)

    def area(self):
        """Returns the area of an equilateral triangle is (squared side length multiplied by the provided constant"""
        constant = math.sqrt(3) / 4
        return constant * self.side_len**2


class Pet:
    def __init__(self, name: str, owner: str):
        self.is_alive = True  # It's alive!!!
        self.name = name
        self.owner = owner

    def eat(self, thing: str):
        print(self.name + " ate a " + str(thing) + "!")

    def talk(self):
        print(self.name)


class Cat(Pet):
    """
    >>> cat = Cat("Felix", "Kevin")
    >>> cat
    Felix, 9 lives
    >>> cat.lose_life()
    >>> cat
    Felix, 8 lives
    >>> print(cat)
    Felix
    """

    def __init__(self, name: str, owner: str, lives: int = 9):
        super().__init__(name, owner)
        self.lives = lives

    def __repr__(self):
        return f"{self.name}, {self.lives} lives"

    def __str__(self):
        return self.name

    def talk(self):
        """Print out a cat's greeting.

        >>> Cat('Thomas', 'Tammy').talk()
        Thomas says meow!
        """
        print(f"{self.name} says meow!")

    def lose_life(self):
        """Decrements a cat's life by 1. When lives reaches zero,
        is_alive becomes False. If this is called after lives has
        reached zero, print 'This cat has no more lives to lose.'
        """
        self.lives -= 1
        assert self.lives >= 0, "lives error"
        if self.lives == 0:
            self.is_alive = False
        if self.is_alive is False:
            print("This cat has no more lives to lose.")

    def revive(self):
        """Revives a cat from the dead. The cat should now have
        9 lives and is_alive should be true. Can only be called
        on a cat that is dead. If the cat isn't dead, print
        'This cat still has lives to lose.'
        """
        if not self.is_alive:  # 如果貓死了
            self.is_alive = True
            self.lives = 9
        else:
            print("This cat still has lives to lose.")


class NoisyCat(Cat):  # Fill me in!
    """A Cat that repeats things twice."""

    def talk(self):
        """Talks twice as much as a regular cat.
        >>> NoisyCat('Magic', 'James').talk()
        Magic says meow!
        Magic says meow!
        """
        print(f"{self.name} says meow!")
        print(f"{self.name} says meow!")
