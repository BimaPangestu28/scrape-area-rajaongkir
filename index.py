import requests
import os
import csv


class Scrape:
    def __init__(self):
        self.api_key = "84a3c4c90fe80707cfd5648eb9f5d855"
        self.base_url = "https://pro.rajaongkir.com/api/"

    def generate_values(self, keys, data):
        values = []
        for key in keys:
            values.append(data[key])

        return values

    def generate_request(self, path, params={}):
        headers = {'key': self.api_key }

        return requests.get("{}{}".format(self.base_url, path), headers=headers, params=params)

    def get_province(self):
        r = self.generate_request('province')

        if os.path.isdir('results') == False:
            os.mkdir('results')

        province_ids = []

        with open('results/province.csv', 'w', newline='') as file:
            writer = csv.writer(file)

            keys = ['province_id', 'province']
            writer.writerow(keys)

            for province in r.json()['rajaongkir']['results']:
                writer.writerow(self.generate_values(keys, province))
                province_ids.append(province['province_id'])

                print('Berhasil menyimpan data provinsi {}'.format(
                    province['province']))

        self.get_city(province_ids)

    def get_city(self, province_ids):
        city_ids = []

        with open('results/city.csv', 'w', newline='') as file:
            writer = csv.writer(file)

            keys = ['city_id', 'province_id', 'province',
                    'type', 'city_name', 'postal_code']
            writer.writerow(keys)

            for province_id in province_ids:
                r = self.generate_request('city', {'province': province_id})

                for city in r.json()['rajaongkir']['results']:
                    writer.writerow(self.generate_values(keys, city))
                    city_ids.append(city['city_id'])

                    print('Berhasil menyimpan data kota {}'.format(
                        city['city_name']))

        self.get_subdistrict(city_ids)

    def get_subdistrict(self, city_ids):
        with open('results/subdistrict.csv', 'w', newline='') as file:
            writer = csv.writer(file)

            keys = ['subdistrict_id', 'province_id', 'province',
                    'city_id', 'city', 'type', 'subdistrict_name']
            writer.writerow(keys)

            for city_id in city_ids:
                r = self.generate_request('subdistrict', {'city': city_id})

                for subdistrict in r.json()['rajaongkir']['results']:
                    writer.writerow(self.generate_values(keys, subdistrict))
                    print('Berhasil menyimpan data kecamatan {}'.format(
                        subdistrict['subdistrict_name']))


scrape = Scrape()

scrape.get_province()
