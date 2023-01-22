import psycopg2 as p
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def search(query, search_within, start_year, end_year, export):
    results = {'dkey':[], 'doi':[], 'title':[], 'author':[], 'year':[]}
    if start_year != 'all_start_year' and end_year != 'all_end_year':
        if start_year > end_year:
            info = "end year must greater than start year"
            return results, info
    if start_year == 'all_start_year':
        start_year = 1960
    else:
        start_year = int(start_year) - 1
    if end_year == 'all_end_year':
        end_year = 2024
    else:
        end_year = int(end_year) + 1
    con = p.connect('postgresql://rccuser:password@localhost:5432/generalindex_metadata')
    cur = con.cursor()
    if search_within == 'title':
        sql = "select dkey,doi,title,author,year from metadata_recent where title like '%{query}%' and year > '{start_year}' and year < '{end_year}' limit 10000".format(query=query, start_year=start_year, end_year=end_year)
    elif search_within == 'author':
        sql = "select dkey,doi,title,author,year from metadata_recent where author like '%{query}%' and year > '{start_year}' and year < '{end_year}' limit 10000".format(query=query, start_year=start_year, end_year=end_year)
    elif search_within == 'doi':
        sql = "select dkey,doi,title,author,year from metadata_recent where doi like '%{query}%' and year > '{start_year}' and year < '{end_year}' limit 10000".format(query=query, start_year=start_year, end_year=end_year)
    else:
        sql = "select dkey,doi,title,author,year from metadata_recent limit 1000;"
    cur.execute(sql)
    data = cur.fetchall()
    for item in data:
        results['dkey'].append(item[0])
        results['doi'].append(item[2])
        results['title'].append(item[1])
        results['author'].append(item[3])
        results['year'].append(item[4])
    # use pandas dataframe to store results for later use, you can use the dataframe to create plot.
    metadata_df = pd.DataFrame(data=results)
    # if user ticks export as csv, the result will save in the same directory where they run the app.
    # Note that only one export can be saved at any one time
    # filestamp
    file_to_save = rf'./results_Datetime:{datetime.now()}_SearchTerm:{query}_YearBetween:{start_year}And{end_year}.csv'
    if export == 'yes':
        metadata_df.to_csv(file_to_save, sep='\t', encoding='utf-8', header=True, index=False)
    
    cur.close()
    con.close()
    
    #plot settings
    fig, ax = plt.subplots()
    ax = metadata_df['year'].value_counts(sort=False).plot(ax=ax, kind='bar')
    ax.bar_label(ax.containers[0])
    ax.set_ylabel('Frequency')
    fig.suptitle("Frequency over time")
    fig.savefig("static/IMG/year_plot.png")
    
    info = ''
    return metadata_df, info
