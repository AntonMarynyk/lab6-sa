# import different modules
from faulthandler import disable
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import numpy as np

from build import MapBuild

from cogn import Map

# Базові налаштування вебсторінки
st.set_page_config(
    page_title='Task 6',
    layout='wide')

st.title('LAB-6')

# визначення 2 колонок- для введення та виведення
col1, col2 = st.columns(spec=[2, 1])

# прочитання даних 
try:
    adj_file = col1.file_uploader('', type=['csv'], key='input_file')
    input_df = pd.read_csv(adj_file, delimiter=',', decimal='.', index_col=0)
except:
    input_df = pd.read_csv('input.csv', delimiter=',', decimal='.', index_col=0)
    
names = list(input_df['name'])
input_df = input_df.reset_index().drop(columns=['name'])
print(input_df)
# параметри за замовчуванням для побудови графіків - візуалізації
builder = GridOptionsBuilder.from_dataframe(input_df)
builder.configure_default_column(
    resizable=True, filterable=False, editable=True,
    sorteable=False, groupable=False
)
builder.configure_column('index', header_name='FACTOR', editable=False)
builder.configure_grid_options(
    autoSizePadding=1
)
options = builder.build()

custom_css= {
    'font-size': '30px !important'
}

# для першої колонки
with col1:
    reload = False     
    
    if col1.button('Reset matrix', key='reset_edit'):
        reload = True

    grid_return = AgGrid(
        input_df, options,
        reload_data=reload, 
        update_mode=GridUpdateMode.VALUE_CHANGED,
        columns_auto_size_mode=1,
        custom_css=custom_css
    )
    
    reload = False

    df = grid_return['data']
    df_to_save = df.copy()
    df_to_save['name'] = names
    df_to_save.to_csv('names.csv', index=False)
    M = df.values[:, 1:].astype(float)
    build_map = MapBuild()
    fig = build_map.make_graph_fig(M, names)
    # col1.plotly_chart(fig)
    cogn_map = Map(M, df.columns.to_list()[1:])

with col2:
    R = cogn_map.getRadius()

    col2.header('RESULTS OF MODELING:')
    col2.write(f'Spectral radius $R$: **{R:.5f}**.')

    even_cycles = cogn_map.getCycles(only_even = True)
    even_cycles.sort(key=len, reverse=True)
    even_number = len(even_cycles)

    col2.write(f'Number of even cycles: **{even_number}**.')
    col2.write(f'Numerical stability ($R < 1$): **' + ('$+$' if cogn_map.isStable2() else ' -') + '**.')
    col2.write(f'Disruption stability ($R \leq 1$): **' + ('$+$' if cogn_map.isStable() else ' - ') + '**.')

    col2.write('List of even cycles:')
    col2.text_area(
        '',
        value='\n'.join(
            [' > '.join([str(i+1) for i in cycle] + [str(cycle[0]+1)]) for cycle in even_cycles]
        ), height=200
    )

graph_column = st.columns(3)

M = df.values[:, 1:].astype(float)
build_map = MapBuild()
fig = build_map.make_graph_fig(M, names)

cogn_map = Map(M, df.columns.to_list()[1:])

graph_column[1].plotly_chart(fig)


# st.header('RESULTS OF MODELING:')


# sub_cols = st.columns(3)

# R = cogn_map.getRadius()

# sub_cols[0].write(f'Spectral radius $R$: **{R:.5f}**.')

# even_cycles = cogn_map.getCycles(only_even = True)
# even_cycles.sort(key=len, reverse=True)
# even_number = len(even_cycles)

# sub_cols[1].write(f'Number of even cycles: **{even_number}**.')
# sub_cols[1].write(f'Numerical stability ($R < 1$): **' + ('$+$' if cogn_map.isStable2() else ' -') + '**.')
# sub_cols[1].write(f'Disruption stability ($R \leq 1$): **' + ('$+$' if cogn_map.isStable() else ' - ') + '**.')

# sub_cols[2].write('List of even cycles:')
# sub_cols[2].text_area(
#     '',
#     value='\n'.join(
#         [' > '.join([str(i+1) for i in cycle] + [str(cycle[0]+1)]) for cycle in even_cycles]
#     ), height=200
# )

st.header('Modeling')

impulse_cols = st.columns([1, 4])

q = []
for i in range(M.shape[0]):
    q.append(
        impulse_cols[0].number_input(f'q_{i+1}', 
        min_value=-5.0, max_value=5.0, value=0.0,
        step=1.0, key=f'q_{i}')
    )

iter_count = impulse_cols[1].number_input(
    'Step number', min_value=1, max_value=20,
    value=5, step=1, key='iter_count'
)

if impulse_cols[1].button('Run', key='run_impulse'):
    res = cogn_map.impulse(impulse=q, steps=iter_count)
    impulse_plot_fig = build_map.make_impulse_fig(res, cogn_map.node_names)
    impulse_cols[1].plotly_chart(impulse_plot_fig)
