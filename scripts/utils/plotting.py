import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

def dim_reduc_plot(df, args, type='plotly', display_names=False):

    run_name = '{}_{}_{}'.format(args.country_code, args.chamber, args.legislature_num)

    color_dict = {}
    for party in list(set(df['party'])):
        color_dict[party] = 'grey'

    # France
    color_dict['LREM'] = 'yellow'
    color_dict['UDI'] = 'orange'
    color_dict['MODEM'] = 'orange'
    color_dict['LR'] = 'blue'
    color_dict['PS'] = 'pink'
    color_dict['FI'] = 'red'
    color_dict['Divers Gauche'] = 'red'
    color_dict['FN'] = 'black'
    color_dict['Écologie Démocratie Solidarité'] = 'green'

    # US
    color_dict['Democratic'] = 'blue'
    color_dict['Republican'] = 'red'
    color_dict['Independent'] = 'green'

    ids = {}
    ids['us_senate_116'] = [
        18, 25, 31, 37, 47, 51, 57, 58, 66, 70, 73, 77, 80
    ]
    if run_name not in ids:
        ids[run_name] = []
    df['display_name'] = [name if id in ids[run_name] else "" for name, id in zip(df['name'], df['id'])]

    if type == 'static':
        # Matplotlib version
        axis_1 = df['axis_1'].values
        axis_2 = df['axis_2'].values
        name_fontsize = [5 for x in df['name']]
        name_color = ['black' for x in df['name']]
        color = [color_dict[party] for party in df['party']]
        names = df['name'].values
        fig, ax = plt.subplots(figsize = (10,10))
        for _x, _y, _c, _txt, _nc, _ns in zip(axis_1, axis_2, color, names, name_color, name_fontsize):
            ax.scatter(_x, _y, color=_c)
            ax.annotate(_txt, (_x, _y), fontsize=_ns, color=_nc)
        plt.xlabel('First Principal Component', size = 'x-large')
        plt.ylabel('Second Principal Component', size = 'x-large')
        return fig

    elif type == 'plotly':
        fig = go.Figure()
        for party_subset in list(set(df['party'].values)):
            temp = df[df['party']==party_subset]
            fig.add_trace(go.Scatter(
                    x=temp["axis_1"], y=temp["axis_2"], mode='markers',
                    marker_color = [color_dict[party] for party in temp['party']], marker_opacity=0.8,
                    text = ["<b>{}</b> ({})".format(name, info) for name, info in zip(temp['name'], temp['info'])],
                    hovertemplate = '%{text}<extra></extra>', name = party_subset,
                ))
        fig.update_traces(
            marker=dict(size=8, line=dict(width=1, color='DarkSlateGrey')), selector=dict(mode='markers'),
            hoverlabel=dict(bgcolor='white')
        )
        fig.update_layout(
            legend_orientation="h", legend_title_text=None,
            margin=dict(l=0, r=0, t=0, b=0),
            autosize=True, width=1000, height=1000,
            xaxis_title="First Principal Component", yaxis_title="Second Principal Component",
            yaxis={'showticklabels': False},
            xaxis={'showticklabels': False}
        )
        fig.add_trace(go.Scatter(
                x=df["axis_1"], y=df["axis_2"], mode='text',
                text = ["<b>{}</b>".format(x) for x in df['display_name']], textposition='bottom left',
                textfont=dict(
                    # family='Balto'
                ),
                hoverinfo='skip',
                showlegend=False
            ))
        return fig
