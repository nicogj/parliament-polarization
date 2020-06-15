import matplotlib.pyplot as plt
import plotly.io as pio
import argparse
import pandas as pd

from utils.dim_reduction import pca_plot

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('country_code', help='which country?')
    parser.add_argument('chamber', help='which chamber?')
    parser.add_argument('legislature_num', help='which legislature?')
    args = parser.parse_args()

    print("Plotting {} {} {}".format(args.country_code.upper(), args.chamber, args.legislature_num))

    pca_df = pd.read_csv('data/votes_{}_{}_{}_pca.tsv'.format(args.country_code, args.chamber, args.legislature_num), sep='\t')

    fig = pca_plot(pca_df, type='static')
    plt.savefig('output/votes_{}_{}_{}_pca.png'.format(args.country_code, args.chamber, args.legislature_num), bbox_inches='tight')

    fig = pca_plot(pca_df, type='plotly')
    pio.write_html(fig, file='output/votes_{}_{}_{}_pca.html'.format(args.country_code, args.chamber, args.legislature_num), auto_open=False)

    print("Done !")
