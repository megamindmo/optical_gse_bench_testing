import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from flightsql import FlightSQLClient

token = os.environ.get("INFLUXDB_TOKEN")
org = "mo"
url = "https://us-east-1-1.aws.cloud2.influxdata.com"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
bucket="quadcell_live_test"

# Define the write api
write_api = write_client.write_api(write_options=SYNCHRONOUS)

data = {
  "point1": {
    "ch1": 100,
    "ch2": 1,
    "ch3": 23,
    "ch4": 23,
  },
  "point2": {
    "ch1": 10000,
    "ch2": 1,
    "ch3": 23,
    "ch4": 23,
  },
  "point3": {
    "ch1": 100,
    "ch2": 1,
    "ch3": 23,
    "ch4": 23,
  },
  

}

def construct_point(point,fields,data):
    for i in range(len(fields)):
        point.field(fields[i],data[fields[i]])
    return point

def write_db(data,measurement="TEST",fields=["ch1","ch2","ch3","ch4"]):
    for key in data:
        point = (construct_point(Point(measurement),fields,data[key]))
        write_api.write(bucket=bucket, org=org, record=point)
    print("Complete. Return to the InfluxDB UI.")

def read_all(measurement):
    query = """SELECT *
    FROM '{}'
    WHERE time >= now() - interval '24 hours'""".format(measurement)

    # Define the query client
    query_client = FlightSQLClient(
    host = "us-east-1-1.aws.cloud2.influxdata.com",
    token = os.environ.get("INFLUXDB_TOKEN"),
    metadata={"bucket-name": "quadcell"})

    # Execute the query
    info = query_client.execute(query)
    reader = query_client.do_get(info.endpoints[0].ticket)

    # Convert to dataframe
    data = reader.read_all()
    df = data.to_pandas().sort_values(by="time")
    print(df)

if __name__=="__main__":
    write_db(data,measurement='final')
    read_all('final')