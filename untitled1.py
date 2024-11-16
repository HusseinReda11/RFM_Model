import pandas as pd
import plotly.graph_objects as gr
from datetime import datetime
import seaborn as sns 
import matplotlib.pyplot as plt
data = pd.read_csv("D:\\AssRFM\\SalesRecords.csv",encoding= 'ISO-8859-1')
df =pd.DataFrame(data)
df.shape  #to know numbers of my rows and columns
df.info()
df= df.dropna(subset=["Order ID"])#we will use order id as uniqe value so we will drop null values
df['Order ID'] = df['Order ID'].astype('int64')  #to make sure its integer not string 
df.duplicated().any()
#it check if there a duplicated rows it give me bool value
#in our model we dont have any suplicated value (false)
#if we have a duplicated row we will write>>>
df.drop_duplicates(inplace=True)
#now we will do a data frame with our uniqe value and th ecountry
filtered_data=df[["Country","Order ID"]].drop_duplicates()
filtered_data.shape
filtered_data.Country.value_counts()[:10].plot(kind='bar')
guiena_data=df[df["Country"]=="Guinea"]
guiena_data.head()
# Convert Order Date to datetime for recency calculation
data['Order Date'] = pd.to_datetime(data['Order Date'], errors='coerce')
# Filter out rows with missing dates if any
data = data.dropna(subset=['Order Date'])
# Choose a reference date for Recency calculation
reference_date = data['Order Date'].max()
#Group by 'Country' or other customer-related identifier if available
# Aggregate to calculate Recency, Frequency, Monetary
rfm_data = data.groupby('Country').agg({
    'Order Date': lambda x: (reference_date - x.max()).days,  # Recency
    'Order ID': 'nunique',                                    # Frequency
    'Total Revenue': 'sum'                                    # Monetary
}).reset_index()
# Rename columns for RFM to get the concept of RFM
rfm_data.rename(columns={
    'Order Date': 'Recency',
    'Order ID': 'Frequency',
    'Total Revenue': 'Monetary'
}, inplace=True)
# display the RFM table
print(rfm_data.head())
# assign quartiles for Recency, assigning lower values to more recent purchases
rfm_data['r_quartile'] = pd.qcut(rfm_data['Recency'], 4, labels=['1', '2', '3', '4'])
# create quartiles for Frequency, assigning higher values to more frequent purchases
rfm_data['f_quartile'] = pd.qcut(rfm_data['Frequency'], 4, labels=['4', '3', '2', '1'])
# Create quartiles for Monetary, assigning higher values to higher spenders
rfm_data['m_quartile'] = pd.qcut(rfm_data['Monetary'], 4, labels=['4', '3', '2', '1'])
# Check the first few rows to confirm the quartile columns
print(rfm_data.head())
# Create an RFM score by concatenating the R, F, and M quartile values as strings
rfm_data["RFM_Score"] = rfm_data.r_quartile.astype(str) + rfm_data.f_quartile.astype(str) + rfm_data.m_quartile.astype(str)
# Display the first few rows of RFM data
print(rfm_data.head())
# Filter for customers with the highest RFM score ('111') and sort by Monetary value in descending order
top_rfm = rfm_data[rfm_data['RFM_Score'] == '111'].sort_values('Monetary', ascending=False)
print(top_rfm.head())