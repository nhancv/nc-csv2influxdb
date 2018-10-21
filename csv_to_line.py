import pandas as pd
import datetime

# Convert csv's to line protocol

df_full = pd.read_csv("data.csv")
df_full["measurement"] = ['price' for t in range(len(df_full))]
lines = [str(df_full["measurement"][d])
         + ",type=transaction"
         + " "
         + "brand=" + str(df_full["brand"][d]) + ","
         + "model=" + str(df_full["model"][d]) + ","
         + "quantity=" + str(df_full["quantity"][d]) + ","
         + "price=" + str(df_full["price"][d]) + ","
         + "store=" + str(df_full["store"][d]) + ","
         + "area=" + str(df_full["area"][d]) + ","
         + "username=" + str(df_full["username"][d]) + ","
         + "user_age=" + str(df_full["user_age"][d]) + ","
         + "user_gender=" + str(df_full["user_gender"][d])
         + " "
         + str(int(datetime.datetime.strptime(df_full["created_at"][d], "%Y-%m-%d %H:%M:%S").timestamp())*1000000000)
         for d in range(len(df_full))]


theImportFile = open('import.txt', 'w')
dbName = "retail1"

# Write header file
theImportFile.write('''
# DDL
CREATE DATABASE %s

# DML
# CONTEXT-DATABASE: %s

''' % (dbName, dbName))

# Write data
for item in lines:
    theImportFile.write("%s\n" % item)
