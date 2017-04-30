import numpy as np
from haversine import haversine
from scipy.spatial import ConvexHull
import models


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


def form_polygon_to_spots_relationships(fire_spot_ids, polygon_id):
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


def store_polygons():
    fire_spots = models.FireSpot.query.all()
    fire_spot_groups = group_fire_spots_by_distance(fire_spots)
    for spot_group in fire_spot_groups:
        polygon = models.Polygon(type='Fire')
        models.db_session.add(polygon)
        models.db_session.commit()
        spot_group_ids = [spot.id for spot in spot_group]
        polygon_to_spots = form_polygon_to_spots_relationships(spot_group_ids, polygon.id)
        models.db_session.add_all(polygon_to_spots)
        models.db_session.commit()


def determine_fire_center(fire_polygon):
    spot_polygon_relationships = models.SpotM2MPolygon.query.filter_by(polygon_id=fire_polygon.id).all()
    spot_ids = [relationship.spot_id for relationship in spot_polygon_relationships]
    spots = models.FireSpot.query.filter(models.FireSpot.id.in_(spot_ids)).all()
    oldest_spot = min(spots, key=lambda x: x.date_time)
    return oldest_spot


def store_firestart_polygon(fire_polygon, db_session):
    fire_center = determine_fire_center(fire_polygon)
    fake_fire_spot1 = models.FireSpot(
        latitude=fire_center.latitude + 0.001,
        longitude=fire_center.longitude,
        date_time=fire_center.date_time,
        is_day=fire_center.is_day
    )
    fake_fire_spot2 = models.FireSpot(
        latitude=fire_center.latitude,
        longitude=fire_center.longitude + 0.001,
        date_time=fire_center.date_time,
        is_day=fire_center.is_day
    )
    fake_fire_spot3 = models.FireSpot(
        latitude=fire_center.latitude + 0.001,
        longitude=fire_center.longitude + 0.001,
        date_time=fire_center.date_time,
        is_day=fire_center.is_day
    )
    firestart_polygon = models.Polygon(type='fire_start')
    db_session.add_all(
        [
            fake_fire_spot1,
            fake_fire_spot2,
            fake_fire_spot3,
            firestart_polygon
        ]
    )
    db_session.commit()
    fake_fire_spot1_relationship = SpotM2MPolygon(
        polygon_id=firestart_polygon.id,
        spot_id=fake_fire_spot1.id
    )
    fake_fire_spot2_relationship = SpotM2MPolygon(
        polygon_id=firestart_polygon.id,
        spot_id=fake_fire_spot1.id
    )
    fake_fire_spot3_relationship = SpotM2MPolygon(
        polygon_id=firestart_polygon.id,
        spot_id=fake_fire_spot1.id
    )
    db_session.add_all(
        [
            fake_fire_spot1_relationship,
            fake_fire_spot2_relationship,
            fake_fire_spot3_relationship
        ]
    )
    db_session.commit()


if __name__ == '__main__':
    store_polygons()
