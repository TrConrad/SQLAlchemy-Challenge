This Challenge was an excerise in utilizing SQLAchemy to reflect data from SQLlite and CSV files, as well as to analyze this data. The analyzed data was then reflected into a Flask API, on the local host. Data was pulled from two CSV files and one SQLlite file, filtered through query sessions, then loaded into tables for data vizualization. Several of the queries focused on finding the last recorded data of data entry, which was then used to determine and gather tweleve months of data for analysis, specifically the last year's worth of Data on precipitation and recorded temperatures in Hawaii. This data was then converted into a dataframe, then graphed as a bar chart and histogram respectively. From there, the data was refected into a python file via the Autobases function, and used to create a Flask API with five possible routes. The first listed the preciptation data for each date, the second listed the stations the data was gathered from, and the third listed the temperatures gathered in one year. The fourth and fifth routes both listed the minimum, maximum, and average temperatures within a specific date range. The fourth route only allows for the start date to be set, while the fifth was programmed to allow users to input both a beginning and ending date for a specific date range. 


Citations: 

While websites such as Bing Ai and Slack Overflow were referenced for researching functions and formatting as needed, such as the data formatting for the Precipitation BarChart, no code was directly copied. I did work directly with my instructor and TA, on the use of np.ravel in the Flask API for the second, fourth, and fifth routes during office hours on August 14th, 2023. The Citations are as follows: 

Barnes, B.,  climate_starter.ipynb (Version 1.0) [np.ravel]. August 14th, 2023
Qi, A.,  climate_starter.ipynb (Version 1.0) [np.ravel]. August 14th, 2023
