#!/usr/bin/python
import sys, getopt
import time
import pandas as pd
import datetime

def main(argv):
   dbname = 'retail1'
   inputfile = 'data.csv'
   outputfile = 'import.txt'

   usage = 'csv2line.py -d <dbname> -i <inputfile> -o <outputfile>'
   try:
      opts, args = getopt.getopt(argv,"hd:i:o:",["db=","ifile=","ofile="])
   except getopt.GetoptError:
      print (usage)
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print (usage)
         sys.exit()
      elif opt in ("-d", "--db"):
         dbname = arg
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg

   convert(dbname, inputfile, outputfile)


def convert(dbname, inputfile, outputfile):
    # Convert csv's to line protocol
    '''
    https://docs.influxdata.com/influxdb/v1.6/write_protocols/line_protocol_tutorial/
    weather,location=us-midwest temperature=82 1465839830100400200
      |    -------------------- --------------  |
      |             |             |             |
      |             |             |             |
    +-----------+--------+-+---------+-+---------+
    |measurement|,tag_set| |field_set| |timestamp|
    +-----------+--------+-+---------+-+---------+
    '''
    start_time = time.time()


    df_full = pd.read_csv(inputfile)
    df_full["measurement"] = ['transaction' for t in range(len(df_full))]
    lines = [str(df_full["measurement"][d])
             + ",brand=" + str(df_full["brand"][d])
             + " "
             + "model=\"" + str(df_full["model"][d]) + "\","
             + "quantity=" + str(df_full["quantity"][d]) + ","
             + "price=" + str(df_full["price"][d]) + ","
             + "store=\"" + str(df_full["store"][d]) + "\","
             + "area=\"" + str(df_full["area"][d]) + "\","
             + "username=\"" + str(df_full["username"][d]) + "\","
             + "user_age=" + str(df_full["user_age"][d]) + ","
             + "user_gender=\"" + str(df_full["user_gender"][d]) + "\""
             + " "
             + str(int(datetime.datetime.strptime(df_full["created_at"][d], "%Y-%m-%d %H:%M:%S").timestamp())*1000000000)
             for d in range(len(df_full))]

    # Export to file
    theImportFile = open(outputfile, 'w')
    # Write header file
    theImportFile.write('''
# DDL
CREATE DATABASE %s

# DML
# CONTEXT-DATABASE: %s

''' % (dbname, dbname))

    # Write data
    for item in lines:
        theImportFile.write("%s\n" % item)

    # Print log
    print ('---Converting finished !!! (%s seconds)---' % (time.time() - start_time))
    print ('\t-Dabase name is: %s' % dbname)
    print ('\t-Input file is: %s' % inputfile)
    print ('\t-Output file is: %s' % outputfile)

if __name__ == "__main__":
   main(sys.argv[1:])

