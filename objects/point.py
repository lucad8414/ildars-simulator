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
        plt.scatter(self.value[0], self.value[1], s=30, color = color, label=name)
        plt.text(self.value[0], self.value[1], name, size=8, color="green")


    def compute_image_point(sender: "Point", reflection_path, walls: list) -> "Point":
        """
        Rebuild the image point I_w directly from the sender and the
        ordered list of wall labels in `reflection_path`, e.g. [2, 1, 3]
        for the path you currently label "I213".
    
        This is the replacement for `pov()`'s reconstruction via
        `distance + rad`. It uses only the wall mirror formula, so it
        carries no dependence on the receiver radius at all.
    
        :param sender: the original sender position, as a Point
        :param reflection_path: ordered list of wall indices, first
            reflection first, exactly the order already encoded in your
            path labels like "I213" -> [2, 1, 3]
        :param walls: dict mapping a wall index (1, 2, 3) to its Line
        :return: the exact image point I_w, as a Point
        """
        current = sender
        for wall_index in reflection_path:
            wall = walls[wall_index - 1]
            current = wall.mirror(current)
        return current