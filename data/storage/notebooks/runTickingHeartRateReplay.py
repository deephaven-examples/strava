from deephaven.replay import TableReplayer
from deephaven import DynamicTableWriter
from deephaven.time import to_j_instant
from deephaven import dtypes as dht
from deephaven import read_csv
from time import strftime, localtime
from threading import Thread
import pathlib, time

# Max number of csv files to pull in
csv_files = 250

# Setup deephaven tables to hold heart rate results
column = {"Timestamp":dht.Instant, "HeartRate":dht.int_}
hr_table_writer = DynamicTableWriter(column)
heartrate = hr_table_writer.table

# Function to log data to the dynamic table
def thread_func():
    for x in range(1, 250): #, csv_files):
        next_file = ("/data/TickingHeartRate/%d.csv" % x)
        path = pathlib.Path(next_file)
        if path.exists() and path.is_file():
            data = open(next_file, "r").readlines()[0].strip().split(", ")

            timestamp = to_j_instant(strftime('%Y-%m-%dT%H:%M:%S UTC', localtime(int(data[0])/1000)))
            actual_data = int(data[1])

            hr_table_writer.write_row(timestamp, actual_data)
        else:
            print("File does not exist: " + next_file)

# Thread to log data to the dynamic table
thread = Thread(target = thread_func)
thread.start()