import matplotlib
matplotlib.use('Agg')

from flask import Flask, request, render_template
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from io import BytesIO
import pandas as pd
import requests
import datetime
import base64
import os

data_folder = "./data/"
mask = "https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={}&year1=1981&year2=2020&type=Mean"

update_data = True
if not os.path.exists(data_folder):
    os.makedirs(data_folder)
    print("data folder created")
else:
    files = [os.path.join(data_folder, file) \
        for file in os.listdir(data_folder)]
    if len(files) != 0:
        update_data = False
        if input('Do you want to update data? (y/N): ').strip().lower() == 'y':
            for file in files:
                os.remove(file)
            update_data = True

if update_data:
    files = []
    for n in range(1, 28):
        url = mask.format(n)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        timestamp = datetime.datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
        filename = 'vhi_id_{}_{}.csv'.format(str(n).zfill(3), timestamp)
        path = os.path.join(data_folder, filename)
        with open(path, 'w') as file:
            file.write(soup.find("pre").text)
        files.append(path)
        print("{} downloaded".format(filename))

def create_frame(data_folder):
    if os.path.exists(data_folder) and files:
        data = []
        for path in files:
            df = pd.read_csv(path, index_col=False, header=0, skip_blank_lines=True, names=['year', 'week', 'NDVI', 'BT', 'VCI', 'TCI', 'VHI'])
            data.append(df)
        print('dataframe with {} frames created'.format(len(data)))
        return data
    print('folder does not exist')
    return -1

def change_name(name):
    provinces = ['Черкаська', 'Чернігівська', 'Чернівецька', 'Республіка Крим', 'Дніпропетровська', 'Донецька', 'Івано-Франківська', 'Харківська', 'Херсонська', 'Хмельницька', 'Київська', 'місто Київ', 'Кіровоградська', 'Луганська', 'Львівська', 'Миколаївська', 'Одеська', 'Полтавська', 'Рівенська', 'Севастопольська', 'Сумська', 'Тернопільська', 'Закарпатська', 'Вінницька', 'Волинська', 'Запорізька', 'Житомирська']
    if name in provinces:
        return provinces.index(name) + 1
    return provinces[name - 1]

def check_weeks_text(weeks_text):
    chars = '0123456789,- '
    for char in weeks_text:
        if char not in chars:
            return False
    return True


data = create_frame(data_folder)

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        form = request.form
        col = form['cols']
        province = form['provinces']
        weeks_text = form['weeks']
        
        weeks = []
        if weeks_text and check_weeks_text(weeks_text):
            for week_text in weeks_text.strip().split(','):
                if '-' in week_text:
                    start, end = map(int, week_text.split('-'))
                    for week in range(start, end + 1):
                        weeks.append(week)
                else:
                    weeks.append(int(week_text))
        
            df = data[change_name(province) - 1]
            selection = df[(df['week'].isin(weeks)) & (df[col] != -1.0)][['year', 'week', col]]
            sels = []
            for week in weeks:
                sels.append(df[(df['week'] == week) & (df[col] != -1.0)][['year', col]])
            
            fig = plt.figure()
            years = range(1981, 2021)
            for i, sel in enumerate(sels):
                plt.plot(sel['year'], sel[col], marker="o", label=weeks[i])
            plt.xticks(years, rotation=70)
            plt.ylabel(col, fontsize=14)
            fig.set_size_inches(9, 5.5, forward=True)
            io_file = BytesIO()
            fig.savefig(io_file, format='png', dpi=100)
            base64_string = base64.b64encode(io_file.getvalue()).decode()
            
            return render_template("main_plot.html", 
                                    col=col, 
                                    province=province, 
                                    weeks_text=weeks_text, 
                                    tables=[selection.to_html(classes='data', header="true", index=False)],
                                    data=base64_string)
    return render_template("main.html")

if __name__ == '__main__':
    app.run()
