import time
import pandas as pd
import csv
from threading import RLock
from WeatherGetter import WeatherGetter
from pathlib import Path


output_filename_HU = 'weather_data_HU.csv'
output_filename_IE = 'weather_data_IE.csv'

def convert_to_xlsx(input_filename, output_filename):
    df = pd.read_csv(input_filename, sep=';', on_bad_lines='warn', engine='python')
    df.to_excel(output_filename, sheet_name="Data", index=False)


def main():
    
    city_list_HU = ('Sopron', 'Pécs', 'Budapest', 'Kecskemét', 'Debrecen')
    city_list_IE = ["Dublin","Cork","Limerick","Galway","Waterford","Drogheda","Kilkenny","Wexford","Sligo","Clonmel","Dundalk","Bray","Ennis","Tralee","Carlow","Naas","Athlone","Letterkenny","Tullamore","Killarney","Arklow","Cobh","Castlebar","Midleton","Mallow","Ballina","Enniscorthy","Wicklow","Cavan","Athenry","Longford","Dungarvan","Nenagh","Trim","Thurles","Youghal","Monaghan","Buncrana","Ballinasloe","Fermoy","Westport","Carrick-on-Suir","Birr","Tipperary","Carrickmacross","Kinsale","Listowel","Clonakilty","Cashel","Macroom","Castleblayney","Kilrush","Skibbereen","Bundoran","Templemore","Clones","Newbridge","Mullingar","Balbriggan","Greystones","Leixlip","Tramore","Shannon","Gorey","Tuam","Edenderry","Bandon","Loughrea","Ardee","Mountmellick","Bantry","Boyle","Ballyshannon","Cootehill","Ballybay","Belturbet","Lismore","Kilkee","Granard"]
    thread_list_HU = []
    thread_list_IE = []

    output_file_rlock_HU = RLock()
    output_file_rlock_IE = RLock()
    
    if not Path('weather_data_HU.csv').is_file():
        with open(output_filename_HU, 'w') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['local timestamp', 'server timestamp', 'city', 'temp', 'wind_speed', 'wind_dir'])

    if not Path('weather_data_IE.csv').is_file():
        with open(output_filename_IE, 'w') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['local timestamp', 'server timestamp', 'city', 'temp', 'wind_speed', 'wind_dir'])
    
    for city in city_list_HU:
        thread = WeatherGetter(city, output_filename_HU, output_file_rlock_HU, threads=5)
        thread_list_HU.append(thread)
    for thread in thread_list_HU:
        thread.start()
    for thread in thread_list_HU:
        thread.join()
        
    print()
    
    for city in city_list_IE:
        thread = WeatherGetter(city, output_filename_IE, output_file_rlock_IE, threads=5)
        thread_list_IE.append(thread)
    for thread in thread_list_IE:
        thread.start()
    for thread in thread_list_IE:
        thread.join()


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    total = end-start
    print(f'Total query time {total:.8f} seconds')
    start = time.time()
    convert_to_xlsx(output_filename_HU, output_filename_HU.replace('.csv', '.xlsx'))
    convert_to_xlsx(output_filename_IE, output_filename_IE.replace('.csv', '.xlsx'))
    end = time.time()
    total = end-start
    print(f'Total file write time {total:.8f} seconds')