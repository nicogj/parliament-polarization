import pandas as pd
import numpy as np
from sklearn.decomposition import PCA as sklearnPCA
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def pca_analysis(X, ids, info_df):

    X_std = StandardScaler().fit_transform(X)
    sklearn_pca = sklearnPCA(n_components=2, random_state=123)
    coords = sklearn_pca.fit_transform(X_std)

    pca_df = pd.DataFrame(coords).rename(columns={0:'pca_1', 1:'pca_2'})
    pca_df['id'] = ids
    pca_df = pd.merge(pca_df, info_df, how='left', on='id')

    # Rotate Left Right in the US:
    if pca_df.loc[pca_df['pca_1'].values.argmin(), 'party']=="R":
        pca_df['pca_1'] = -pca_df['pca_1']

    # # Center on param.central:
    # glg = "Gilles Le Gendre"
    # pca_df['pca_1'] = pca_df['pca_1'] - pca_df[pca_df['name']==glg]['pca_1'].values[0]
    # pca_df['pca_2'] = pca_df['pca_2'] - pca_df[pca_df['name']==glg]['pca_2'].values[0]

    return pca_df#[['id', 'name', 'party', 'pca_1', 'pca_2']]

def pca_plot(df, type='plotly'):

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
    ids['us_senate'] = [
        7, 18, 22, 25, 31, 34, 37, 47, 48, 50, 51, 57, 58, 63, 66, 70, 73, 76, 77, 80, 96
    ]

    if type == 'static':
        # Matplotlib version
        pca_1 = df['pca_1'].values
        pca_2 = df['pca_2'].values
        name_fontsize = [5 for x in df['name']]
        name_color = ['black' for x in df['name']]
        color = [color_dict[party] for party in df['party']]
        names = df['name'].values
        fig, ax = plt.subplots(figsize = (10,10))
        for _x, _y, _c, _txt, _nc, _ns in zip(pca_1, pca_2, color, names, name_color, name_fontsize):
            ax.scatter(_x, _y, color=_c)
            ax.annotate(_txt, (_x, _y), fontsize=_ns, color=_nc)
        ax.set_title('Distribution des Députés selon leurs Votes à l\'Assemblée', size = 'xx-large')
        plt.xlabel('Composante Principale 1', size = 'x-large')
        plt.ylabel('Composante Principale 2', size = 'x-large')
        return fig

    elif type == 'plotly':
        fig = go.Figure()
        for party_subset in list(set(df['party'].values)):
            temp = df[df['party']==party_subset]
            fig.add_trace(go.Scatter(
                    x=temp["pca_1"], y=temp["pca_2"], mode='markers',
                    marker_color = [color_dict[party] for party in temp['party']], marker_opacity=0.8,
                    text = ["<b>{}</b> ({})".format(name, info) for name, info in zip(temp['name'], temp['info'])],
                    hovertemplate = '%{text}<extra></extra>', name = party_subset
                ))
        fig.update_traces(
            marker=dict(size=8, line=dict(width=1, color='DarkSlateGrey')), selector=dict(mode='markers'),
            hoverlabel=dict(bgcolor='white')
        )
        fig.update_layout(
            legend_orientation="h", legend_title_text=None,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis_title=None, yaxis_title=None,
        )
        return fig
