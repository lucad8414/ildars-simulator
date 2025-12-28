import numpy as np


class Vector:
    def __init__(self, anc: np.array, dir: np.array):
        self.dir = dir
        self.anc = anc

    def size(self) -> float:
        return np.sqrt(self.dir ** 2 + self.anc ** 2)
    
    def __str__(self):
        return f"({self.anc[0]}, {self.anc[1]}) + t * ({self.dir[0]}, {self.dir[1]})"
    
    def intersect(self, other: "Vector", verbose: bool) -> np.array:
        """
        Computes the intersection between two Vectors.
        Raises an error, if the Vectors are parrallel, but should never happen.
        Changes the direction vectors, such that they intersect.
        verbose prints the updatet direction vectors.
        """
        # assert dot_product(self, other) != 0
        
        # anc + x * dir = anc2 + y * dir2 | -anc
        # x * dir = anc2 - anc + y * dir2 | -y * dir2
        # x * dir - y * dir2 = anc2 - anc <= LGS
        # -------------------------------------
        # x * 1dir - y * 1dir2 = 1anc2 - 1anc
        # x * 2dir - y * 2dir2 = 2anc2 -2anc
        # -------------------------------------
        # x * 1dir - y * 1dir2 = 1anc2 - 1anc
        # x = (2anc2 - 2anc + y * 2dir2) / 2dir
        # -------------------------------------
        # ((2anc2 - 2anc + y * 2dir2) / 2dir) * 1dir - y * 1dir2 = 1anc2 - 1anc
        # x = (2anc2 - 2anc + y * 2dir2) / 2dir
        # -------------------------------------
        # (2anc2 - 2anc) * 1dir/2dir + y * 2dir2 * 1dir / 2dir - y * 1dir2 = 1anc2 - 1anc
        # x = (2anc2 - 2anc + y * 2dir2) / 2dir
        # -------------------------------------
        # y * (2dir2 * 1dir / 2dir - 1dir2) = 1anc2 - 1anc - (2anc2 - 2anc) * 1dir/2dir
        # x = (2anc2 - 2anc + y * 2dir2) / 2dir
        # -------------------------------------
        # y = (1anc2 - 1anc - (2anc2 - 2anc) * 1dir/2dir) / (2dir2 * 1dir / 2dir - 1dir2)
        # x = (2anc2 - 2anc + y * 2dir2) / 2dir

        print(self.dir[0], self.dir[1])
        print(other.anc[0] - self.anc[0] - (other.anc[1] - self.anc[1]) * self.dir[0]/self.dir[1])
        print((other.dir[1] * self.dir[0] / self.dir[1] - other.dir[0]))
        y = (other.anc[0] - self.anc[0] - (other.anc[1] - self.anc[1]) * self.dir[0]/self.dir[1]) / (other.dir[1] * self.dir[0] / self.dir[1] - other.dir[0])
        x = (other.anc[1] - self.anc[1] + y * other.dir[1]) / self.dir[1]

        # update the vectors:
        return [self.dir[0] * x + self.anc[0], self.dir[1] * x + self.anc[1]]

        if verbose:
            print("Own vector:", str(self))
            print("Other vector:", str(other))

    def relative_pos(self, point: np.array) -> bool:
        """
        checks whether a point is inside or outside of the triangle.
        True if inside, False if outside.
        """

        # we are the left wall, so left of it is outside
        if self.anc == np.array([0., 0.]):
            pass

        # we are the right wall, so left is inside
        else:
            pass

        
def dot_product(v1: Vector, v2: Vector) -> float:
    return sum(v1.dir[i] * v2.dir[i] for i in range(len(v1.dir)))

def create_triangle(angles: list[float], base: float):
    bot = np.array([0., base])
    left = np.array([1.,np.sin(angles[0])])
    right = np.array([1.,np.cos(angles[1])])
    return (bot, (np.array([0.,0.], left)), right)

def intersection(left: np.array, right: np.array) -> np.array:
    x = 1
    y = 1
    

if __name__ == "__main__":
    x = np.array([1,2,3,4])
    print(x[0], x[1], x[2], x[3])
    v = Vector(np.array([0,0]), np.array([2,2]))
    u = Vector(np.array([2,0]), np.array([-2,2]))
    print(v.intersect(u, False))