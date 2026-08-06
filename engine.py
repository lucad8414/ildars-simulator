from objects.ray import Ray
from objects.line import Line
from objects.vector import Vector
from objects.point import Point
import numpy as np
import matplotlib.pyplot as plt
import os
import objects.analytics as analysis
import math


ROUNDS = 20000 # Important HYPERPARAMETER, amount of Signals, which are send.


class Engine:
    def __init__(self):
        self.walls = []
        self.sender = None
        self.reciever = Point([0.,0.])
        self.radius = 0.0125 # Important HYPERPARAMETER, represents the buffer for floats.
        self.rays = []
        self.images = []
        self.edm = []
        self.distance_pairs = {}

    
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
        base = Line(Point([-5., -10.]), Vector(Point([0.,0.]), Point([15, -6.0]))) # 1
        right = Line(Point([10.,15.]), Vector(Point([0.,0.]), Point([25, -30]))) # 2
        left = Line(Point([-12., 0.]), Vector(Point([0.,0.]), Point([3.4, 10.0]))) # 3
        additional = Line(Point([17.,-1.]), Vector(Point([0.,0.]), Point([0., 10.])))
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
        
        self.sender = Point([10., 2.])
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


        # compute all the rays, with each having a unique outgoing angle of the sender.
        for x in range(ROUNDS):
            ray = Ray(Vector(self.sender, Point([self.sender.value[0] + np.cos((2 * np.pi)* (x/ROUNDS)), self.sender.value[1] + np.sin((2* np.pi)* (x/ROUNDS))])), max_order)
            
            # expend every ray and add it to the ray collection.
            ray.expand(self.walls, (self.reciever, self.radius) , False)
            self.rays.append(ray)
        

        # plot all the recieved points (only recieved, because else its just a black mess).
        for r in self.rays:
            if r.recieved:
                r.plot()
                
                # only take image points once, many are multile, because of rounding buffer.
                img = r.pov((self.reciever, self.radius))
                add = True
                for e in self.images:
                    if img[1] == e[1]:
                        add = False
                        break
                
                if add:
                    self.images.append(img)
                

                r.expanded = False
                r.recieved = False
                r.value = r.values[0]
                r.values = []
                r.expand(self.walls, (self.reciever, self.radius) , True)

        # plot the walls and their reflection behaviour if desired.
        for w in self.walls:
            w.plot()
            if max_order >= 1:
                # w.create_circle(1)
                pass
        
        # plot the two points.
        self.sender.plot()
        self.reciever.plot("cyan")


    def create_edm(self):
        # initilize the entire edm
        self.edm = [[None for _ in range(len(self.images) + 1)] for _ in range(len(self.images) + 1)]

        # corner with no value
        self.edm[0][0] = " "

        # add the labels to all the rows and columns
        for index, pair in enumerate(self.images):
            self.edm[0][index + 1] = pair[1]
            self.edm[index + 1][0] = pair[1]
        
        row = 1
        column = 1
        while row < len(self.images) + 1:
            while column < len(self.images) + 1:
                self.edm[row][column] = abs(Vector(Point(self.images[row - 1][0].value), Point(self.images[column - 1][0].value)))
                column += 1
            column = 1
            row += 1


    def round_up(self, n, decimals=0):
        factor = 10 ** decimals
        return math.ceil(n * factor) / factor


    def compare_point_pair_distances(self, nd: int):
        # self.distance_pairs hashes distances with their respective labeling
        # check every element, even though it is symetric, but this is easier
        for i, row in enumerate(self.edm[1:]):
            for j, el in enumerate(row[1:]):

                if self.images[i][1] == self.images[j][1]:
                    continue
                
                # prepair the entry for comparison
                item = (self.images[i][1], self.images[j][1])

                # this distance exists already
                if self.round_up(el, nd) in self.distance_pairs.keys():
                    # check if its just the symmetric counter part.
                    if not (self.images[j][1], self.images[i][1]) in self.distance_pairs[self.round_up(el, nd)]:
                        self.distance_pairs[self.round_up(el, nd)].append(item)

                # new distance
                else:
                    self.distance_pairs[self.round_up(el, nd)] = [item]


if __name__ == "__main__":
    # some settings for good plots.
    reflection_order = 5
     
    e = Engine()
    e.generate()
    e.sound_events(reflection_order, True) # orders of reflection, which are allowed.
    e.create_edm()
    print("Unfiltered EDM", e.edm)
    print("Image points captured with (Position, Label): \n", e.images)
    line = ""
    for row in e.edm:
        line += "["
        for el in row:
            if isinstance(el, float):
                line += str(round(el, 5)) + ", "
            else:
                line += el +", "
        line += "]\n"
    print("Rounded and formatted data", line)

    e.compare_point_pair_distances(1)
    print("Unfilted distance pairs", e.distance_pairs)
    print()
    filtered_data = {}
    for key, value in e.distance_pairs.items():
        if len(value) > 1:
            filtered_data[key] = value

    print("Filtered data", filtered_data)

    seperated_data = {}
    for dist, line in filtered_data.items():
        G, comp = analysis.analyze_distance_row(line)
        main, residual, isolated = analysis.evaluate_components(comp)
        seperated_data[dist] = [main, residual, isolated]
        print(f"{dist}: Main: {main},\n Residual: {residual},\n Isolated: {isolated}\n")


    plt.autoscale(False)
    plt.gca().set_aspect('equal', adjustable='box')
    fig = plt.gcf()
    filename = f"data/o{reflection_order}s{ROUNDS}r{int(1000 * e.radius)}.png"
    fig.savefig(filename)
    plt.show()

    save = True if str(input("Save this plot? Y / N: ")) == "Y" else False
    if not save:
       os.remove(filename) 
    plt.close(fig)


    

        
