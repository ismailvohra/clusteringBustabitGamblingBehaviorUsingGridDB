# Clustering Bustabit Gambling Behavior Using GridDB
**Introduction:**

Understanding human behavior can be a tricky and attention-demanding task. It is not easy or simple to explain how people would act in a certain situation or how they make certain decisions. But observing people and trying to predict what they will do next can provide a real learning experience. It can help us to make an informed decision for better chances of a positive outcome.

One such situation where predicting human nature can be beneficial for observers is gambling. For instance, a game of poker - understanding why players raise, call, and fold in various situations can provide a distinct advantage competitively. In this project, we are going to use **Bustabit** data, an online platform for gamblers.

Rules for the game are as follows:

1. You can **&#39;Bet&#39;** any amount in Bits, that is 1 millionth of a bitcoin
2. You can win if you cash out before the game busts
3. Your win calculated at the cash out according to the multiplier value at that moment
4. A percentage of **&#39;Bonus&#39;** per game is applied to your bet and summed to give your final winning or **&#39;Profit&#39;** in a winning game

We will be using GridDB to store our large amount of data, to access the data in real-time with fast processing.

**Exporting and Import dataset using GridDB:**

GridDB is a highly scalable and optimized in-memory No SQL database that allows parallel processing for higher performance and efficiency, especially for time-series databases. We will be using GridDB&#39;s python client, which allows us to connect GridDB to python and import or export data in real-time.

Libraries:

We will be using some python libraries to preprocess and analyze the data visually.

1. Pandas: Vastly used python library, especially when dealing with data frames.
2. Matplotlib: Primary library to present data visually using basic plots
3. Numpy: Library used to make some advanced mathematical calculations
4. Sklearn: Library that contains clustering algorithm that will be used in our project

Preprocessing:

![](RackMultipart20220312-4-1ylzs33_html_c7e811cfb1bfb5a.png)

The dataset is now saved in the form of a data frame into the variable &quot;data&quot;.

To make our analysis more understandable, we will be adjusting a few columns of our dataset. We will be replacing the &#39;ID&#39; column with a new one that acts as a primary key for our database. Also, we would be replacing &#39;PlayDate&#39; with &#39;Year&#39; because our project does not require any further information related to time.

![](RackMultipart20220312-4-1ylzs33_html_8965478c230aa7b3.png)

These are the columns remaining in the data frame that we would be using in our analysis:

1. ID: Primary key for our database
2. GameID: Unique ID associated with the bustabit game
3. Username: Unique name used by the player on bustabit platform
4. Bet - The number of Bits betted by the player in this game
5. CashedOut - The multiplier at which this particular player cashed out
6. Bonus - The bonus reward (in percent) awarded to this player for the game
7. Profit - The amount this player won in the game, including the Bonus
8. BustedAt - The multiplier value at which this game busted
9. Year – The year in which the game was played

Before we export our database to GridDB, we need to deal with the NULL values present in our dataset, as GridDB does not allow null values in its database. We will be replacing the NULL values using the following rules:

1. CashedOut - If the value for &#39;CashedOut&#39; is NA, we will set it to be 0.01 greater than the &#39;BustedAt&#39; value to signify that the user failed to cash out before busting
2. Profit - If the value for Profit is NA, we will set it to be zero to indicate no profit for the player in that game
3. Bonus – If the value for Bonus is NA, we will set it to zero to indicate that there was no bonus for the player in that game.

![](RackMultipart20220312-4-1ylzs33_html_e703918a762dac12.png)

As we have completed the preprocessing of our data, we can now save it on our local drive.

![](RackMultipart20220312-4-1ylzs33_html_65e0b7e9c8f2a8c8.png)

Exporting Dataset into GridDB:

To upload the dataset to GridDB, we would read the CSV file that contains the preprocessed data.

![](RackMultipart20220312-4-1ylzs33_html_4e77074a2154ff28.png)

Now, we will create a GridDB container to pass our database schema to the GridDB to be able to generate the design of the database before inserting the row information. Next, we would insert our data into the GridDB.

![](RackMultipart20220312-4-1ylzs33_html_7879017887a85c7d.png)

We have now successfully exported the dataset to the GridDB platform.

Importing Dataset from GridDB:

To import the dataset from the GridDB platform, we will use TQL, GridDB&#39;s query language similar to SQL. We will create a container and store the fetched data in it.

![](RackMultipart20220312-4-1ylzs33_html_4b55d914e08711b0.png)

The next step would be to extract the rows in order of the column info and save it into a data frame to use for data visualization and analysis.

![](RackMultipart20220312-4-1ylzs33_html_98b6461dd4022da9.png)

We now have our data saved into pandas data frame &quot;data&quot; and can continue to use it for our project.

**Data Analysis:**

We will be using the Kmeans clustering algorithm to cluster the players into five different sets. We will start y introducing three new columns to understand the dataset even better. The new columns are based on the following rules:

1. Losses - If the new value for Profit is zero, we will set this to be the amount the player lost in that game, otherwise we will set it to zero. This value should always be zero or negative
2. GameWon - If the user made a profit in this game, the value should be 1, and 0 otherwise
3. GameLost If the user had a loss in this game, the value should be 1, and 0 otherwise

![](RackMultipart20220312-4-1ylzs33_html_8c138c34436fcf5f.png)

Let&#39;s take a look into some specific rows by filtering out data using conditions:

1. Highest multiplier: Details of the Game and User with highest &#39;BustedAt&#39; value

![](RackMultipart20220312-4-1ylzs33_html_26f8b31e23f6ac81.png)

1. Highest Bet: Details of the Game and User with the highest Bet

![](RackMultipart20220312-4-1ylzs33_html_c104bbb940f74171.png)

1. Highest Profit: Details of the Game and User with the highest Profit

![](RackMultipart20220312-4-1ylzs33_html_dea39704ef2f8acd.png)

Next, we would group the data using &#39;Username&#39; to identify the earnings, winnings, and losses by each user, throughout their gambling history at Bustabit. This would help us identify the gambling habits of each user and better understand of relationship and similarities between groups of players.

![](RackMultipart20220312-4-1ylzs33_html_3a84190b80b8b91e.png)

This is what our data looks like now:

![](RackMultipart20220312-4-1ylzs33_html_3051482a8791fe3e.png)

Before moving unto clusters formation, we would first like to standardize the data across the dataset. This would transform the dataset into a standard measuring unit, making our algorithm more efficient. We will create our standardization function and apply it to every numerical column of our dataset.

![](RackMultipart20220312-4-1ylzs33_html_2b38ade9a4fbdc69.png)

Our last step is to now form clusters of players into five sets using the sklearn library.

![](RackMultipart20220312-4-1ylzs33_html_91f14f0e32be4429.png)

Here is a glimpse of our data divided into five clusters:

![](RackMultipart20220312-4-1ylzs33_html_ef6db9ae7018e097.png)

![](RackMultipart20220312-4-1ylzs33_html_199838c55ed8fbaa.png)

**Conclusion:**

By looking at the final results of our project, we can conclude that most of the players have similar attributes and fall in the same clustering group while there are very few exceptions of players that are different from the standard behavior. All of the analysis was done using the GridDB database at the backend, making the integration seamless and efficient.
