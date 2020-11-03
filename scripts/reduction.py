# python3 scripts/reduction.py fr assemblee 15 --dim_reduc pca

import pandas as pd
import numpy as np
import argparse
import os
import matplotlib.pyplot as plt

from utils.cleaning import cleaning_vote_outcomes, data_restriction
from utils.dim_reduction import get_dim_reduction

DATA_PATH = '/Users/nico/Dropbox (MIT)/data_lake/parliament_voting_data/'

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('country_code', help='which country?')
    parser.add_argument('chamber', help='which chamber?')
    parser.add_argument('legislature_num', help='which legislature or year?')
    parser.add_argument('--vote_freq_cutoff', default = 0.25, type = float, help='what share of people have to vote for the vote to count?')
    parser.add_argument('--ind_freq_cutoff', default = 0.5, type = float, help='What share of votes must a person cast to count?')
    parser.add_argument('--dim_reduc', default = 'pca', type = str, help='Which type of dimension reduction?')
    args = parser.parse_args()

    print("\nRunning {} {} {}".format(args.country_code.upper(), args.chamber, args.legislature_num))

    if args.country_code=='fr':
        votes = pd.read_csv(DATA_PATH + 'france_assemblee_voting/legislature_{}_vote_outcome.tsv'.format(args.legislature_num), sep='\t')

    elif args.country_code=='us' and args.chamber == 'senate':
        votes = pd.read_csv(DATA_PATH + 'us_senate_voting/congress_{}_1_vote_outcome.tsv'.format(args.legislature_num), sep='\t')
        votes['vote_num'] = "1_" + votes['vote_num'].astype(str)
        if os.path.exists(DATA_PATH + 'us_senate_voting/congress_{}_1_vote_outcome.tsv'.format(args.legislature_num)):
            votes_2 = pd.read_csv(DATA_PATH + 'us_senate_voting/congress_{}_2_vote_outcome.tsv'.format(args.legislature_num), sep='\t')
            votes_2['vote_num'] = "2_" + votes['vote_num'].astype(str)
            votes = pd.concat([votes, votes_2])
            del votes_2

    df, info_df = cleaning_vote_outcomes(votes, args.country_code)

    df = data_restriction(df, vote_freq_cutoff=args.vote_freq_cutoff, ind_freq_cutoff=args.ind_freq_cutoff)

    # PCA Analysis
    dim_reduc_df = get_dim_reduction(df, info_df, reduc_type=args.dim_reduc, weighted=False)
    dim_reduc_df.to_csv('data/votes_{}_{}_{}_{}.tsv'.format(args.country_code, args.chamber, args.legislature_num, args.dim_reduc), sep='\t', index=False)

    print("Done !")
