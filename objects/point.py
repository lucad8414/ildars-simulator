import matplotlib.pyplot as plt

class Point:
    """
    Represents a single point in a Cartesian system of any wished dimension.
    Supports a variaty of operations like: print, addition, substraction.
    Basic methods hold for any dimension.
    """
    def __init__(self, coordinates: list[float]):
        self.value = coordinates

    # ------------------------------------------------------------------------
    
    def __str__(self):
        """
        Creates a string of the point like (a,b,c,d,...,z)
        """
        res = ""
        for v in self.value[:-1]:
            res += str(v) + ", "
        res += str(self.value[-1])
        return f"({res})"
    
    # ------------------------------------------------------------------------
    
    def __add__(self, other: "Point") -> "Point":
        """
        Does a pairwise addition and returns a new vector
        
        :param self: own values
        :param other: other values
        :type other: Point
        :return: New Point
        :rtype: Point
        """
        res = []
        for i,_ in enumerate(self.value):
            res.append(self.value[i] + other.value[i])
        return Point(res)
    
    # ------------------------------------------------------------------------
    
    def __sub__(self, other: "Point") -> "Point":
        """
        Does a pairwise substraction.
        
        :param self: own values
        :param other: other values
        :type other: Point
        :return: new Point
        :rtype: Point
        """
        res = []
        for i,_ in enumerate(self.value):
            res.append(self.value[i] - other.value[i])
        return Point(res)

    # ------------------------------------------------------------------------

    def __eq__(self, other: "Point") -> bool:
        """
        Does a list comparison.
        
        :param self: Own Values
        :param other: Other values
        :type other: "Point"
        :return: equality
        :rtype: bool
        """
        return self.value == other.value
        
    # ------------------------------------------------------------------------

    def plot(self, color: str = "blue", name: str = ""):
        """
        Adds the point to the plot with the scaling factor 100.
        
        :param color: Color of the point, default is blue.
        :type color: str
        :param name: label of the point, will be displayed with plt.legend()
        :type name: str
        """
        plt.scatter(self.value[0], self.value[1], s=100, color = color, label=name)