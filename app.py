#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dash  
import dash_core_components as dcc 
import dash_html_components as html  
from datetime import datetime
import pandas
import plotly.graph_objs as go

# appという箱作り①
app = dash.Dash(__name__)


#データをloadする
colors = {
    'background': '#008080',
    'text': '#7FDBFF'
}




bmon_cancel=pandas.read_csv("bmonster_canceldata.csv")
# データを整える
bmon_cancel=[datetime.strptime(i, '%Y/%m/%d %H:%M:%S') for i in bmon_cancel['date_time'], '%Y/%m/%d %H:%M:%S')]
df.groupby(pd.TimeGrouper(freq='10Min')).count().plot(kind='bar')





# appという箱に中身を詰める②
app.layout = html.Div(
    style={'backgroundColor': colors['background']},
    children =[
        # H1を設定
        html.H1(
            children='Hello Dash',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        # divを設定
        html.Div(
            children='Dash: A web application framework for Python.'
        ),

        # graphを描く
        dcc.Graph(
            # htmlのidを描く
            id = "first-graph",

            figure={
                'data': [
                    go.Scatter(
                        x=bmon_cancel.loc[:,'date_time_onlytime'],
                        y=bmon_cancel.loc[:,'time_of_lesson'],
                        text=bmon_cancel.loc[:,'performer'],
                        mode='markers',
                        opacity=0.7,
                        marker={
                            'size': 15,
                            'line': {'width': 0.5, 'color': 'white'}
                        }
                    )
                ],
                'layout':go.Layout(
                    xaxis={'title':'date_time'},
                    yaxis={'title': 'time_of_lesson'},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    legend={'x': 0, 'y': 1},
                    hovermode='closest'
                )
            }
        )
])

# 実行用③
if __name__=='__main__':
    app.run_server(debug=True)

