import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import base64
import dash_table as dt
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import chart_studio.plotly


df1 = pd.read_csv("//projects/projects/QA_Dashboard/Data/profiles.csv")

df = df1[['table_name', 'column_name', 'dtype_count', 'max_length', 'col_data_type', 'non_null_values', '%_of_non_nulls',
          'null_values', '%_of_nulls',	'unique_values_count', 'count', 'cardinality_pct', 'PK_Flag']]

df2 = df[['table_name', 'column_name', 'max_length', 'col_data_type', 'non_null_values', '%_of_non_nulls',
          'null_values', '%_of_nulls',	'unique_values_count', 'count', 'cardinality_pct', 'PK_Flag']]

df_numbers = df1[['table_name', 'column_name', 'max_length', 'col_data_type', 'mean', 'std', 'min', '25%', '50%',
                  '75%', 'max']]

TargetMap = pd.read_csv("//projects/projects/QA_Dashboard/Data/mappings.csv")
tgt = pd.DataFrame(TargetMap)


def generate_table(dataframe, max_rows=100):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))],

    )


app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

test_png = '//projects/projects/QA_Dashboard/Assets/QA.png'
test_base64 = base64.b64encode(open(test_png, 'rb').read()).decode('ascii')

app.layout = html.Div([
                html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Img(src='data:image/png;base64,{}'.format(test_base64)),
                        ], className="one columns"),
                        html.Br(),
                        html.H1(children='Profiling Dashboard', style={'textAlign': 'left', 'color': '#566D7E'},
                                className="eleven columns"),

                         ], className="row"),

    dcc.Tabs(
        id="tabs-with-classes",
        value='tab-1',
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=[
            dcc.Tab(
                label='Table View',
                value='tab-1',
                className='custom-tab',
                selected_className='custom-tab--selected'
            ),
            # dcc.Tab(
            #     label='Column View',
            #     value='tab-2',
            #     className='custom-tab',
            #     selected_className='custom-tab--selected'
            # ),
            dcc.Tab(
                label='Self-Guided Profiles',
                value='tab-3', className='custom-tab',
                selected_className='custom-tab--selected'
            ),
            dcc.Tab(
                label='Source-to-Target',
                value='tab-4',
                className='custom-tab',
                selected_className='custom-tab--selected'
            ),
        ]),
    html.Div(id='tabs-content-classes')
])
                ])
                ])


