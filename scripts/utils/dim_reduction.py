import pandas as pd
import numpy as np
from sklearn.decomposition import PCA as sklearnPCA
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm

def get_dim_reduction(df, info_df, reduc_type='pca', weighted=False):

    X = np.array(df.fillna(0))
    X_std = StandardScaler().fit_transform(X)

    if weighted==True:
        share_vote = np.array(df.count(axis=0)/df.shape[0])
        X_std = np.array(df.fillna(0)) * share_vote

    if reduc_type=='pca':
        sklearn_pca = sklearnPCA(n_components=2, random_state=123)
        coords = sklearn_pca.fit_transform(X_std)

    else:
        if reduc_type=='tsne':
            mds = manifold.TSNE(
                n_components=2, n_jobs=-1, n_iter=10000, random_state=123, early_exaggeration=5
            )
        elif reduc_type=='mds':
            mds = manifold.MDS(
                n_components=2, dissimilarity="euclidean", random_state=6, n_init=6, n_jobs=-1, max_iter=500
            )
        else:
            print("Choose a proper reduction type.")
        results = mds.fit(X_std)
        coords = results.embedding_

    dim_reduc_df = pd.DataFrame(coords).rename(columns={0:'axis_1', 1:'axis_2'})
    dim_reduc_df['id'] = df.index
    dim_reduc_df = pd.merge(dim_reduc_df, info_df, how='left', on='id')

    # Rotate Left Right in the US:
    if dim_reduc_df.loc[dim_reduc_df['axis_1'].values.argmin(), 'party']=="R":
        dim_reduc_df['axis_1'] = -dim_reduc_df['axis_1']

    return dim_reduc_df
