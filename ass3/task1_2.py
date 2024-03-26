import pandas as pd
def solve_task1_2(hyperlinks_file_path, dict_path):
    hyperlinks_df = pd.read_csv(hyperlinks_file_path, sep='\t')

    dict_df = pd.read_csv(dict_path, sep='\t', header=None, names=['identifier', 'subreddit'])

    hyperlinks_df = hyperlinks_df.merge(dict_df, left_on='SOURCE_SUBREDDIT', right_on='subreddit', how='left')
    hyperlinks_df.rename(columns={'identifier': 'source_identifier'}, inplace=True)
    hyperlinks_df.drop('subreddit', axis=1, inplace=True)

    hyperlinks_df = hyperlinks_df.merge(dict_df, left_on='TARGET_SUBREDDIT', right_on='subreddit', how='left')
    hyperlinks_df.rename(columns={'identifier': 'target_identifier'}, inplace=True)
    hyperlinks_df.drop('subreddit', axis=1, inplace=True)

    hyperlinks_df['TIMESTAMP'] = pd.to_datetime(hyperlinks_df['TIMESTAMP']).dt.tz_localize('Asia/Hong_Kong').dt.tz_convert(None)

    hyperlinks_df['TIMESTAMP'] = (hyperlinks_df['TIMESTAMP'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')

    hyperlinks_df.drop_duplicates(subset=['source_identifier', 'TIMESTAMP', 'target_identifier'], inplace=True)

    hyperlinks_df.sort_values(by=['TIMESTAMP', 'target_identifier'], inplace=True)

    hyperlinks_df['interaction'] = hyperlinks_df.apply(
        lambda x: f"{x['TIMESTAMP']},{x['target_identifier']},{x['LINK_SENTIMENT']}", axis=1)

    adjacency_list = hyperlinks_df.groupby('source_identifier')['interaction'].apply(lambda x: ' '.join(x)).reset_index(name='interactions')

    adjacency_list.to_csv('graph.tsv', sep='\t', index=False, header=False)

    return

if __name__ == "__main__":
    solve_task1_2("../dataset/soc-redditHyperlinks-title.tsv", "dict.tsv")
