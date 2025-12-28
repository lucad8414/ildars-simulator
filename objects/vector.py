import matplotlib.pyplot as plt
from objects.point import Point
import math

class Vector:
    """
    A Vector is a representation of a specific distance in the Cartesian field.
    Has some basic methods and the ability to be plottet, as an arrow with the
    given direction of the distance.
    Not all methods are multi dimensional, some are only for 2D.
    """
    def __init__(self, v: Point, u: Point):
        self.anchor = v # keep this as a referencing point on the line, is needed for later.
        self.end = u
        tmp = u - v # creation of the distance via difference vector
        self.value = tmp.value # the actual distance.
    
    # ------------------------------------------------------------------------

    def __abs__(self) -> float:
        """
        Overrides the absolute value, which is the length of the vector.
        """
        res = 0.

        # sum the square of all coordinates in the vector.
        for v in self.value:
            res += v ** 2

        # take the square root.
        return math.sqrt(res)
    
    # ------------------------------------------------------------------------

    def __str__(self):
        """
        Creates a string of the vector like {a,b,c,d,...,z}
        """
        res = ""
        for v in self.value[:-1]:
            res += str(v) + ", "
        
        # exception for the last entry, because it does not need a coma.
        res += str(self.value[-1])
        return f"{{{res}}}"
    
    # ------------------------------------------------------------------------

    def scalar(self, scalar: float) -> "Vector":
        """
        Performs the scalar multiplication on the vector, with a given scalar.
        Does not change the value of the distance, but returns a updated new one.

        :type scalar: float
        :return: new Vector object with the same attributes as self, but new length.
        :rtype: Vector
        """
        res = []
        # multiply everything with the scalar.
        for x in self.value:
            res.append(x * scalar)
        
        # created the updated clone.
        return Vector(self.anchor, self.anchor + Point(res))

    # ------------------------------------------------------------------------

    def normalized(self) -> "Vector":
        """
        Returns a normalized version of the object, but with length 1.
        
        :return: self with length = 1.
        :rtype: Vector
        """
        # get current length
        scalar = abs(self)

        # protecting agains Zero division
        if self.value == [0., 0.]:
            return self
        
        # do the inverse scaling.
        return self.scalar(1. / scalar)

    # ------------------------------------------------------------------------

    def dot(self, other: "Vector") -> float:
        """
        Computes the Dot product of two given vectors.
        
        :param self: Own vector
        :param other: Other vector
        :type other: "Vector"
        :return: Sum of products.
        :rtype: float
        """
        res = 0.
        for i,_ in enumerate(self.value):
            
            # sum the product of each pairwise multiplication.
            res += self.value[i] * other.value[i]
        
        return res

    # ------------------------------------------------------------------------

    def extend(self):
        """
        Extends the vector, so the specific distance to a Line object, which is the
        same, but with arbitrary length depending on the parameter t.
        
        :param self: Own object with direction and anchor.
        :return: Line with the direction of the vector.
        :rtype: Line
        """
        # Imports Line here due to circular import, hence no type declariation for return.
        from objects.line import Line

        # creates a Line object with given values.
        return Line(self.anchor, self)

    # ------------------------------------------------------------------------

    def plot(self, color: str = "black", name: str = ""):
        """
        Adds the distance, with its length, direction and starting point to the plot.
        Uses the arrow method, do add a small arrow to the front, to display its direction in the plot.
        
        :param self: Own values
        :param color: color of the arrow, with black as default.
        :type color: str
        :param name: Label, which is later displayed in the legend.
        :type name: str
        """
        plt.arrow(self.anchor.value[0], self.anchor.value[1],
          self.value[0], self.value[1],
          length_includes_head=True,
          head_width=0.1,
          head_length=0.2, color=color, label=name)