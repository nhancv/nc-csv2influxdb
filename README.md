# nc-csv2influxdb
Convert CSV to Line protocol for InfluxDb

Required: 
- Python 3
- pandas `pip install pandas`


Usage

Generate `import.txt` file:

```
python csv2line.py -d <dbname> -i <inputfile> -o <outputfile>

ex:
python csv2line.py -d retail1 -i data.csv -o import.txt
```

Import to InfluxDB

```
influx -import -path=./import.txt -precision=ns
```

Verify
```
$influx
> use retail1
> precision rfc3339
> select * from price limit 3
```

Delete all measurement
```
> drop series from /.*/
```

---------
## NOTE

### Line protocol
https://docs.influxdata.com/influxdb/v1.6/write_protocols/line_protocol_tutorial/
```
weather,location=us-midwest temperature=82 1465839830100400200
  |    -------------------- --------------  |
  |             |             |             |
  |             |             |             |
+-----------+--------+-+---------+-+---------+
|measurement|,tag_set| |field_set| |timestamp|
+-----------+--------+-+---------+-+---------+
```

With tag_set value doesn't have double quote ("), but with field_set value must have double quote for string.

Ex:
```
weather,location=us-midwest temp_str="too hot",out=false 1465839830100400201
```








