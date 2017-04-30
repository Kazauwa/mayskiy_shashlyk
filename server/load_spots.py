from models import db_session, FireSpot, FireParams, WeatherParams
import datetime
import requests
import csv
from itertools import cycle


def loading_data(file):
    with open(file, 'r') as csv_file:
        has_header = csv.Sniffer().has_header(csv_file.read(1024))
        csv_file.seek(0)  # rewind
        incsv = csv.reader(csv_file)
        if has_header:
            next(incsv)  # skip header row
        for row in incsv:
            time_string = row[5] + row[6]
            is_day = True if row[12] == 'D' else False
            fire_spot_data = FireSpot(latitude=row[0],
                                      longitude=row[1],
                                      date_time=datetime.datetime.strptime(time_string, "%Y-%m-%d%H%M"),
                                      is_day=is_day)
            fire_params = FireParams(ti4channel=row[2],
                                     ti5channel=row[10],
                                     confidence=row[8],
                                     fire_intens=row[11])
            if fire_params.confidence == 'low':
                continue
            if fire_spot_data.is_day:
                continue
            db_session.add(fire_spot_data)
            db_session.add(fire_params)
    db_session.commit()


def rain_or_not(description):
    if 'rain' in description:
        return True
    elif 'snow' in description:
        return True
    else:
        return False


def get_and_add_to_db_weather_info(lat, lng, obj_id, app_id):
    api_url = 'http://api.openweathermap.org/data/2.5/weather?'
    payload = {'lat': lat, 'lon': lng, 'APPID': app_id}
    weather_info = requests.get(api_url, params=payload)
    speed = weather_info.json().get('wind').get('speed')
    wind_direction = weather_info.json().get('wind').get('deg')
    temperature = weather_info.json().get('main').get('temp')
    humidity = weather_info.json().get('main').get('humidity')
    is_raining = rain_or_not(weather_info.json().get('weather')[0].get('description'))
    weather_params = WeatherParams(object_id=obj_id,
                                   speed=speed,
                                   wind_direction=wind_direction,
                                   temperature=temperature,
                                   humidity=humidity,
                                   is_raining=is_raining)
    db_session.add(weather_params)
    db_session.commit()


if __name__ == '__main__':
    loading_data('VNP14IMGTDL_NRT_Russia_and_Asia_24h.csv')
    APPIDS = ['caf3f5b090bad4ab4f01d448894f54ce', '12d818fdb905bc4498c10f89ed0ec678',
              'fbbeb308b9952d73e6bbca79f7e5d454',
              '40147f09120777a7b624ade7be19b755', '431232f6deabb63aa4d90efdafde6007']
    keys = cycle(APPIDS)
    spots_id_list = [(item_id.latitude, item_id.longitude, item_id.id) for item_id in db_session.query(FireSpot)]
    for item in spots_id_list:
        get_and_add_to_db_weather_info(item[0], item[1], item[2], next(keys))
