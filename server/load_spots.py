from models import db_session, FireSpot, FireParams, WeatherParams
import datetime
import requests
import json
import csv


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
            db_session.add(fire_spot_data)
            db_session.add(fire_params)
    db_session.commit()


def get_weather_info(lat, lng):
    api_url = 'http://api.openweathermap.org/data/2.5/weather'
    payload = {'lat': lat, 'lng': lng, 'APPID': '12d818fdb905bc4498c10f89ed0ec678'}
    weather_info = requests.get(api_url, params=payload)
    return weather_info.json


def add_weather_info_to_db(weather_info, obj_id):
    weather_params = WeatherParams(object_id=obj_id,
                                   speed=weather_info['wind']['speed'],
                                   wind_direction=weather_info['wind']['deg'],
                                   temperature=weather_info['main']['temp'],
                                   humidity=weather_info['main']['humidity'],
                                   is_raining=1 if 'rain' or 'snow' in weather_info['weather']['description'] else 0)
    db_session.add(weather_params)
    db_session.commit()


if __name__ == '__main__':
    loading_data('../../VNP14IMGTDL_NRT_Russia_and_Asia_7d.csv')
