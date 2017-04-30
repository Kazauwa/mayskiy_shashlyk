from haversine import haversine 
import numpy as np
from scipy.spatial import ConvexHull
from server import models


def is_close_enough(first_fire_spot, second_fire_spot):
    acceptable_distance_meters = 500
    first_point = (first_fire_spot.longitude, first_fire_spot.latitude)    
    second_point = (second_fire_spot.longitude, second_fire_spot.latitude)    
    distance_in_meters = haversine(first_point, second_point) * 1000
    return distance_in_meters <= acceptable_distance_meters


def group_fire_spots_by_distance(fire_spots):
    groups = []
    is_in_group = [False for _ in range(len(fire_spots))]
    for start_spot_index, start_spot in enumerate(fire_spots):
        if is_in_group[start_spot_index]:
           continue
        nearby_fire_spots = [start_spot]
        is_in_group[start_spot_index] = True
        for current_spot_index, current_spot in enumerate(fire_spots[start_spot_index + 1:]):
            if is_close_enough(start_spot, current_spot):
                nearby_fire_spots.append(current_spot)
                is_in_group[start_spot_index + 1 + current_spot_index] = True
        groups.append(nearby_fire_spots)
    return groups


def form_polygon_to_spots_relationship(fire_spot_ids, polygon_id):
    spot_polygon_relationships = []
    for fire_spot_id in fire_spot_ids:
        spot_polygon = models.SpotM2MPolygon(polygon_id=polygon_id, spot_id=fire_spot_id)
        spot_polygon_relationships.append(spot_polygon)
    return spot_polygon_relationships


def get_outer_fire_spots(fire_spots):
    coordinates_data = np.matrix([[s.longitude, s.latitude] for s in fire_spots])
    convex_hull_indices = coordinates_data[ConvexHull(coordinates_data).vertices]
    outer_fire_spots = [fire_spots[spot_index] for spot_index in convex_hull_indices]
    return outer_fire_spots
