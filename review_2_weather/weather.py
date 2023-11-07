import time
from threading import RLock
from WeatherGetter import WeatherGetter
import pandas as pd
import csv

def convert_to_xlsx():
    infile = 'weather_data.csv'
    outfile = 'weather_data.xlsx'
    df = pd.read_csv(infile, sep=';', on_bad_lines='warn', engine='python')
    df.to_excel(outfile, sheet_name="Data", index=False)

def main():
    
    city_list = ('Sopron', 'Pécs', 'Budapest', 'Kecskemét', 'Debrecen')
    #city_list = ["Dublin","Cork","Limerick","Galway","Waterford","Drogheda","Kilkenny","Wexford","Sligo","Clonmel","Dundalk","Bray","Ennis","Tralee","Carlow","Naas","Athlone","Letterkenny","Tullamore","Killarney","Arklow","Cobh","Castlebar","Midleton","Mallow","Ballina","Enniscorthy","Wicklow","Cavan","Athenry","Longford","Dungarvan","Nenagh","Trim","Thurles","Youghal","Monaghan","Buncrana","Ballinasloe","Fermoy","Westport","Carrick-on-Suir","Birr","Tipperary","Carrickmacross","Kinsale","Listowel","Clonakilty","Cashel","Macroom","Castleblayney","Kilrush","Skibbereen","Bundoran","Templemore","Clones","Newbridge","Mullingar","Balbriggan","Greystones","Leixlip","Tramore","Shannon","Gorey","Tuam","Edenderry","Bandon","Loughrea","Ardee","Mountmellick","Bantry","Boyle","Ballyshannon","Cootehill","Ballybay","Belturbet","Lismore","Kilkee","Granard"]
    thread_list = []
    
    output_file_rlock = RLock()
    with open('weather_data.csv', 'a') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['timestamp', 'city', 'temp', 'wind_speed', 'wind_dir'])
    
    
    for city in city_list:
        thread = WeatherGetter(city, output_file_rlock, threads=1)
        thread_list.append(thread)
    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    total = end-start
    print(f'Total time {total:.8f} seconds')
    convert_to_xlsx()