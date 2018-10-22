#!/usr/bin/python
import sys, getopt
import progressbar
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
  
  # Read csv
  bar = progressbar.ProgressBar(maxval=100, widgets=[progressbar.Bar('=', '[', ']'), 'Read csv file ', progressbar.Percentage()])
  bar.start()
  df_full = pd.read_csv(inputfile)
  bar.finish()

  # Measurement
  bar = progressbar.ProgressBar(maxval=len(df_full), widgets=[progressbar.Bar('=', '[', ']'), 'Measurement ', progressbar.Percentage()])
  bar.start()

  measurement = []
  for t in range(len(df_full)):
    measurement.append('transaction')
    bar.update(t+1)
  df_full["measurement"] = measurement
  bar.finish()


  # Processing
  bar = progressbar.ProgressBar(maxval=len(df_full), widgets=[progressbar.Bar('=', '[', ']'), 'Processing ', progressbar.Percentage()])
  bar.start()

  # Export to file
  theImportFile = open(outputfile, 'w')
  # Write header file
  theImportFile.write('''
# DDL
CREATE DATABASE %s

# DML
# CONTEXT-DATABASE: %s

''' % (dbname, dbname))

  lines = []
  for d in range(len(df_full)): 
    item = str(df_full["measurement"][d]) \
           + ",brand=" + str(df_full["brand"][d]).replace(" ", "_") \
           + ",model=" + str(df_full["model"][d]).replace(" ", "_") \
           + ",area=" + str(df_full["area"][d]).replace(" ", "_") \
           + ",user_name=" + str(df_full["user_name"][d]).replace(" ", "_") \
           + ",user_gender=" + str(df_full["user_gender"][d]).replace(" ", "_") \
           + " " \
           + "quantity=" + str(df_full["quantity"][d]) \
           + ",store=" + str(df_full["store"][d]) \
           + ",price=" + str(df_full["price"][d]) \
           + ",user_age=" + str(df_full["user_age"][d]) \
           + " " \
           + str(df_full["time"][d])

    if item not in lines:
      lines.append(item)
      theImportFile.write("%s\n" % item)
    bar.update(d+1)

  bar.finish()

  # Print log
  print ('---Converting finished !!! (%s seconds)---' % (time.time() - start_time))
  print ('\t-Dabase name is: %s' % dbname)
  print ('\t-Input file is: %s' % inputfile)
  print ('\t-Output file is: %s' % outputfile)

if __name__ == "__main__":
   main(sys.argv[1:])

