# implement all kinds of ingestion
# implement csv, json, parquet, fixed width
# configs to read the file would be sent from the notebook as parameter and not stored in any of the files eg: reader.readcsv(filepath,config)
#would call unzipper to unzip the file if it is zipped (common function for all files)