import numpy as np
import griddb_python as griddb
import sys
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


factory = griddb.StoreFactory.get_instance()

argv = sys.argv

try:
    # Get GridStore object
    # Provide the necessary arguments
    gridstore = factory.get_store(
        host=argv[1], 
        port=int(argv[2]), 
        cluster_name=argv[3], 
        username=argv[4], 
        password=argv[5]
    )

    # Define the container names
    data_container = "data_container"

    # Get the containers
    obtained_data = gridstore.get_container(data_container)
    
    # Fetch all rows - language_tag_container
    query = obtained_data.query("select *")
    
    rs = query.fetch(False)
    print(f"{data_container} Data")

    
    # Iterate and create a list
    retrieved_data= []
    while rs.has_next():
        data = rs.next()
        retrieved_data.append(data)

    # Convert the list to a pandas data frame
    data = pd.DataFrame(retrieved_data,
                        columns=['ID', 'GameID',"Username","Bet","CashedOut" ,"Bonus",
                                 "Profit","BustedAt","Year"])

    # Get the data frame details
    print(data)
    data.info()
    
    
except griddb.GSException as e:
    for i in range(e.get_error_stack_size()):
        print("[", i, "]")
        print(e.get_error_code(i))
        print(e.get_location(i))
        print(e.get_message(i))
        
        
    ##Analysis
data = data.assign(Losses = np.where((data['Profit'] == 0 ), -  data['Bet'], 0))
data = data.assign(GameWon = np.where((data['Profit'] == 0 ), 0 , 1))
data = data.assign(GameLost = np.where((data['Profit'] == 0 ), 1, 0))



data.iloc[data['BustedAt'].idxmax()]
data.iloc[data['Bet'].idxmax()]
data.iloc[data['Profit'].idxmax()]


data_groupby = data.groupby('Username').agg({'CashedOut': 'mean',
                                             'Bet': 'mean',
                                             'Profit': 'sum',
                                             'Losses': 'sum',
                                             'GameWon': 'sum',
                                             'GameLost': 'sum'})

print(data_groupby)

def standardization_function(x):
    return (x-np.mean(x)/np.std(x))


bustabit_standardized = data_groupby.apply(lambda x: standardization_function(x) 
                                           if ((x.dtype == float) or (type(x) == int)) 
                                           else x)         

bustabit_standardized.describe()

kmeans = KMeans(n_clusters=5, random_state=0).fit(bustabit_standardized)
clustering_data = pd.DataFrame()  
clustering_data['cluster'] = kmeans.predict(bustabit_standardized)

summary = clustering_data.groupby("cluster").mean()
summary['count'] = clustering_data['cluster'].value_counts()

print(summary['count'])