# python3 scripts/visualizations.py fr assemblee 15

import matplotlib.pyplot as plt
import plotly.io as pio
import argparse
import pandas as pd
import chart_studio
import chart_studio.plotly as py
chart_studio.tools.set_credentials_file(username='nicogj', api_key='DkQKByIZRu5QoLqq7TUe')

from utils.plotting import dim_reduc_plot

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('country_code', help='which country?')
    parser.add_argument('chamber', help='which chamber?')
    parser.add_argument('legislature_num', help='which legislature?')
    args = parser.parse_args()

    print("Plotting {} {} {}".format(args.country_code.upper(), args.chamber, args.legislature_num))

    dim_reduc_df = pd.read_csv('data/votes_{}_{}_{}_pca.tsv'.format(args.country_code, args.chamber, args.legislature_num), sep='\t')

    fig = dim_reduc_plot(dim_reduc_df, args, type='static')
    plt.savefig('output/votes_{}_{}_{}_pca.png'.format(args.country_code, args.chamber, args.legislature_num), bbox_inches='tight')

    fig = dim_reduc_plot(dim_reduc_df, args, type='plotly')
    py.plot(fig, filename='votes_{}_{}_{}_pca'.format(args.country_code, args.chamber, args.legislature_num), auto_open=False)
    pio.write_html(
        fig, file='output/votes_{}_{}_{}_pca.html'.format(args.country_code, args.chamber, args.legislature_num),
        auto_open=False,
        config={
            'modeBarButtonsToRemove': ['lasso2d', 'resetScale2d', 'toggleSpikelines','hoverCompareCartesian', 'hoverClosestCartesian']
        }
    )
    print("Done !")
