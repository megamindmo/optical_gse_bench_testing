import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from flightsql import FlightSQLClient

token = 'MDbet2Kz0OrFJQX0r4k_WOOu4IbftBamqmxXKKTRDysqFSKK9bxOU6cbPJgvuilk_IW1nXuzr9U_cjp9burtTw=='
org = "mo"
url = "https://us-east-1-1.aws.cloud2.influxdata.com"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
bucket="quad_live"

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

def construct_point_fields(point,fields,data):
    for i in range(len(fields)):
        point.field(fields[i],data[fields[i]])
    return point
def construct_point_tags(point,tags,data):
    print('infunc',tags)
    for i in range(len(tags)):
        print(tags[i],data[tags[i]])
        point.tag(tags[i],data[tags[i]])
    return point

def write_db(data,measurement="TEST",fields=["ch1","ch2","ch3","ch4"],tags=[]):
    print(fields)
    print(tags)
    for key in data:
        point = construct_point_fields(Point(measurement),fields,data[key])
        point = construct_point_tags(point,tags,data[key])
        point = (point)
        write_api.write(bucket=bucket, org=org, record=point)
    print("Complete. Return to the InfluxDB UI.")

def read_all(measurement):
    query = """SELECT *
    FROM '{}'
    WHERE time >= now() - interval '24 hours'""".format(measurement)

    # Define the query client
    query_client = FlightSQLClient(
    host = "us-east-1-1.aws.cloud2.influxdata.com",
    #token = os.environ.get("INFLUXDB_TOKEN"),
    metadata={"bucket-name": bucket})

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