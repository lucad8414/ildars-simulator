import matplotlib.pyplot as plt
from objects.point import Point
from objects.vector import Vector
from typing import Optional
import math
import numpy as np


class Line:
    """
    The most important class of the Project, representing an infinite vector in the 2D field.
    Supports loads of operations, but very specific to 2D.
    Creates a line of following structure:
    (p0,p1) + t * {r0,r1}
    """
    def __init__(self, anchor: Point, direction: Vector):
        self.anchor = anchor
        self.direction = direction 
        self.images: dict[int, list[Point]] = {} # stores all the imaginary points depending on their reflection order.
    
    # ------------------------------------------------------------------------

    def __str__(self):
        """
        Printing the value, by using point and vectors methods.
        """
        return f"{str(self.anchor)} + t * {str(self.direction)}" 
    
    # ------------------------------------------------------------------------

    def point(self, t: float) -> Point:
        """
        Creates a single point on the line. Using the parameter t.
        
        :param self: Start and direction
        :param t: amount of steps in the direction.
        :type t: float
        :return: the point in t steps of direction from anchor.
        :rtype: Point
        """
        return Point([self.anchor.value[0] + t * self.direction.value[0], self.anchor.value[1] + t * self.direction.value[1]])
    
    # ------------------------------------------------------------------------

    def intersection(self, other: tuple[Point, float] | Vector, show: bool = False) -> Optional[Point]:
        """
        Computes the intersection thorogh some Formula, created by solwing the equation of setting two lines equal.
        See documentation in .ipynb.
        Is inteded, for self to be a wall and other to be a vector trying to bounce of that wall.
        If the vectors direction does not match, so t <= 0, then we don't want this intersection.

        Special addition of a point and a radius. This is for the intersection of a Line (in this case not a wall),
        but an extended ray. We use the radius, because directly intersecting with the point in real numbers is nonsense.
        If Line intersects with the circle around the point return the point, else None.
        
        :param self: The line it self, to be intersected with.
        :param other: Other line or Vector to be intersected with (Point not implemented yet).
        :type other: tuple[Point, float] | Vector | Line
        :param show: Add the intersection point to the plot.
        :type show: bool
        :return: Returns the Point, if there is an intersection with the wall through following the direction not opposing!
        :rtype: Point | None
        """
        if isinstance(other, tuple):
            (p,r) = other

            # using the circle formula (x - p0)^2 + (y - p1)^2 = r^2
            # for x and y we substiute our line. x = direction[0] * t + anchor[0] and y = direction[1] * t + anchor[1]
            # then we solve the equation after t:
            # (direction[0] * t + anchor[0] - p0)^2 + (direction[1] * t + anchor[1] - p1)^2 - r^2 = 0
            # (d0 * t + a0 - p0)^2 + (d1 * t + a1 - p1)^2 - r^2 = 0
            # (d0t)^2 + 2d0t(a0-p0) + (a0 - p0)^2 + (d1t)^2 + 2d1t(a1-p1) + (a1 - p1)^2 - r^2 = 0
            # (d0^2 + d1^2) * t^2 + (2d0(a0-p0) + 2d1(a1-p1)) * t + (a0 - p0)^2 + (a1 - p1)^2 - r^2
            # now we use the quadratic formula
            a = self.direction.value[0] ** 2 + self.direction.value[1] ** 2
            b = 2 * self.direction.value[0] * (self.anchor.value[0] - p.value[0]) + 2 * self.direction.value[1] * (self.anchor.value[1] - p.value[1])
            c = (self.anchor.value[0] - p.value[0]) ** 2 + (self.anchor.value[1] - p.value[1]) ** 2 - r ** 2
            
            # check for legal value and also tells us, that there is no intersection.
            if b**2 < 4 * a * c:
                return None
            
            # compute the ts
            t1 = (-b + math.sqrt(b**2 - 4 * a * c)) / (2 * a)
            t2 = (-b - math.sqrt(b**2 - 4 * a * c)) / (2 * a)
            
            # if they are the same we now it is only one intersection, so just touching the circle.
            if t1 == t2:
                return self.point(t1)
            
            # we have to intersections.
            else:
                # compute the distances to the anchor, so the sender or the last reflection point.
                inter1 = self.point(t1)
                inter2 = self.point(t2)
                v1 = Vector(inter1, self.anchor)
                v2 = Vector(inter2, self.anchor)

                # return the closest.
                if abs(v1) < abs(v2):
                    return inter1
                else:
                    return inter2

        
        ext = other
        # we need to extend the vector, incase it takes more then abs(vector) to reach the wall
        if isinstance(other, Vector):
            ext = other.extend()
        
        # for simplicity define the values real quick (we have enough memory)!
        r = [self.direction.value[0], self.direction.value[1]]
        s = [ext.direction.value[0], ext.direction.value[1]]
        p = [self.anchor.value[0], self.anchor.value[1]]
        q = [ext.anchor.value[0], ext.anchor.value[1]]
             
        # This is the divisor, which happens to be the determinant of the matrix (don't know why).
        det = (r[1] * s[0]) - (r[0] * s[1])
        
        # can't be 0, because error and no intersection, because parallel.
        if det == 0:
            return None
        

        # The actual formula, to find y, witch extends other, to intersect with the wall.
        y = (r[1] * (p[0] - q[0]) + r[0] * (q[1] - p[1])) / (det)
        
        # Reversing the vector is not allowed, so we decline that.
        if y > 0:

            # If we want to show the interwsection point.
            if show:
                ext.point(y).plot("red", "Intersection")
            
            return ext.point(y)
        
        # None, because no default value, but can be guarded easily.
        else:
            return None

    # ------------------------------------------------------------------------
    
    def perp_point(self, p: Point, show: bool = False) -> Point:
        """
        A more complex method, but easy to compute. It finds the point on the line, which 
        is perpendicular to the given point p.
        
        :param self: The line we look at
        :param p: The point we want the perpendicular to.
        :type p: Point
        :param show: Add to the plot.
        :type show: bool
        :return: A point on the line with the wished behaviour.
        :rtype: Point
        """
        # Shorter versions for the direction Vector.
        r = [self.direction.value[0], self.direction.value[1]]

        # Create two vectors, which are perpendicular to the Lines direction.
        # In 2D this is only one possibility, but we take both directions, so n and -n.
        # For derivation see .ipynb.
        v1 = Vector(Point([r[1], 2 * r[0]]), Point([2 * r[1], r[0]]))
        v2 = Vector(Point([2 * r[1], r[0]]), Point([r[1], 2 * r[0]]))

        # create lines that contain p and have the given direction.
        l1 = Line(p, v1)
        l2 = Line(p, v2)

        # compute both, because one should be None, due to the constraints in intersection method.
        inter1 = self.intersection(l1)
        inter2 = self.intersection(l2)


        # only return the intersection, which is not None, and show if desired.
        if inter1 is None:

            # check if actually perpendicular.
            assert self.angle(v2) == 0.5 * math.pi
            if show:
                p.plot("black", "anchor")
                inter2.plot("grey","inter point")
                l2.plot("green", "perp line")
            return inter2
        else:

            # check if actually perpendicular.
            assert self.angle(v1) == 0.5 * math.pi
            if show:
                p.plot("black", "anchor")
                inter1.plot("grey","inter point")
                l1.plot("green", "perp line")
            return inter1

    # ------------------------------------------------------------------------

    def image(self, intersection: Point, start: Point, show: bool = False, order: int = 0) -> "Line":
        """
        Implements the "Image-Source-Method" of Ray tracing, which imagines the reflected point as a
        point behind the mirror. This is what is used, to compute the new Ray after a reflection with the
        wall.
        
        :param self: Wall to be reflected of.
        :param intersection: The precomputed intersection point of the vector and the wall.
        :type intersection: Point
        :param start: The previous starting point of the vector (either a reflecting point or the sender).
        :type start: Point
        :param show: Display the entire process for debugging.
        :type show: bool
        :return: Returns a line, with the new computed direction after reflection.
        :rtype: Line
        """
        # Compute the perpendicular Point on the wall (self)
        p = self.perp_point(start, show)
        
        # get the direction vector between the source and the perpendicular point p.
        n = Vector(start, p)

        # follow this point for exactly two units, one to the actual line and one to the perpendicular, imaginary
        # position begin the vector.
        length = abs(n)
        normalized = n.normalized()
        
        # create the imaginary point.
        anchor = Point([start.value[0] + 2 * length * normalized.value[0], start.value[1] + 2 * length * normalized.value[1]])

        # add the anchor to the walls hashmap
        if order in self.images.keys():
            if not anchor in self.images[order]:
                self.images[order].append(anchor)
        
        else:
            self.images[order] = [anchor]


        direction = Vector(anchor, intersection)
        if show:  
            Line(anchor, direction).plot("orange", "Image")
            colors = ["red", "green", "pink", "grey", "orange", "blue", "black", "yellow"]
            anchor.plot(colors[order], "image")

        # create a line with the computed values.
        return Line(anchor, direction)
    
    # ------------------------------------------------------------------------

    def angle(self, other: Vector) -> float:
        """
        Determines the angle between the direction Vectors. 
        Values range from 180° or pi (if they are opposing), to 90° or pi/2 if they are perpendicular
        and 0° or 0 (if they are parallel).
        If they actually intersect or not doesnt matter.
        """
        # Uses the standart fromular for the intersection angle (See .ipynb)
        return np.arccos(self.direction.dot(other) / math.sqrt((self.direction.value[0] ** 2 + self.direction.value[1] ** 2) * (other.value[0] ** 2 + other.value[1] ** 2)))
    
    # ------------------------------------------------------------------------

    def plot(self, color: str = "blue", name: str = ""):
        """
        Plots a line of length 20, will be changed for later, if triangles are complete.
        
        :param self: Own Values
        :param color: color, with default beeing blue.
        :type color: str
        :param name: label to be displayed.
        :type name: str
        """
        a = self.point(-15 * (1/ abs(self.direction)))
        b = self.point(25 * (1/ abs(self.direction)))
        plt.plot([a.value[0], b.value[0]], [a.value[1], b.value[1]], color=color, label=name)

    # ------------------------------------------------------------------------

    def create_circle(self, order: int, color: str = "magenta", name: str = ""):
        """
        Creates a unique circle out of at least 3 image points created through reflections.
        Also adds them to the plot.
        Hardcoded function, just for one plot.
        
        :param self: saved image points
        :param order: Description
        :type order: int
        :param color: Description
        :type color: str
        :param name: Description
        :type name: str
        """
        p = [self.images[order][0]] + self.images[0] + [self.images[order][1]]
        m1 = Point([(p[0].value[0] + p[1].value[0]) / 2, (p[0].value[1] + p[1].value[1]) / 2])
        m2 = Point([(p[2].value[0] + p[1].value[0]) / 2, (p[2].value[1] + p[1].value[1]) / 2])


        v1 = Vector(p[0], p[1])
        v2 = Vector(p[1], p[2])


        orth1 = Vector(Point([v1.value[1], 2 * v1.value[0]]), Point([2 * v1.value[1], v1.value[0]]))
        orth2 = Vector(Point([2 * v2.value[1], v2.value[0]]), Point([v2.value[1], 2 * v2.value[0]]))


        l1 = Line(m1, orth1)
        l2 = Line(m2, orth2)


        center = l1.intersection(l2)
        center2 = l2.intersection(l1)
        angles = np.linspace(0, 2 * np.pi, 50)

        if center2 is None:
            radius = abs(Vector(center, p[0]))
            xs = center.value[0] + radius * np.cos(angles)
            ys = center.value[1] + radius * np.sin(angles)
            center.plot()

        else:
            radius = abs(Vector(center2, p[0]))
            xs = center2.value[0] + radius * np.cos(angles)
            ys = center2.value[1] + radius * np.sin(angles)
            center2.plot()

        plt.plot(xs, ys, color = color, label = name)


