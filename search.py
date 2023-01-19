import sqlite3

def search(query, search_within, start_year, end_year):
    results = {}
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
    con = sqlite3.connect('metadata.db')
    cur = con.cursor()
    if search_within == 'title':
        sql = "select * from t where title like '%{query}%' and year > '{start_year}' and year < '{end_year}' limit 10000".format(query=query, start_year=start_year, end_year=end_year)
    elif search_within == 'author':
        sql = "select * from t where author like '%{query}%' and year > '{start_year}' and year < '{end_year}' limit 10000".format(query=query, start_year=start_year, end_year=end_year)
    elif search_within == 'doi':
        sql = "select * from t where doi like '%{query}%' and year > '{start_year}' and year < '{end_year}' limit 10000".format(query=query, start_year=start_year, end_year=end_year)
    else:
        sql = "select * from t limit 1000"
    data = cur.execute(sql)
    for item in data:
        results[item[0]] = [item[2], item[1], item[3], item[4]]
    cur.close()
    con.close()
    info = 'succed'
    return results, info
