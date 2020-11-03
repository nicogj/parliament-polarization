import pandas as pd
import numpy as np
from tqdm.auto import tqdm

fr_party_df = pd.DataFrame([
    ['Groupe La République en Marche', 'LREM'],
    ['Groupe Les Républicains', 'LR'],
    ['Groupe du Mouvement Démocrate et apparentés', 'MODEM'],
    ['Groupe Les Constructifs\xa0: républicains, UDI, indépendants', 'UDI'],
    ['Groupe Nouvelle Gauche', 'PS'],
    ['Groupe La France insoumise', 'FI'],
    ['Groupe de la Gauche démocrate et républicaine', 'Divers Gauche'],
    ['Non inscrits', 'Non Inscrits'],
    ['Groupe UDI, Agir et Indépendants', 'UDI'],
    ['Groupe Socialistes et apparentés', 'PS'],
    ['Groupe Libertés et Territoires', 'Libertés et Territoires'],
    ['Groupe UDI et Indépendants', 'UDI'],
    ['Groupe Écologie Démocratie Solidarité', 'Écologie Démocratie Solidarité'],
    ['Groupe Agir Ensemble', 'UDI']
], columns=['party', 'party_clean'])

us_party_df = pd.DataFrame([
    ['D', 'Democratic'],
    ['R', 'Republican'],
    ['I', 'Independent']
], columns=['party', 'party_clean'])

def print_duplicates(df):

    for i in tqdm(list(set(df['vote_num']))):
        temp = pd.DataFrame(df[df['vote_num']==i]['id'].value_counts())
        if temp['id'].max()>1:
            print("Vote {}:".format(i))
            print(temp[temp['id']>1])

def cleaning_vote_outcomes(df, country_code):

    if country_code == 'us':
        id_vars = ['name', 'state']
        df = pd.merge(df, us_party_df, how='left', on='party')

    if country_code == 'fr':
        id_vars = ['name']

        df['name'] = df['name'].str.replace(r'\s\(par\sdélégation\)', '')
        df['name'] = df['name'].str.replace(r'\s\(Présidente?\sde\sséance\)', '')
        df['name'] = df['name'].str.replace(r'\s\(Présidente?\sde\sl\'Assemblée\snationale\)', '')
        df['name'] = df['name'].str.replace(r'\s\(Membre\sdu\sGouvernement\)', '')
        df['name'] = df['name'].str.strip()

        df = df[df['name'].str.contains(r'\bM\.\s')==False]
        df = df[df['name'].str.contains(r'\bMme\s')==False]
        df = df[df['name'].str.contains(r'\,')==False]
        df = df[df['name'].str.contains(r'\set\s')==False]

        df['name'] = df['name'].str.replace(r'\.', '')
        df['name'] = df['name'].str.replace(u'\xa0', ' ')
        df['name'] = df['name'].str.strip()

        df['party'] = df['party'].str.strip()
        df = pd.merge(df, fr_party_df, how='left', on='party')

    # Replace by Numbers
    df['vote_temp'] = 0
    df.loc[df['vote']=='Pour', 'vote_temp']=1
    df.loc[df['vote']=='Yea', 'vote_temp']=1
    df.loc[df['vote']=='Contre', 'vote_temp']=-1
    df.loc[df['vote']=='Nay', 'vote_temp']=-1
    del df['vote']
    df.rename(columns={'vote_temp':'vote'}, inplace=True)

    df['id'] = df.groupby(id_vars).ngroup()
    print("Checking duplicate names")
    print_duplicates(df)

    if country_code=='fr':
        geocols = []
    elif country_code=='us':
        geocols = ['state']

    info_df = df[['id', 'name', 'party_clean']+geocols].drop_duplicates('id', keep='last').rename(columns={'party_clean':'party'})

    if country_code == 'fr':
        info_df['info'] = info_df['party']
    elif country_code == 'us':
        info_df['info'] = info_df['state']+", "+info_df['party']

    df = df.pivot(index='id', columns='vote_num', values='vote')

    return df, info_df

def data_restriction(df, vote_freq_cutoff, ind_freq_cutoff):

    print("Before restriction: {} individuals and {} votes".format(df.shape[0], df.shape[1]))

    # Restrict Votes:
    big_vote = (df.count(axis=0) > vote_freq_cutoff*df.shape[0])
    df = df.loc[:, big_vote]

    # Restrict Individuals
    big_voter = (df.count(axis=1) > ind_freq_cutoff*df.shape[1])
    df = df.loc[big_voter, :]

    print("After restriction: {} individuals and {} votes".format(df.shape[0], df.shape[1]))

    return df
