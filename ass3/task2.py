import heapq
from datetime import datetime
from collections import defaultdict
import bisect
import pytz
import pandas as pd

class Graph:
    def __init__(self):
        self.nodes = defaultdict(list)  # Each node will have a list of tuples (neighbor, timestamp)

    def add_edge(self, source, target, timestamp, sentiment):
        # Using bisect to maintain a sorted list of tuples by timestamp for each source
        bisect.insort(self.nodes[source], (timestamp, target, sentiment))

    def get_interactions(self, source):
        return self.nodes[source]

def hongkong_time_to_unix_epoch(hk_time_str):
    hk_time = datetime.strptime(hk_time_str, '%Y-%m-%d %H:%M:%S')
    hongkong = pytz.timezone('Asia/Hong_Kong')
    hk_time = hongkong.localize(hk_time)
    unix_epoch = int(hk_time.timestamp())

    return unix_epoch

def unix_epoch_to_hk_time(epoch_time):
    utc_time = datetime.utcfromtimestamp(epoch_time)
    hong_kong = pytz.timezone('Asia/Hong_Kong')
    hk_time = utc_time.replace(tzinfo=pytz.utc).astimezone(hong_kong)
    hk_time_str = hk_time.strftime('%Y-%m-%d %H:%M:%S')

    return hk_time_str

def parse_time(timestr):
    return datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S')

def find_earliest_arrival_path(graph, source, target, start_time):
    # Priority queue, storing tuples of (arrival_time, subreddit, path)
    pq = [(start_time, source, [source])]
    visited = set()

    while pq:
        current_time, current_subreddit, path = heapq.heappop(pq)
        if current_subreddit == target:
            return current_time, path

        if current_subreddit in visited:
            continue

        visited.add(current_subreddit)

        # Iterate through neighbors of the current subreddit
        for interaction_time, neighbor, sentiment in graph.get_interactions(current_subreddit):
            if sentiment != 1: continue
            if neighbor not in visited and interaction_time >= current_time:
                new_time = max(current_time, interaction_time)
                heapq.heappush(pq, (new_time, neighbor, path + [neighbor]))

    return None, []

def initialize_graph(graph, graph_path):

    with open(graph_path, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                source, edges_str = parts
                source_id = int(source)
                edges = edges_str.split(' ')
                for edge in edges:
                    timestamp, target_id, sentiment = map(int, edge.split(','))
                    graph.add_edge(source_id, target_id, timestamp, sentiment)
    return graph


def subreddit_to_identifier(subreddit_name, dict_df):
    match = dict_df[dict_df['subreddit'] == subreddit_name]
    if not match.empty:
        return int(match['identifier'].values[0])
    else:
        return None
def identifier_to_subreddit(identifier, dict_df):
    match = dict_df[dict_df['identifier'] == identifier]
    if not match.empty:
        return str(match['subreddit'].values[0])
    else:
        return None

if __name__ == "__main__":
    file_path = 'graph.tsv'
    graph = Graph()
    dict_df = pd.read_csv('dict.tsv', sep='\t', header=None, names=['identifier', 'subreddit'])

    # Initialize the graph with the data from file_path
    # Note: you will need to implement the initialize_graph function according to your graph structure.
    graph = initialize_graph(graph, file_path)

    while True:
        input_str = input("Enter source, target and start time (or type 'exit' to quit): ")
        if input_str.lower() == 'exit':
            break

        try:
            source, target, start_time_str1, start_time_str2= input_str.split()
            start_time_str = start_time_str1 + ' ' + start_time_str2

            start_time = hongkong_time_to_unix_epoch(start_time_str)

            source_id = subreddit_to_identifier(source, dict_df)
            target_id = subreddit_to_identifier(target, dict_df)

            if source_id is None or target_id is None:
                print("Invalid source or target subreddit.")
                continue

            arrival_time, path = find_earliest_arrival_path(graph, source_id, target_id, start_time)
            if arrival_time:
                arrival_time_str = unix_epoch_to_hk_time(arrival_time)
                print(f"Arrival time: {arrival_time_str}")
                path_subreddits = [identifier_to_subreddit(i, dict_df) for i in path]
                print(f"Path: {' -> '.join(path_subreddits)}")
            else:
                print("No path found")
        except ValueError:
            print("Invalid input format. Please enter source, target, and start time separated by spaces.")