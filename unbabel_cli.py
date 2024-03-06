import json
import argparse
from datetime import datetime, timedelta

def calculate_moving_average(events, window_size):
    averages = []
    total_duration = 0
    timestamp_format = "%Y-%m-%d %H:%M:%S.%f"

    #Find the first and last timestamp in the events array
    start_time = min(events, key=lambda x: datetime.strptime(x["timestamp"], timestamp_format))["timestamp"]
    end_time = max(events, key=lambda x: datetime.strptime(x["timestamp"], timestamp_format))["timestamp"]

    #Convert timestamps to datetime objects
    start_datetime = datetime.strptime(start_time, timestamp_format)
    end_datetime = datetime.strptime(end_time, timestamp_format)

    #Loop to iterate the range of minutes
    current_datetime = start_datetime
    while current_datetime <= end_datetime + timedelta(minutes=1):
        #Current timestamp. To be shown on the final result
        timestamp_str = current_datetime.strftime("%Y-%m-%d %H:%M:00")

        
        #Determinate current minute
        events_within_window = []
        lower_limit = current_datetime - timedelta(minutes=window_size)
        upper_limit = current_datetime
        
        #Loop to verify if the events are in range of current minute
        for event in events:
            event_timestamp = datetime.strptime(event["timestamp"], timestamp_format)

            #If there is a new event between in the current minute is added
            if lower_limit <= event_timestamp < upper_limit:
                events_within_window.append(event)

        #Calculate moving average for the current minute
        total_duration = sum(event["duration"] for event in events_within_window)

        averages.append({
            "date": timestamp_str,
            "average_delivery_time": total_duration / len(events_within_window) if events_within_window else 0
        })

        current_datetime += timedelta(minutes=1)

    return averages

def main():
    parser = argparse.ArgumentParser(description="Calculate moving average delivery time for translations.")
    parser.add_argument("--input_file", required=True, help="Input file path containing events in JSON format.")
    parser.add_argument("--window_size", type=int, required=True, help="Size of the time window for moving average.")

    args = parser.parse_args()

    with open(args.input_file, "r") as file:
        events = json.load(file)

    moving_averages = calculate_moving_average(events, args.window_size)

    for average in moving_averages:
        print(json.dumps(average))

if __name__ == "__main__":
    main()
