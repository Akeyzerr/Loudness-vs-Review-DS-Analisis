import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3 as sql
from mpl_toolkits.axes_grid1 import host_subplot

def reviews_sql_read(sqldb_path, tables, merge_on='reviewid'):
    """
    A function to read a sqlite3 db and return pandas.dataframe obj.
    """
    db_read = sql.connect(sqldb_path)
    result_df = pd.DataFrame()
    for table in tables:
        temp_df = pd.read_sql(f'SELECT * FROM {table}', db_read)
        if merge_on in result_df:
            result_df = pd.merge(result_df, temp_df, how='left', on=merge_on)
        else:
            result_df = temp_df.copy()
    db_read.close()
    return result_df

def reviews_sql_cleanup(df):
    pass

def artists_list_to_artist(df, column='artist', fltr='['):
    """
    A function to filter and simplify the string
    for artists from Spotify's API 
    """
    if fltr in df[f'{column}'].any():
        df[f'{column}'] = df[f'{column}'].str.slice(1, -1)
        df[f'{column}'] = df[f'{column}'].str.split(', ', 1)
        df[f'{column}'] = [artist[0][1:-1] for artist in df[f'{column}']]
    return df

def graph_loudnes_per_artist(df, artist, column='artist_y', value='loudness'):
    result = pd.DataFrame(columns=df.columns)
    for i in range(len(artist)):
        result = pd.concat([result, df.loc[df[f'{column}'] == f'{artist[i]}']])
    result.dropna(inplace=True)
    result.reset_index(inplace=True)
    artists_dict = {}
    plt.figure(figsize=(12,7))
    plt.style.use('ggplot')
    for e in range(len(artist)):
        plot_data = result.loc[result[f'{column}'] == f'{artist[e]}'].pivot_table(values=value, index='year', aggfunc=np.mean, margins=True)
        plt.scatter(plot_data.index[:-1], plot_data.loudness[:-1], marker='+', lw=2, alpha=1)
        plt.plot(plot_data.index[:-1], plot_data.loudness[:-1], marker='+', lw=2, alpha=.5)
        artists_dict.update({f'{artist[e].title()}': e})
#     print(artists_dict)
    plt.ylim(-18, -2)
    plt.xlabel('Years')
    plt.ylabel('Loudness (dB)')
    if len(artists_dict.keys()) > 1:
        plt.title(f'Loudness for {len(artists_dict.keys())} various artists through the years')
    else:
        plt.title(f'Loudness for {artist[0].upper()} through the years')
    plt.legend(artists_dict, fontsize=14)
    plt.show()
    
def graph_scores_per_artist(df, artist, column='artist_y', value='year_mean_score_per_artist'):
    result = pd.DataFrame(columns=df.columns)
    for i in range(len(artist)):
        result = pd.concat([result, df.loc[df[f'{column}'] == f'{artist[i]}']])
    result.dropna(inplace=True)
    result.sort_values('year', inplace=True)
    result.reset_index(inplace=True)
    artists_dict = {'Year mean score': 0}
    plt.figure(figsize=(12,7))
    plt.style.use('ggplot')
    plt.scatter(result.year, result.year_mean_score)
    plt.plot(result.year, result.year_mean_score, alpha=0)
    for e in range(len(artist)):
        plot_data = result.loc[result[f'{column}'] == f'{artist[e]}']
        print(plot_data.sample())
        plt.scatter(plot_data.year[:-1], plot_data.year_mean_score_per_artist[:-1], marker='+', lw=2, alpha=1)
        plt.plot(plot_data.year[:-1], plot_data.year_mean_score_per_artist[:-1], marker='+', lw=2, alpha=.25)
        artists_dict.update({f'{artist[e].title()}': e+1})
    plt.xlabel('Years')
    plt.ylabel('Loudness (dB)')
    plt.ylim(3,12)
    if len(artists_dict.keys()) > 2:
        plt.title(f'Loudness for {len(artists_dict.keys())-1} various artists through the years')
    else:
        plt.title(f'Loudness for {artist[0].upper()} through the years')
    plt.legend(artists_dict, fontsize=14)
    plt.show()

def successful_imports():
    success = 'Imports from akeyzerr_exam module have been successful'
    return success
