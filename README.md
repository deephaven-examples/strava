# strava

This example is meant to work alongside your Deephaven IDE. Please see our [QuickStart Guide]](https://deephaven.io/core/docs/tutorials/quickstart/). 

Maybe you're training for a race or simply maintaining an exercise routine. Personally, I consistently use my fitness watch to ensure I'm meeting my step goals and to track my progress as I try to shave a few seconds off my mile time. The free [Strava](https://www.strava.com) app beloved by runners and cyclists is another great resource to motivate you in your fitness journey and connect with a community. You can track a variety of exercises and store your results in the app. Did you know you can also download this data as .fit files?

We walk you through (pun intended!) downloading your Strava data and importing it into Deephaven Community Core, where you can get an overview of your performance and even use this information to adjust your routine for more health benefits.

## Grab your data

I'm a big fan of being able to analyze my data, and I'd rather have the tools to do so on my own when possible. Whether you use Strava's free app or upgrade to their Summit version, you can import your fitness data into Deephaven and access a powerful suite of data analysis options.

To follow along, make sure you've got Deephaven up and running. See our [Quickstart](/core/docs/tutorials/quickstart/#set-up-your-deephaven-deployment) if you're a new user.

First, pull your own data from your [Strava](https://www.strava.com/) account. 

1. Login to your Strava account.
2. Select an activity.
3. At the bottom of the menu, select **...** for more.
4. Select **Export Original**. Provided you have supplied the data in FIT format, this should now provide a file to download with the `.fit` extension.
5. Put this `.fit` file in the data folder underneath your Docker starting location. You might also want to create a new folder to organize the data. Ours is in `data/Fit`.

## Import your data


@dtcooper wrote a really cool Python script to read the FIT binary file format. To install that script, run this code inside the IDE:

```python
import os
os.system("pip install fitparse")
```

To read the FIT file into Deephaven, specify the file path, making sure to include any intermediate directory if you have them. Our example file is called `ThursMorn.fit`.

```python
from fitparse import FitFile

fitfile = FitFile('/data/Fit/ThursMorn.fit')
```

Like most data work, the hard part is cleaning and formatting the data. At the time of writing, this FIT file worked, but in the event Strava alters the format, I left comments on my debugging so you can see how you might want to change things if and when Strava makes changes. I put the rest of the script below to copy and paste into your IDE.


```python
from deephaven.time import to_datetime
from deephaven import DynamicTableWriter
import deephaven.dtypes as dht 
# Ensure fitparse is installed.
import os
try:
    from fitparse import FitFile
except ImportError:
    os.system("pip install fitparse")
    from fitparse import FitFile

# Change to the name of the downloaded file (including any intermediate directory added to docker)
fitfile = FitFile('/data/Fit/ThursMorn.fit')

# See the size of your file
records = list(fitfile.get_messages('record'))
print("Number of data points: {}".format(len(records)))

# Setup deephaven tables to hold results
# Heart rate
columns = {"Timestamp":dht.DateTime, "HeartRate":dht.int_}

hr_table_writer = DynamicTableWriter(columns)
heart_rate_data = hr_table_writer.table
# Gps data
column_gps = {"Timestamp":dht.DateTime, "EnhancedAltitude":dht.double, "EnhancedSpeed":dht.double, "GPSAccuracy":dht.int_, "PositionLat":dht.int_, "PositionLong"dht.int_, "Speed"dht.double}
gps_table_writer = DynamicTableWriter(column_gps)
gps_data = gps_table_writer.table

# Set timezone based on preferences. Fit data may not include timezone
timezone = "MT"
timezone = " " + timezone # Ensure there is a blank space before timezone for later parsing.

# Process in smaller batches first, until you are happy with the results you are working with
counter = 20
counter = len(records) + 1

## Debug your files by looking at individual records at a time.
# record = records[0]
# for field in record:
#     print (field.name, field.value, field.units)
#
## In my example
## records[1] is an example of enhanced gps
## records[3] is an example of heart rate
## records[0] is an example of step counter (guessing)

# Get all data messages that are of type record
for record in fitfile.get_messages('record'):
    mode="None"

    if (counter > 0):
        counter -= 1
    else:
        break

    for field in record:
        if field.name.startswith('heart_rate'):
            mode="hr"
        if field.name.startswith('enhanced'):
            mode="gps"
        # Other types can be added, following a similar pattern.

    # Go through all the data entries in this record
    items=list(record)
    if (mode == "hr"):
        raw_heart_rate = str(items[0]).split()[1]
        final_heart_rate = int(raw_heart_rate)
        raw_time = str(items[1]).split()[1]
        final_time = to_datetime(raw_time.replace(" ", "T") + timezone)
        hr_table_writer.write_data(final_time, final_heart_rate)

    if (mode == "gps"):
        raw_time = str(items[6])[11:30]
        final_time = to_datetime(raw_time.replace(" ", "T") + timezone)

        final_altitude = float(str(items[0]).split()[1])
        final_enh_speed = float(str(items[1]).split()[1])
        final_pos_lat = int(str(items[3]).split()[1])
        final_pos_long = int(str(items[4]).split()[1])
        final_speed = float(str(items[5]).split()[1])

        raw_gps_acc = str(items[2]).split()[1]
        # If preferred, the col type for GPS could be set as String, then further processing done even when value is None
        if raw_gps_acc != "None":
            final_gps_acc = int(str(items[2]).split()[1])
            gps_table_writer.write_data(final_time, final_altitude, final_enh_speed, final_gps_acc, final_pos_lat, final_pos_long, final_speed)
```


It's useful to sort the data in descending time, like below:

```python
gps_data = gps_data.sort_descending(["Timestamp"])

heart_rate_data = heart_rate_data.sort_descending(["Timestamp"])
```

![img](Fit/heartRateTable.png)


note:
Your mileage may vary if using a `.fit` file which reports different data types. Different sensors can report different data. In the example here, both GPS and heart rate monitor data is intertwined.



Now that is being a [Strava](https://www.strava.com/) Power User!

## Extra credit

Some of the most interesting use cases for this data are to correlate the data with other sources of interest to you.

The first step is importing many `.fit` files to compare:

- Today's heart rate with last month's heart rate.
- Average heart rate last week/month.
- Heart rate at different points during the day (morning, lunch, bedtime).
- Correlate live heart rate data with past heart rate data from your `.fit` files: see our [`tickingHeartRate`](https://github.com/deephaven/examples/tree/main/TickingHeartRate) example data for ideas on getting started with live heart rate data.

For more insight, correlate this data with:

- diet macronutrients - do you run faster when you have more protein?
- sleep patterns - is heart rate affected by your amount of sleep?
- weather - temperature, wind chill, humidity, etc.
- health improvements - do you see positive gains in heart health over time?
