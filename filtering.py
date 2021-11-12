

def filter(column_name, filter_out, pct, df):

    rows_removed = 0

    rows_with_undesired_element = len(df[(df['votes'] == 0)])

    # Iterate through the dataframe removing rows that contain the 'filter_out' element
    for index, row in df.iterrows():
        if row[column_name] == filter_out and rows_removed < rows_with_undesired_element*pct:
            df = df.drop(index)
            rows_removed += 1

    return df

