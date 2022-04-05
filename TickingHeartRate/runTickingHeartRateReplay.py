from deephaven import read_csv
from deephaven.time import to_datetime, now, plus_period, to_period
from deephaven import DynamicTableWriter
import deephaven.Types as dht
import pathlib
import time
from threading import Thread

# Max number of csv files to pull in
csv_files=500

# Setup deephaven tables to hold heart rate results
column = {"Timestamp":dht.DateTime, "HeartRate":dht.int_}
hr_table_writer = DynamicTableWriter(column)
heart_rate_data = hr_table_writer.table

# Function to log data to the dynamic table
def thread_func():
    for x in range(1, csv_files):
        next_file = ("/data/examples/TickingHeartRate/csv/%d.csv" % x)
        print(next_file)
        path = pathlib.Path(next_file)
        if path.exists() and path.is_file():
            next_hr = read_csv(next_file, headless = True).view(["Timestamp=Column1", "HeartRate=Column2"])
            next_record = next_hr.getRecord(0, "Timestamp", "HeartRate")
            timestamp = next_record[0]
            hr_table_writer.write_row(timestamp, int(next_record[1]))
            time.sleep(1)
        else:
            print("File does not exist: " + next_file)

# Thread to log data to the dynamic table
thread = Thread(target = thread_func)
thread.start()