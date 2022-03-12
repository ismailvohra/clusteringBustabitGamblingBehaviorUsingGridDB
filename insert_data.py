import griddb_python as griddb
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans


factory = griddb.StoreFactory.get_instance()

argv = sys.argv

try:
    
    #Reading csv file
    data= pd.read_csv("bustabit.csv")
    
    
    #preprocessing
    
    data = data.drop(["Id"], axis = 1)
    
    
    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)
    data.index.name = 'ID'
    
    data['Year'] = pd.DatetimeIndex(data['PlayDate']).year
    data = data.drop('PlayDate', axis = 1)
    
    data = data.assign(CashedOut = np.where((data['CashedOut'].isnull()),data['BustedAt'] + .01, data['CashedOut']))
    data = data.assign(Profit = np.where((data['Profit'].isnull()), 0 , data['Profit']))
    data = data.assign(Profit = np.where((data['Bonus'].isnull()), 0 , data['Bonus']))

    
    #save it into csv
    data.to_csv("preprocessed.csv")
    
    #read the cleaned data from csv
    data_processed = pd.read_csv("preprocessed.csv")

    for row in data_processed.itertuples(index=False):
            print(f"{row}")

    # View the structure of the data frames
    data_processed.info()

    # Provide the necessary arguments
    gridstore = factory.get_store(
        host=argv[1], 
        port=int(argv[2]), 
        cluster_name=argv[3], 
        username=argv[4], 
        password=argv[5]
    )

    #Create container 
    data_container = "data_container"

    # Create containerInfo
    data_containerInfo = griddb.ContainerInfo(data_container,
                    [["ID", griddb.Type.FLOAT],
        		    ["GameID", griddb.Type.FLOAT],
         		    ["Username", griddb.Type.STRING],
                    ["Bet", griddb.Type.FLOAT],
                    ["CashedOut", griddb.Type.FLOAT],
         		    ["Bonus", griddb.Type.FLOAT],
                    ["Profit", griddb.Type.FLOAT],
                    ["BustedAt", griddb.Type.FLOAT],
                    ["Year", griddb.Type.INTEGER]],
                    griddb.ContainerType.COLLECTION, True)
    
    data_columns = gridstore.put_container(data_containerInfo)

    print("container created and columns added")
    
    
    # Put rows
    data_columns.put_rows(data_processed)
    
    print("Data Inserted using the DataFrame")

except griddb.GSException as e:
    print(e)
    for i in range(e.get_error_stack_size()):
        print(e)
        # print("[", i, "]")
        # print(e.get_error_code(i))
        # print(e.get_location(i))
        print(e.get_message(i))
