from objects.ray import Ray
from objects.line import Line
from objects.vector import Vector
from objects.point import Point
import numpy as np
import matplotlib.pyplot as plt

class Engine:
    def __init__(self):
        self.walls = []
        self.sender = None
        self.reciever = Point([0.,0.])
        self.radius = 0.125 # Important HYPERPARAMETER, represents the buffer for floats.
        self.rays = []
    
    def generate(self):
        """
        Docstring for generate
        
        No angles larger then 120° and smaller then 30°
        arccos does only allow values from 0 = 0 degrees to pi = 180 degrees.
        120° = 2pi/3 and 30° = pi/6
        150° and 60° is also possible, just less then 90° difference, else the triangle gets to large
        :param self: Description
        """
        rng = np.random.default_rng()
        # generate the angular range
        alpha = rng.uniform(low=(np.pi/6), high=(2*np.pi / 3))
        print(alpha)
        beta = rng.uniform(low=np.pi/6, high=(np.pi - alpha))
        print(beta)

        # generate random starting point and line
        base = Line(Point([-5., -10.]), Vector(Point([0.,0.]), Point([0.7, -0.2])))
        right = Line(Point([10.,-6.]), Vector(Point([0.,0.]), Point([-1., 2.5])))
        left = Line(Point([-10.,-6.]), Vector(Point([0.,0.]), Point([1., 1.5])))
        self.walls = [base,right,left]
        # generate another line from the anfgular range to l1

        # generate another line from the angular range to l1

        # generate points in random positions for sender and reciever.
        flag = True
        s = Point([rng.uniform(low=-10., high=10.), rng.uniform(low=-3., high=10)])
        
        flags = []
        for w in self.walls:
            pass
        
        while flag:
            flag = False
        
        self.sender = Point([1., -7.])
        # think of some bounds: how far from each other? how far from each wall at least?


    def sound_events(self, max_order: int, show: bool = False):
        """
        Docstring for sound_events
        
        Area for the reciever, where it is legal to mark a sound as an hit.
        Or other approach, create all reflections in the possible order and use
        only those intersecting with a point and its other area.
        :param self: Positions and Rays, so the entire dataset.
        :param max_order: The maximum order reflection. Only less iff recieved.
        """
        assert max_order >= 0

        ROUNDS = 720 # Important HYPERPARAMETER, amount of Signals, which are send.

        # compute all the rays, with each having a unique outgoing angle of the sender.
        for x in range(ROUNDS):
            ray = Ray(Vector(self.sender, Point([self.sender.value[0] + np.cos((2 * np.pi)* (x/ROUNDS)), self.sender.value[1] + np.sin((2* np.pi)* (x/ROUNDS))])), max_order)
            
            # expend every ray and add it to the ray collection.
            ray.expand(self.walls, (self.reciever, self.radius) , show)
            self.rays.append(ray)
        

        # plot all the recieved points (only recieved, because else its just a black mess).
        for r in self.rays:
            if r.recieved:
                r.plot()
                r.pov((self.reciever, self.radius))
        
        # plot the walls and their reflection behaviour if desired.
        for w in self.walls:
            w.plot()
            if max_order >= 1:
                # w.create_circle(1)
                pass
        
        # plot the two points.
        self.sender.plot()
        self.reciever.plot("cyan")
        
    
if __name__ == "__main__":
    # some settings for good plots.
    e = Engine()
    e.generate()
    e.sound_events(4, False) # orders of reflection, which are allowed.
    plt.autoscale(False)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
        

        