@app.callback(Output('tabs-content-classes', 'children'),
              [Input('tabs-with-classes', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        dcc.Dropdown(id='dropdown', options=[
                            {'label': i, 'value': i} for i in df['table_name'].unique()
                        ], multi=False, value='advisor', style={'width': '40%'}),
                    ], className="six columns"),

                    html.Div([
                        dcc.Dropdown(
                            id='dropdown_child',
                            multi=True, value='Advisor ID', style={'width': '40%'}),
                    ], className="six columns"),

                ], className="row"),

                html.Div([
                    html.Div([
                        html.Div(id='output-container', children=[]),
                                ], className="six columns")
                      ], className="row"),
    html.Div([
        html.Div([
            dbc.Card([
                dbc.CardHeader(" "),
                dbc.CardBody(
                    [
                        html.H4(id='output-container_card0', children=[], className="card-title"
                                )
                    ]),
            ], style={"width": "30rem"}),
        ], className="two columns"),
        html.Div([
            dbc.Card([
                dbc.CardHeader("RECORDS"),
                dbc.CardBody(
                    [
                        html.H4(id='output-container_card', children=[], className="card-title"
                                )
                    ]),
            ], style={"width": "30rem"}),
        ], className="three columns"),

        html.Div([
            dbc.Card([
                dbc.CardHeader("COLUMNS"),
                dbc.CardBody(
                    [
                        html.H4(id='output-container_card2', children=[], className="card-title"
                                )
                    ]),
            ], style={"width": "30rem"}, ),
        ], className="three columns"),

    ], className="row"),

    html.Div([
        html.Div([
            dcc.Graph(id='tg3', figure={}),
        ], className="six columns"),

        html.Div([
            dcc.Graph(id='tg2'),
        ], className="six columns"),

    ], className="row"),
    html.Div([
        html.Div([
            dcc.Graph(id='tg4'),
        ], className="six columns"),

        html.Div([
            dcc.Graph(id='tg5'),
        ], className="six columns"),

    ], className="row"),

    # html.Div([
    #     html.Div([
    #         dcc.Graph(id='tg5'),
    #     ], className="six columns"),
    #
    #
    # ], className="row"),

            ])
    ])

    elif tab == 'tab-3':
        return html.Div([
            dt.DataTable(
                id='datatable-interactivity',
                columns=[
                    {"name": i, "id": i, "deletable": True, "selectable": True} for i in df2.columns
                ],
                data=df2.to_dict('records'),
                editable=True,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                column_selectable="single",
                row_selectable="multi",
                row_deletable=True,
                selected_columns=[],
                selected_rows=[],
                page_action="native",
                page_current=0,
                page_size=15,
                fixed_rows={'headers': True},
                style_table={'height': 400},
                style_cell={'minWidth': 95, 'maxWidth': 95, 'width': 95},
                style_data_conditional=[{
                    'if': {
                        'column_id': 'PK_Flag',
                        'filter_query': '{PK_Flag} = 1'
                    },
                    'backgroundColor': 'lightgreen'
                }, {
                    'if': {
                        'column_id': 'column_name',
                        'filter_query': '{count} = {unique_values_count}'
                    },
                    'backgroundColor': 'lightgreen'
                }, {
                    'if': {
                        'column_id': 'cardinality_pct',
                        'filter_query': '{cardinality_pct} >= 90 && {cardinality_pct} < 100'
                    },
                    'backgroundColor': 'lightyellow'
                }, {
                    'if': {
                        'column_id': 'cardinality_pct',
                        'filter_query': '{cardinality_pct} < 90'
                    },
                    'backgroundColor': 'pink'
                }, {
                    'if': {
                        'column_id': 'cardinality_pct',
                        'filter_query': '{cardinality_pct} = 100'
                    },
                    'backgroundColor': 'lightgreen'
                }]
            ),
            html.Br(),

            html.Div(id='datatable-interactivity-container')
        ])
    elif tab == 'tab-4':
        return html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='dropdown_tab4', options=[
                        {'label': i, 'value': i} for i in tgt['TABLE'].unique()
                    ], multi=True, style={'width': '40%'}),
                ], className="six columns"),

                html.Div([
                    dcc.Dropdown(id='dropdown2_tab4', options=[
                        {'label': i, 'value': i} for i in tgt['COLUMN.1'].unique()
                    ], multi=True, style={'width': '40%'}),
                ], className="six columns")
            ], className="row"),

            html.Br(),

            html.Div([
                html.Div([
                    html.Div(id='map_table'),
                ], className="twelve columns"),
            ], className="row")


        ])


@app.callback(
    [dash.dependencies.Output(component_id='output-container', component_property='children'),
     dash.dependencies.Output(component_id='output-container_card', component_property='children'),
     dash.dependencies.Output(component_id='output-container_card2', component_property='children')],
    [dash.dependencies.Input(component_id='dropdown', component_property='value')]
             )
