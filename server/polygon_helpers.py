import numpy as np
from scipy.spatial import ConvexHull

import models


def get_convex_hull_from(fire_spots):
    coordinates_data = np.matrix([[s.longitude, s.latitude] for s in fire_spots])
    return coordinates_data[ConvexHull(coordinates_data).vertices]


if __name__ == '__main__':
    hull_vertices = get_convex_hull_from(models.FireSpot.query.all()[:10])
    print(hull_vertices)
