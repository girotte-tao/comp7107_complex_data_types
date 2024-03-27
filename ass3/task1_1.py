import pandas as pd

def solve_task_1_1(file_path):
    try:
        df = pd.read_csv(file_path, sep='\t')
    except FileNotFoundError:
        return "File not found. Please check the file path."
    except Exception as e:
        return f"An error occurred while reading the file: {e}"

    required_columns = {'SOURCE_SUBREDDIT', 'TARGET_SUBREDDIT'}
    if not required_columns.issubset(df.columns):
        return "File does not contain the required columns."

    try:
        source_subreddits = df['SOURCE_SUBREDDIT']
        target_subreddits = df['TARGET_SUBREDDIT']

        all_subreddits = pd.concat([source_subreddits, target_subreddits]).drop_duplicates()
        sorted_subreddits = all_subreddits.sort_values()
        sorted_subreddits_df = pd.DataFrame(sorted_subreddits).reset_index(drop=True)

        sorted_subreddits_df.to_csv('dict.tsv', sep='\t', index_label='index', header=False)
    except Exception as e:
        return f"An error occurred while processing the data: {e}"

    return "Process completed successfully."

if __name__ == "__main__":
    file_path = '../dataset/soc-redditHyperlinks-title.tsv'
    result = solve_task_1_1(file_path)
    print(result)