def update_fig(dropdown_value):

    container = "The table selected by user is: {}".format(dropdown_value)

    dff2 = df[df['table_name'] == dropdown_value]

    container2 = "{:,.0f}".format(dff2['count'].sum()/dff2['count'].count())

    container3 = "{:,.0f}".format(dff2['column_name'].count())

    fig_sc = go.Figure(go.Bar(
        x=dff2['col_data_type'],
        y=dff2['dtype_count'],
        # orientation='h',
        text=dff2['dtype_count'],
        textposition='auto',
        marker_color='#6ab187',
        texttemplate='%{text:.4s}',
        textfont=dict(
            family="sans serif",
            size=15,
            color="#1f3f49"
        )
    ))

    fig_sc.update_layout(
        title={
            'text': "Data Types",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    fig = go.Figure(go.Bar(
        x=dff2['column_name'],
        y=dff2['non_null_values'],
        # orientation='h',
        text=dff2['non_null_values'],
        textposition='auto',
        marker_color='#31708e',
        texttemplate='%{text:.4s}',
        textfont=dict(
            family="sans serif",
            size=19,
            color="#e98074"
        )
    ))

    fig.update_layout(
        title={
            'text': "Non-Null Value Counts",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    fig3 = go.Figure(data=[
        go.Bar(name='Total Records', x=dff2['column_name'], y=dff2['count'], text=dff2['non_null_values'],
               textposition='auto', marker_color='#37536d', texttemplate='%{text:.4s}'),
        go.Bar(name='Unique Record Count', x=dff2['column_name'], y=dff2['unique_values_count'],
               text=dff2['unique_values_count'], textposition='auto', marker_color='#31708e',
               texttemplate='%{text:.4s}')

    ])

    fig3.update_layout(barmode='group',
                       title={
                            'text': "Unique vs. Null Counts",
                            'y': 0.9,
                            'x': 0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'})

    fig2 = go.Figure(data=[
        go.Bar(name='Non-Null %', x=dff2['column_name'], y=dff2['%_of_non_nulls'], text=dff2['%_of_non_nulls'],
               textposition='auto', marker_color='#7e909a', texttemplate='%{text:.4s}'),
        go.Bar(name='Unique Record Count', x=dff2['column_name'], y=dff2['%_of_nulls'],
               text=dff2['%_of_nulls'], textposition='auto', marker_color='#31708e',
               texttemplate='%{text:.4s}')

    ])

    fig2.update_layout(barmode='group',
                       title={
                            'text': "Non-Null vs Nulls %",
                            'y': 0.9,
                            'x': 0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'})

    fig5 = go.Figure(data=[
        go.Bar(name='Non-Null %', x=dff2['column_name'], y=dff2['PK_Flag'], text=dff2['PK_Flag'],
               textposition='auto', marker_color='#dbae58', texttemplate='%{text:.0s}')


    ])

    fig5.update_layout(title={
                            'text': "PK Candidate based on Cardinality %",
                            'y': 0.9,
                            'x': 0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'})

    return container, container2, container3


@app.callback(
    dash.dependencies.Output('d_table', 'children'),
    [dash.dependencies.Input('dropdown_tab2', 'value')])
def display_table(dropdown_value_column):

    if dropdown_value_column is None:
        return generate_table(df)
    if dropdown_value_column is not None:
        dff2 = df[df['column_name'] == dropdown_value_column]
        return generate_table(dff2)


@app.callback(
    dash.dependencies.Output('datatable-interactivity-container', "children"),
    [dash.dependencies.Input('datatable-interactivity', "derived_virtual_data"),
     dash.dependencies.Input('datatable-interactivity', "derived_virtual_selected_rows")])
def update_graphs(rows, derived_virtual_selected_rows):

    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff2 = df2 if rows is None else pd.DataFrame(rows)

    colors = ['#6ab187' if i in derived_virtual_selected_rows else '#31708e'
              for i in range(len(dff2))]

    return [

        dcc.Graph(
            id=column,
            figure={
                "data": [
                    {
                        "x": dff2['table_name'],
                        "x": dff2['column_name'],
                        "y": dff2[column],
                        "text": dff2[column],
                        "type": "bar",
                        "marker": {"color": colors},
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True},
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": column}
                    },
                    "height": 400,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            },

        )

        for column in ['non_null_value_count', 'unique_values_count', 'count', 'cardinality_pct', 'null_values',
                       'non_null_values', '%_of_nulls']
        if column in dff2
    ]


@app.callback(
    dash.dependencies.Output('map_table', 'children'),
    [dash.dependencies.Input('dropdown_tab4', 'value'),
     dash.dependencies.Input('dropdown2_tab4', 'value')])
def display_table(dropdown_value_table, dropdown_value_column):

    if dropdown_value_table is None and dropdown_value_column is None:
        return dt.DataTable(
            id='d_table_map',
            columns=[
                {"name": i, "id": i, "deletable": True, "selectable": True} for i in tgt.columns
            ],
            data=tgt.to_dict('records'),
            editable=True,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable="single",
            row_selectable="multi",
            row_deletable=True,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=25,
            fixed_rows={'headers': True},
            style_table={'height': 800},
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                'lineHeight': '15px'
            },
            style_cell={
                'height': 'auto',
                # all three widths are needed
                'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                'whiteSpace': 'normal'
            },
            style_data_conditional=[{
                'if': {
                    'column_id': 'TABLE',
                    'filter_query': '{TABLE} != NULL'
                }, 'backgroundColor': 'lightgray'},
                {
                    'if': {
                        'column_id': 'COLUMN.1'
                        # 'filter_query': '{COLUMN.1} != NULL'
                    },
                    'backgroundColor': 'lightgreen'
                }

            ]

        )
    if dropdown_value_table is not None and dropdown_value_column is None:
        dff2 = tgt[tgt['TABLE'].str.contains('|'.join(dropdown_value_table))]
        return dt.DataTable(
            id='d_table_map',
            columns=[
                {"name": i, "id": i, "deletable": True, "selectable": True} for i in dff2.columns
            ],
            data=dff2.to_dict('records'),
            editable=True,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable="single",
            row_selectable="multi",
            row_deletable=True,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=25,
            fixed_rows={'headers': True},
            style_table={'height': 800},
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                'lineHeight': '15px'
            },
            style_cell={
                'height': 'auto',
                # all three widths are needed
                'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                'whiteSpace': 'normal'
            },
            style_data_conditional=[{
                'if': {
                    'column_id': 'TABLE',
                    'filter_query': '{TABLE} != NULL'
                }, 'backgroundColor': 'lightgray'}
            ]

                            )
    if dropdown_value_table is None and dropdown_value_column is not None:
        dff2 = tgt[tgt['COLUMN.1'].str.contains('|'.join(dropdown_value_column))]
        return dt.DataTable(
            id='d_table_map',
            columns=[
                {"name": i, "id": i, "deletable": True, "selectable": True} for i in dff2.columns
            ],
            data=dff2.to_dict('records'),
            editable=True,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable="single",
            row_selectable="multi",
            row_deletable=True,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=25,
            fixed_rows={'headers': True},
            style_table={'height': 800},
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                'lineHeight': '15px'
            },
            style_cell={
                'height': 'auto',
                # all three widths are needed
                'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                'whiteSpace': 'normal'
            },
            style_data_conditional=[{
                'if': {
                    'column_id': 'TABLE',
                    'filter_query': '{TABLE} != NULL'
                }, 'backgroundColor': 'lightgray'}
            ]

        )
    if dropdown_value_table is not None and dropdown_value_column is not None:
        dff = tgt[tgt['TABLE'].str.contains('|'.join(dropdown_value_table))]
        dff = dff[dff['COLUMN.1'].str.contains('|'.join(dropdown_value_column))]
        return dt.DataTable(
            id='d_table_map',
            columns=[
                {"name": i, "id": i, "deletable": True, "selectable": True} for i in dff.columns
            ],
            data=dff.to_dict('records'),
            editable=True,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable="single",
            row_selectable="multi",
            row_deletable=True,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=25,
            fixed_rows={'headers': True},
            style_table={'height': 800},
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                'lineHeight': '15px'
            },
            style_cell={
                'height': 'auto',
                # all three widths are needed
                'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                'whiteSpace': 'normal'
            },
            style_data_conditional=[{
                'if': {
                    'column_id': 'TABLE',
                    'filter_query': '{TABLE} != NULL'
                }, 'backgroundColor': 'lightgray'}
            ]

        )


@app.callback(
    dash.dependencies.Output('tab2_table', 'children'),
    [dash.dependencies.Input('dropdown_tab2', 'value'),
     dash.dependencies.Input('dropdown2_tab2', 'value')])
def display_table(dropdown_value_table, dropdown_value_column):

    if dropdown_value_table is None and dropdown_value_column is None:
        return dt.DataTable(
            id='d_table_tab2',
            columns=[
                {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
            ],
            data=df.to_dict('records'),
            editable=True,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable="single",
            row_selectable="multi",
            row_deletable=True,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=25,
            fixed_rows={'headers': True},
            style_table={'height': 800},
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                'lineHeight': '15px'
            },
            style_cell={
                'height': 'auto',
                # all three widths are needed
                'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                'whiteSpace': 'normal'
            },
            style_data_conditional=[{
                'if': {
                    'column_id': 'table_name',
                    'filter_query': '{table_name} != NULL'
                }, 'backgroundColor': 'lightgray'}
            ]

        )
    if dropdown_value_table is not None and dropdown_value_column is None:
        dff2 = df[df['table_name'].str.contains('|'.join(dropdown_value_table))]
        return dt.DataTable(
            id='d_table_tab2',
            columns=[
                {"name": i, "id": i, "deletable": True, "selectable": True} for i in dff2.columns
            ],
            data=dff2.to_dict('records'),
            editable=True,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable="single",
            row_selectable="multi",
            row_deletable=True,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=25,
            fixed_rows={'headers': True},
            style_table={'height': 800},
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                'lineHeight': '15px'
            },
            style_cell={
                'height': 'auto',
                # all three widths are needed
                'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                'whiteSpace': 'normal'
            },
            style_data_conditional=[{
                'if': {
                    'column_id': 'table_name',
                    'filter_query': '{table_name} != NULL'
                }, 'backgroundColor': 'lightgray'}
            ]

                            )
    if dropdown_value_table is None and dropdown_value_column is not None:
        dff2 = df[df['column_name'].str.contains('|'.join(dropdown_value_column))]
        return dt.DataTable(
            id='d_table_tab2',
            columns=[
                {"name": i, "id": i, "deletable": True, "selectable": True} for i in dff2.columns
            ],
            data=dff2.to_dict('records'),
            editable=True,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable="single",
            row_selectable="multi",
            row_deletable=True,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=25,
            fixed_rows={'headers': True},
            style_table={'height': 800},
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                'lineHeight': '15px'
            },
            style_cell={
                'height': 'auto',
                # all three widths are needed
                'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                'whiteSpace': 'normal'
            },
            style_data_conditional=[{
                'if': {
                    'column_id': 'table_name',
                    'filter_query': '{table_name} != NULL'
                }, 'backgroundColor': 'lightgray'}
            ]

        )
    if dropdown_value_table is not None and dropdown_value_column is not None:
        dff = df[df['table_name'].str.contains('|'.join(dropdown_value_table))]
        dff2 = dff[dff['column_name'].str.contains('|'.join(dropdown_value_column))]
        return dt.DataTable(
            id='d_table_tab2',
            columns=[
                {"name": i, "id": i, "deletable": True, "selectable": True} for i in dff2.columns
            ],
            data=dff2.to_dict('records'),
            editable=True,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable="single",
            row_selectable="multi",
            row_deletable=True,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=25,
            fixed_rows={'headers': True},
            style_table={'height': 800},
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                'lineHeight': '15px'
            },
            style_cell={
                'height': 'auto',
                # all three widths are needed
                'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                'whiteSpace': 'normal'
            },
            style_data_conditional=[{
                'if': {
                    'column_id': 'table_name',
                    'filter_query': '{table_name} != NULL'
                }, 'backgroundColor': 'lightgray'}
            ]

        )


@app.callback(Output('dropdown_child', 'options'),
              [Input('dropdown', 'value')])
def get_dropdown_child(table_value):
    dff = df[df['table_name'] == table_value]['column_name']
    return [{'label': i, 'value': i} for i in dff]


@app.callback(dash.dependencies.Output(component_id='tg3', component_property='figure'),
              [dash.dependencies.Input(component_id='dropdown', component_property='value'),
               dash.dependencies.Input(component_id='dropdown_child', component_property='value')])
def update_fig3(dropdown_value, dropdown_value2):

    if dropdown_value is not None and dropdown_value2 is None:
        dff3 = df[df['table_name'] == dropdown_value]

        fig4 = go.Figure(go.Bar(
            x=dff3['column_name'],
            y=dff3['non_null_values'],
            # orientation='h',
            text=dff3['non_null_values'],
            textposition='auto',
            marker_color='#065464',
            texttemplate='%{text:.4s}',
            textfont=dict(
                family="sans serif",
                size=19,
                color="#e98074"
            )
        ))

        fig4.update_layout(
            title={
                'text': "Non-Null Record Counts",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'})

        return fig4

    if dropdown_value is not None and dropdown_value2 is not None:
        dff1 = df[df['table_name'] == dropdown_value]
        dff2 = dff1[dff1['column_name'].str.contains('|'.join(dropdown_value2))]
        dff3 = dff1.merge(dff2)

        fig4_2 = go.Figure(go.Bar(
            x=dff3['column_name'],
            y=dff3['non_null_values'],
            # orientation='h',
            text=dff3['non_null_values'],
            textposition='auto',
            marker_color='#065464',
            texttemplate='%{text:.4s}',
            textfont=dict(
                family="sans serif",
                size=19,
                color="#e98074"
            )
        ))

        fig4_2.update_layout(
            title={
                'text': "Non-Null Record Counts",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'})

        return fig4_2

    if dropdown_value is None and dropdown_value2 is not None:
        dropdown_value_tmp = 'advisor'
        dff1 = df[df['table_name'] == dropdown_value_tmp]
        dff2 = dff1[dff1['column_name'].str.contains('|'.join(dropdown_value2))]
        dff3 = dff1.merge(dff2)

        fig4_3 = go.Figure(go.Bar(
            x=dff3['column_name'],
            y=dff3['non_null_values'],
            # orientation='h',
            text=dff3['non_null_values'],
            textposition='auto',
            marker_color='#065464',
            texttemplate='%{text:.4s}',
            textfont=dict(
                family="sans serif",
                size=19,
                color="#e98074"
            )
        ))

        fig4_3.update_layout(
            title={
                'text': "Non-Null Record Counts",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'})

        return fig4_3

    if dropdown_value is None and dropdown_value2 is None:
        dropdown_value_tmp = 'advisor'
        dff1 = df[df['table_name'] == dropdown_value_tmp]
        dff2 = dff1[dff1['column_name'].str.contains('|'.join(dropdown_value2))]
        dff3 = dff1.merge(dff2)

        fig4_4 = go.Figure(go.Bar(
            x=dff3['column_name'],
            y=dff3['non_null_values'],
            # orientation='h',
            text=dff3['non_null_values'],
            textposition='auto',
            marker_color='#065464',
            texttemplate='%{text:.4s}',
            textfont=dict(
                family="sans serif",
                size=19,
                color="#e98074"
            )
        ))

        fig4_4.update_layout(
            title={
                'text': "Non-Null Record Counts",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'})

        return fig4_4


@app.callback(dash.dependencies.Output(component_id='tg2', component_property='figure'),
              [dash.dependencies.Input(component_id='dropdown', component_property='value'),
               dash.dependencies.Input(component_id='dropdown_child', component_property='value')])
def update_fig3(dropdown_value, dropdown_value2):

    if dropdown_value is not None and dropdown_value2 is None:
        dff3 = df[df['table_name'] == dropdown_value]

        fig4 = go.Figure(go.Bar(
            x=dff3['column_name'],
            y=dff3['unique_values_count'],
            # orientation='h',
            text=dff3['unique_values_count'],
            textposition='auto',
            marker_color='#46648c',
            texttemplate='%{text:.4s}',
            textfont=dict(
                family="sans serif",
                size=19,
                color="#e98074"
            )
        ))

        fig4.update_layout(
            title={
                'text': "Unique Values",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'})

        return fig4

    if dropdown_value is not None and dropdown_value2 is not None:
        dff1 = df[df['table_name'] == dropdown_value]
        dff2 = dff1[dff1['column_name'].str.contains('|'.join(dropdown_value2))]
        dff3 = dff1.merge(dff2)

        fig4_2 = go.Figure(go.Bar(
            x=dff3['column_name'],
            y=dff3['unique_values_count'],
            # orientation='h',
            text=dff3['unique_values_count'],
            textposition='auto',
            marker_color='#46648c',
            texttemplate='%{text:.4s}',
            textfont=dict(
                family="sans serif",
                size=19,
                color="#e98074"
            )
        ))

        fig4_2.update_layout(
            title={
                'text': "Unique Values",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'})

        return fig4_2

    if dropdown_value is None and dropdown_value2 is not None:
        dropdown_value_tmp = 'advisor'
        dff1 = df[df['table_name'] == dropdown_value_tmp]
        dff2 = dff1[dff1['column_name'].str.contains('|'.join(dropdown_value2))]
        dff3 = dff1.merge(dff2)

        fig4_3 = go.Figure(go.Bar(
            x=dff3['column_name'],
            y=dff3['unique_values_count'],
            # orientation='h',
            text=dff3['unique_values_count'],
            textposition='auto',
            marker_color='#46648c',
            texttemplate='%{text:.4s}',
            textfont=dict(
                family="sans serif",
                size=19,
                color="#e98074"
            )
        ))

        fig4_3.update_layout(
            title={
                'text': "Unique Values",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'})

        return fig4_3

    if dropdown_value is None and dropdown_value2 is None:
        dropdown_value_tmp = 'advisor'
        dff1 = df[df['table_name'] == dropdown_value_tmp]
        dff2 = dff1[dff1['column_name'].str.contains('|'.join(dropdown_value2))]
        dff3 = dff1.merge(dff2)

        fig4_4 = go.Figure(go.Bar(
            x=dff3['column_name'],
            y=dff3['unique_values_count'],
            # orientation='h',
            text=dff3['unique_values_count'],
            textposition='auto',
            marker_color='#46648c',
            texttemplate='%{text:.4s}',
            textfont=dict(
                family="sans serif",
                size=19,
                color="#e98074"
            )
        ))

        fig4_4.update_layout(
            title={
                'text': "Unique Values",
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'})

        return fig4_4


@app.callback(dash.dependencies.Output(component_id='tg4', component_property='figure'),
              [dash.dependencies.Input(component_id='dropdown', component_property='value'),
               dash.dependencies.Input(component_id='dropdown_child', component_property='value')])
def update_fig3(dropdown_value, dropdown_value2):

    if dropdown_value is not None and dropdown_value2 is None:
        dff3 = df[df['table_name'] == dropdown_value]

        fig4 = go.Figure(data=[
            go.Bar(name='Non-Null %', x=dff3['column_name'], y=dff3['%_of_non_nulls'], text=dff3['%_of_non_nulls'],
                   textposition='auto', marker_color='#065464', texttemplate='%{text:.4s}'),
            go.Bar(name='Null %', x=dff3['column_name'], y=dff3['%_of_nulls'],
                   text=dff2['%_of_nulls'], textposition='auto', marker_color='#e98074',
                   texttemplate='%{text:.4s}')

        ])

        fig4.update_layout(barmode='group',
                           title={
                                 'text': "Non-Null vs Nulls %",
                                 'y': 0.9,
                                 'x': 0.5,
                                 'xanchor': 'center',
                                 'yanchor': 'top'})

        return fig4

    if dropdown_value is not None and dropdown_value2 is not None:
        dff1 = df[df['table_name'] == dropdown_value]
        dff2 = dff1[dff1['column_name'].str.contains('|'.join(dropdown_value2))]
        dff3 = dff1.merge(dff2)

        fig4_2 = go.Figure(data=[
            go.Bar(name='Non-Null %', x=dff3['column_name'], y=dff3['%_of_non_nulls'], text=dff3['%_of_non_nulls'],
                   textposition='auto', marker_color='#065464', texttemplate='%{text:.4s}'),
            go.Bar(name='Null %', x=dff3['column_name'], y=dff3['%_of_nulls'],
                   text=dff2['%_of_nulls'], textposition='auto', marker_color='#e98074',
                   texttemplate='%{text:.4s}')

        ])

        fig4_2.update_layout(barmode='group',
                             title={
                                 'text': "Non-Null vs Nulls %",
                                 'y': 0.9,
                                 'x': 0.5,
                                 'xanchor': 'center',
                                 'yanchor': 'top'})

        return fig4_2

    if dropdown_value is None and dropdown_value2 is not None:
        dropdown_value_tmp = 'advisor'
        dff1 = df[df['table_name'] == dropdown_value_tmp]
        dff2 = dff1[dff1['column_name'].str.contains('|'.join(dropdown_value2))]
        dff3 = dff1.merge(dff2)

        fig4_3 = go.Figure(data=[
            go.Bar(name='Non-Null %', x=dff3['column_name'], y=dff3['%_of_non_nulls'], text=dff3['%_of_non_nulls'],
                   textposition='auto', marker_color='#065464', texttemplate='%{text:.4s}'),
            go.Bar(name='Null %', x=dff3['column_name'], y=dff3['%_of_nulls'],
                   text=dff2['%_of_nulls'], textposition='auto', marker_color='#e98074',
                   texttemplate='%{text:.4s}')

        ])

        fig4_3.update_layout(barmode='group',
                             title={
                                 'text': "Non-Null vs Nulls %",
                                 'y': 0.9,
                                 'x': 0.5,
                                 'xanchor': 'center',
                                 'yanchor': 'top'})

        return fig4_3

    if dropdown_value is None and dropdown_value2 is None:
        dropdown_value_tmp = 'advisor'
        dff1 = df[df['table_name'] == dropdown_value_tmp]
        dff2 = dff1[dff1['column_name'].str.contains('|'.join(dropdown_value2))]

        fig4_4 = go.Figure(data=[
            go.Bar(name='Non-Null %', x=dff1['column_name'], y=dff1['%_of_non_nulls'], text=dff1['%_of_non_nulls'],
                   textposition='auto', marker_color='#065464', texttemplate='%{text:.4s}'),
            go.Bar(name='Null %', x=dff1['column_name'], y=dff1['%_of_nulls'],
                   text=dff2['%_of_nulls'], textposition='auto', marker_color='#e98074',
                   texttemplate='%{text:.4s}')

        ])

        fig4_4.update_layout(barmode='group',
                             title={
                               'text': "Non-Null vs Nulls %",
                               'y': 0.9,
                               'x': 0.5,
                               'xanchor': 'center',
                               'yanchor': 'top'})

        return fig4_4


@app.callback(dash.dependencies.Output(component_id='tg5', component_property='figure'),
              [dash.dependencies.Input(component_id='dropdown', component_property='value'),
               dash.dependencies.Input(component_id='dropdown_child', component_property='value')])
def update_fig3(dropdown_value, dropdown_value2):

    if dropdown_value is not None and dropdown_value2 is None:
        dff3 = df[df['table_name'] == dropdown_value]

        fig51 = go.Figure(data=[
            go.Bar(name='PK Candidates', x=dff3['column_name'], y=dff3['PK_Flag'], text=dff3['PK_Flag'],
                   textposition='auto', marker_color='#6ab187', texttemplate='%{text:.0s}')

        ])

        fig51.update_layout(title={
            'text': "PK Candidate based on Cardinality %",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

        return fig51

    if dropdown_value is not None and dropdown_value2 is not None:
        dff1 = df[df['table_name'] == dropdown_value]
        dff2 = dff1[dff1['column_name'].str.contains('|'.join(dropdown_value2))]
        dff3 = dff1.merge(dff2)

        fig52 = go.Figure(data=[
            go.Bar(name='PK Candidates', x=dff3['column_name'], y=dff3['PK_Flag'], text=dff3['PK_Flag'],
                   textposition='auto', marker_color='#6ab187', texttemplate='%{text:.0s}')

        ])

        fig52.update_layout(title={
            'text': "PK Candidate based on Cardinality %",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

        return fig52

    if dropdown_value is None and dropdown_value2 is not None:
        dropdown_value_tmp = 'advisor'
        dff1 = df[df['table_name'] == dropdown_value_tmp]
        dff2 = dff1[dff1['column_name'].str.contains('|'.join(dropdown_value2))]
        dff3 = dff1.merge(dff2)

        fig53 = go.Figure(data=[
            go.Bar(name='PK Candidates', x=dff3['column_name'], y=dff3['PK_Flag'], text=dff3['PK_Flag'],
                   textposition='auto', marker_color='#6ab187', texttemplate='%{text:.0s}')

        ])

        fig53.update_layout(title={
            'text': "PK Candidate based on Cardinality %",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

        return fig53

    if dropdown_value is None and dropdown_value2 is None:
        dropdown_value_tmp = 'advisor'
        dff1 = df[df['table_name'] == dropdown_value_tmp]
        dff2 = dff1[dff1['column_name'].str.contains('|'.join(dropdown_value2))]

        fig54 = go.Figure(data=[
            go.Bar(name='PK Candidates', x=dff1['column_name'], y=dff1['PK_Flag'], text=dff1['PK_Flag'],
                   textposition='auto', marker_color='#6ab187', texttemplate='%{text:.0s}')

        ])

        fig54.update_layout(title={
            'text': "PK Candidate based on Cardinality %",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

        return fig54


if __name__ == '__main__':
    app.run_server(debug=True)