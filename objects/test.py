from point import Point
from vector import Vector
from line import Line
from ray import Ray
import math
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------

def test_point(show: bool = False):
    """
    Tests basic methods on points.
    
    :param show: Adds the points with specifications to the plot.
    :type show: bool
    """
    p = Point([1., 5.])
    q = Point([-3.,7.])
    
    assert (p + q).value == [-2., 12.] # addition
    assert (p - q).value == [4., -2.] # substraction
    assert str(p) == "(1.0, 5.0)" # string
    
    # add to the plot.
    if show:
        p.plot()
        q.plot()

# ----------------------------------------------------------------------------

def test_vector(show: bool = False):
    p = Point([1., 5.])
    q = Point([-3.,7.])
    v = Vector(p,q)
    s = Point([5.,8.])
    t = Point([-3.,0.])
    u = Vector(s,t)
    l = v.extend()
    f = Point([0.,0.])
    r = Vector(f,f)
    assert v.dot(u) == 16.
    assert abs(u) == math.sqrt(128)
    assert u.scalar(-1.).value == [8.,8.]
    assert abs(v.normalized()) == 1.
    assert abs(r) == 0
    if show:
        v.plot()
        u.plot()
        plt.show()

        

# ----------------------------------------------------------------------------

def test_line(show: bool = False):
    p = Point([1., 5.])
    q = Point([-3.,7.])
    v = Vector(p,q)
    s = Point([5.,8.])
    t = Point([-3.,0.])
    u = Vector(s,t)
    a = Point([-4., 4.])
    b = Point([-2.,2.])
    w = Vector(a,b)
    l = Line(p, v)
    r = Line(s, u)
    y = Line(a, w)
    assert l.angle(v) == 0.
    assert l.angle(v.scalar(-1.)) == math.pi
    if show:
        inter = l.intersection(r, True)
        l.image(inter, r.anchor, True)
        l.plot("blue")
        r.plot("black")
        y.plot("yellow")
        plt.legend()
        plt.show()

# ----------------------------------------------------------------------------

def test_ray(show: bool = False):
    p = Point([1., 5.])
    q = Point([-3.,7.])
    v = Vector(p,q)
    s = Point([5.,8.])
    t = Point([-3.,0.])
    u = Vector(s,t)
    a = Point([-4., 4.])
    b = Point([-2.,2.])
    w = Vector(a,b)
    l = Line(p, v)
    r = Line(s, u)
    y = Line(a, w)
    c = Point([-2., 4.])
    d = Point([-1., 5.])
    ray = Ray(Vector(c,d), 3)
    walls = [l,r,y]
    ray.expand([l,r,y], show)

    if show:
        for wall in walls:
            wall.plot()
        ray.plot()
        
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    test_point()
    test_vector()
    test_line()
    test_ray(True)
    plt.xlim(-15, 15)
    plt.ylim(-15, 15)
    plt.autoscale(False)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.legend()
    plt.show()
