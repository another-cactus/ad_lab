import streamlit as st
import numpy as np
from utils import *


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
DEFAULTS = {
    'min_week': 1,
    'max_week': 52,
    'min_year': 1982,
    'max_year': 2024,
    'slider_week': (1,52),
    'slider_year': (1982, 2024),
    'sort_ascending': True,
    'sort_descending': False,
    'set': 'vci',
    'oblast': 'Черкаська'
}

for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

def upd_slider(field):
    st.session_state[f'slider_{field}'] = (st.session_state[f'min_{field}'], st.session_state[f'max_{field}'])

def upd_nums(field):
    st.session_state[f'min_{field}'] = st.session_state[f'slider_{field}'][0]
    st.session_state[f'max_{field}'] = st.session_state[f'slider_{field}'][1]

def check_boxes(field):
    a = ['sort_ascending', 'sort_descending']
    a.remove(field)
    the_other=a[0]

    if st.session_state[field]:
        st.session_state[the_other] = False



st.markdown(
    """
    <style>
        .block-container {
            max-width: 80%;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

col1, _, col2 = st.columns([10, 1, 5])  # 3:1 співвідношення

with col1:
    col1_1, col1_2, col1_3 = col1.columns(3)

    tab1, tab2, tab3 = st.tabs(["📅 Таблиця", "📊 Графік", "⚖️ Порівняння"])


    min_year = st.session_state['min_year']
    max_year = st.session_state['max_year']
    min_week = st.session_state['min_week']
    max_week = st.session_state['max_week']
    set = st.session_state['set']
    oblast = st.session_state['oblast']
    sort_ascending = st.session_state['sort_ascending']
    sort_descending = st.session_state['sort_descending']

    table, fig1, fig2 = filter_data(min_year, max_year, min_week, max_week, set, oblast, sort_ascending, sort_descending)

    with tab1:
        st.write(table)

    with tab2:
        st.pyplot(fig1)

    with tab3:
        st.pyplot(fig2)

with col2:

    #ДВА ВИПАДНИХ СПИСКИ
    col2_1, col2_2 = col2.columns([2, 3])
    col2_1.selectbox(
        'Оберіть індекс',
        ('vci', 'tci', 'vhi'),
        key='set')

    col2_2.selectbox(
        'Оберіть область',
        obl_dict.values(),
        key='oblast')



    # -----------------------------------------------------------------------------
    # -----------------------------------------------------------------------------
    #СДАЙДЕР ТИЖНІ
    st.markdown("<hr>" '<b>Оберіть тижні</b>', unsafe_allow_html=True)

    col2_1, col2_2 = col2.columns(2)
    with col2_1:
        st.number_input("Від", key='min_week', min_value=1, max_value=52, step=1,
                        on_change=upd_slider, args=('week',))
    with col2_2:
        st.number_input("До", key='max_week', min_value=1, max_value=52, step=1,
                        on_change=upd_slider, args=('week',))

    slider_week = st.slider(
        " ",
        min_value=1, max_value=52,
        key='slider_week',
        on_change=upd_nums, args=('week',))


    #-----------------------------------------------------------------------------
    #-----------------------------------------------------------------------------
    #СЛАЙДЕР РОКІВ
    st.markdown("<hr>" '<b>Оберіть роки</b>', unsafe_allow_html=True)

    col2_1, col2_2 = col2.columns(2)
    with col2_1:
        st.number_input("Від", key='min_year', min_value=1982, max_value=2024, step=1,
                                                    on_change=upd_slider, args=('year',))
    with col2_2:
        st.number_input("До", key='max_year',min_value=1982, max_value=2024, step=1,
                                                    on_change=upd_slider, args=('year',))


    slider_year = st.slider(
        " ",
        min_value=1982, max_value=2024,
        key='slider_year',
        on_change = upd_nums, args = ('year',)
    )

    # -----------------------------------------------------------------------------
    # -----------------------------------------------------------------------------
    # РЕЖИМ СОРТУВАННЯ
    st.markdown("<hr>" '<b>Оберіть як сортувати</b>', unsafe_allow_html=True)

    st.checkbox('За зростанням', key='sort_ascending', on_change=check_boxes, args=('sort_ascending',))
    st.checkbox('За спаданням', key='sort_descending', on_change=check_boxes, args=('sort_descending',))




    #-----------------------------------------------------------------------------
    #-----------------------------------------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)

    def reset_filters():
        for key in DEFAULTS:
            st.session_state.pop(key, None)


    st.button("Скинути фільтри", on_click=reset_filters)

