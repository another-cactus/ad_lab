import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

obl_dict = {
    1: "Черкаська",
    2: "Чернігівська",
    3: "Чернівецька",
    4: "АР Крим",
    5: "Дніпропетровська",
    6: "Донецька",
    7: "Івано-Франківська",
    8: "Харківська",
    9: "Херсонська",
    10: "Хмельницька",
    11: "Київська",
    12: "м. Київ",
    13: "Кіровоградська",
    14: "Луганська",
    15: "Львівська",
    16: "Миколаївська",
    17: "Одеська",
    18: "Полтавська",
    19: "Рівненська",
    20: "м. Севастополь",
    21: "Сумська",
    22: "Тернопільська",
    23: "Закарпатська",
    24: "Вінницька",
    25: "Волинська",
    26: "Запорізька",
    27: "Житомирська"
}

df = pd.read_csv('df/combined_df.csv', index_col=False)

def filter_data(min_year, max_year, min_week, max_week, set, oblast, sort_ascending, sort_descending):
    obl =  [k for k, v in obl_dict.items() if v == oblast][0]
    selected_df = df[(df['year'] >= min_year) & (df['year'] <= max_year) &
                     (df['week'] >= min_week) & (df['week'] <= max_week) &
                     (df['oblast'] == obl)]
    selected_df = selected_df[['year','week',set]]

    the_rest_df = df[(df['year'] >= min_year) & (df['year'] <= max_year) &
                     (df['week'] >= min_week) & (df['week'] <= max_week) &
                     (df['oblast'] != obl)]

    the_rest_df = the_rest_df[['year','week',set]]
    ang_df = the_rest_df.groupby(['year','week'], as_index=False)[set].mean()

    fig1, ax1 = plt.subplots(figsize=(10, 4))
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    sns.lineplot(data=selected_df, x="year", y=set, ax=ax1, label='Обрана область')
    sns.lineplot(data=selected_df, x="year", y=set, ax=ax2, label='Обрана область')
    sns.lineplot(data=ang_df, x="year", y=set, ax=ax2, label='Решта')

    if sort_ascending and not sort_descending:
        table = selected_df.sort_values(by=[set])
    elif not sort_ascending and sort_descending:
        table = selected_df.sort_values(by=[set], ascending=False)
    else:
        table = selected_df
    return table, fig1, fig2