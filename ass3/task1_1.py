import pandas as pd

def solve_task_1_1(file_path):
    df = pd.read_csv(file_path, sep='\t')
    source_subreddits = df['SOURCE_SUBREDDIT']
    target_subreddits = df['TARGET_SUBREDDIT']

    all_subreddits = pd.concat([source_subreddits, target_subreddits]).drop_duplicates()

    sorted_subreddits = all_subreddits.sort_values()
    sorted_subreddits_df = pd.DataFrame(sorted_subreddits).reset_index(drop=True)

    sorted_subreddits_df.to_csv('dict.tsv', sep='\t', index_label='index', header=False)

    return

if __name__ == "__main__":
    file_path = '../dataset/soc-redditHyperlinks-title.tsv'
    solve_task_1_1(file_path)
