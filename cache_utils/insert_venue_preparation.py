import os

import redis
import csv

# Connect to the Redis server
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", "6379"))
r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

# Path to venue_preparation CSV file
csv_file_path = "./venue_preparation.csv"


def insert_venue_preparation_to_redis(venue_id: str, avg_preparation_time: float):
    """
    Insert average preparation time to redis based on the venue id
    :param venue_id:
    :param avg_preparation_time:
    """
    r.set(venue_id, avg_preparation_time)


# Open the CSV file
with open(csv_file_path, 'r', newline='') as csvfile:
    # Create a csv.DictReader object
    csv_reader = csv.DictReader(csvfile)

    # Enumerate over the reader to get the row along with a row number
    for row_num, row in enumerate(csv_reader, start=1):
        # Insert the avg preparation time for each venue into Redis
        insert_venue_preparation_to_redis(row["venue_id"], row["avg_preparation_time"])
        print(f"Inserted row {row_num} into Redis")

print("All data has been inserted into Redis.")
