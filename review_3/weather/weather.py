import time
import pandas as pd
import csv
from threading import Semaphore, RLock
from WeatherGetter import WeatherGetter
from pathlib import Path
from memory_profiler import profile
import timeit


semaphore_thread_count = 100
output_filename_HU = 'weather_data_HU.csv'
output_filename_IE = 'weather_data_IE.csv'


def convert_to_xlsx(input_filename, output_filename):
    df = pd.read_csv(input_filename, sep=';', on_bad_lines='warn', engine='python')
    df.to_excel(output_filename, sheet_name="Data", index=False)

#@profile
def main():
    print(f'Using thread count {semaphore_thread_count}')
    start = timeit.default_timer()
    with open('config.txt', 'r') as configfile:
        _ = configfile.readlines()
    end = timeit.default_timer()
    print(f'TIMEIT File read took    {end-start:.3f} sec')
    city_list_HU = ('Sopron', 'Pécs', 'Budapest', 'Kecskemét', 'Debrecen')
    city_list_IE = ["Dublin","Cork","Limerick","Galway","Waterford","Drogheda","Kilkenny","Wexford","Sligo","Clonmel","Dundalk","Bray","Ennis","Tralee","Carlow","Naas","Athlone","Letterkenny","Tullamore","Killarney","Arklow","Cobh","Castlebar","Midleton","Mallow","Ballina","Enniscorthy","Wicklow","Cavan","Athenry","Longford","Dungarvan","Nenagh","Trim","Thurles","Youghal","Monaghan","Buncrana","Ballinasloe","Fermoy","Westport","Carrick-on-Suir","Birr","Tipperary","Carrickmacross","Kinsale","Listowel","Clonakilty","Cashel","Macroom","Castleblayney","Kilrush","Skibbereen","Bundoran","Templemore","Clones","Newbridge","Mullingar","Balbriggan","Greystones","Leixlip","Tramore","Shannon","Gorey","Tuam","Edenderry","Bandon","Loughrea","Ardee","Mountmellick","Bantry","Boyle","Ballyshannon","Cootehill","Ballybay","Belturbet","Lismore","Kilkee","Granard"]
    #city_list_IE_gen = (y for y in city_list_IE)
    thread_list_HU = []
    thread_list_IE = []
    semaphore_HU = Semaphore(semaphore_thread_count)
    semaphore_IE = Semaphore(semaphore_thread_count)
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
        thread = WeatherGetter(city, semaphore_HU, output_filename_HU, output_file_rlock_HU)
        thread_list_HU.append(thread)
    start = timeit.default_timer()
    for thread in thread_list_HU:
        thread.start()
    for thread in thread_list_HU:
        thread.join()
    end = timeit.default_timer()
    print(f'TIMEIT HU Process took   {end-start:.3f} sec')

    
    for city in city_list_IE:
        thread = WeatherGetter(city, semaphore_IE, output_filename_IE, output_file_rlock_IE)
        thread_list_IE.append(thread)
    start = timeit.default_timer()
    for thread in thread_list_IE:
        thread.start()
    for thread in thread_list_IE:
        thread.join()
    end = timeit.default_timer()
    print(f'TIMEIT IE Process took   {end-start:.3f} sec')


if __name__ == '__main__':
    TOTAL_START = timeit.default_timer()
    start = timeit.default_timer()
    main()
    end = timeit.default_timer()
    total = end-start
    print(f'Total main() time        {total:.3f} seconds')
    start = timeit.default_timer()
    convert_to_xlsx(output_filename_HU, output_filename_HU.replace('.csv', '.xlsx'))
    convert_to_xlsx(output_filename_IE, output_filename_IE.replace('.csv', '.xlsx'))
    end = timeit.default_timer()
    total = end-start
    print(f'Output file write time   {total:.3f} seconds')
    TOTAL_END = timeit.default_timer()
    TOTAL = TOTAL_END - TOTAL_START
    print()
    print(f'TOTAL time               {TOTAL:.3f} seconds')