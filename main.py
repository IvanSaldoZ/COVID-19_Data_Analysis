# Анализ динамики заражений COVID-19 в России на дату 01.05.2020
# Источник данных: Yandex.DataLens: https://datalens.yandex.ru/dashboards/rbfgkhi6y1aan?tab=5B
# Текущая визуализация данных: https://yandex.ru/covid19/stat?utm_source=main_title
# Хороший туториал по Pandas: https://pythonru.com/uroki/osnovy-pandas-3-vazhnye-metody-formatirovanija-dannyh
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Анализ показателя смертноси к выздоровевшим для России
def russia_analyze():
    df1 = pd.read_csv('data/table_russia_2020-05-01_12-50.csv', delimiter=';')
    # Необходимо для правильной сортировки по дате
    df1['Дата'] = pd.to_datetime(df1['Дата'], dayfirst=True)

    # Какие колонки отображаем
    columns = ['Смертей за день','Заражений за день','Выздоровлений за день']
    # Формируем датафрейм, сгруппированный по датам (по всем регионам получается), суммируем все значения в колонках,
    # которые разняться, и затем сортируем полученные данные по сгруппированной колонке
    dfAllRussia = df1.groupby(['Дата']).sum()[columns].sort_values(by=['Дата'])
    dfRes = dfAllRussia['Смертей за день']/dfAllRussia['Выздоровлений за день']
    dfRes.fillna(0, inplace=True)
    dfRes = round(dfRes*100, 1)

    # Выводим результат
    print(dfAllRussia)
    print(dfRes)

    plt.plot(dfRes)
    plt.show()


# Анализ показателя смертноси к выздоровевшим для определенной страны
def country_analyze(country_name='Россия', mean_window=3, show_plot=False):
    df1 = pd.read_csv('data/table_world_2020-05-01_14-12.csv', delimiter=';')
    # Необходимо для правильной сортировки по дате
    df1['Дата'] = pd.to_datetime(df1['Дата'], dayfirst=True)

    # оставляем только определенную страну
    df1 = df1[df1.Страна == country_name]
    # Какие колонки отображаем
    columns = ['Смертей за день','Заражений за день','Выздоровлений за день']
    # Формируем датафрейм, сгруппированный по датам (по всем регионам получается),
    # суммируем все значения в колонках выше,
    # и затем сортируем полученные данные по сгруппированной колонке
    df_stat = df1.groupby(['Дата']).sum()[columns].sort_values(by=['Дата'])
    df_res = df_stat['Смертей за день']/df_stat['Выздоровлений за день']
    df_res.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_res.fillna(0, inplace=True)
    print(df_res.tail(15))
    #print(round(df_res.tail()*100,1))
    # Сглаживание: считаем средние значения по последним трем дням (window)
    window = mean_window
    df_res = df_res.rolling(window).mean()
    # Считаем проценты от полученной величины и округляем
    df_res = round(df_res*100, 1)
    print(df_res.tail(15))
    df_res.fillna(0, inplace=True)

    # Выводим последние
    print(df_res.tail(5))
    df_res = round((df_res.diff()/df_res)*100,2) # Производная
    df_res = round(df_res.rolling(window).mean(),1)  # Сглаживаем производную
    df_res.fillna(0, inplace=True)
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print('!!!!!!Result (if less than zero than the level Pandemic is decreasing): ',df_res.tail(3).sum())
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    df_res = df_res

    # Выводим результат
    if show_plot:
        #print(df_stat)
        plt.title(country_name)  # заголовок
        plt.xlabel("Дата")  # ось абсцисс
        plt.ylabel('Показатель спада пандемии')  # ось ординат
        plt.grid()  # включение отображение сетки
        plt.plot(df_res)
        plt.show()

    return df_res


if __name__ == '__main__':
    #countries = ['США', 'Россия', 'Италия', 'Испания', 'Индия', 'Южная Корея']
    countries = ['США', 'Россия', 'Бразилия', 'Австралия', 'Швеция', 'Германия']
    for country in countries:
        print('--------------------')
        print(country)
        print(country_analyze(country, show_plot=True, mean_window=10))

    #russia_analyze()

