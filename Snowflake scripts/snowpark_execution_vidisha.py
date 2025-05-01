import snowflake.snowpark as snowpark
from snowflake.snowpark.functions import col
import pandas as pd

def main(session: snowpark.Session): 
    # coding inside the main handler 
    tableName = 'RAW_FOOD_DATA' # name the input table containing raw data
    snow_table = session.table(tableName) # load the raw data table into snowpark df
    df=snow_table.to_pandas() # convert snowspark df to pandas df 
    print(df.shape)

    tableName='ROW_COUNT' # name the  table that counts the transformed rwo count 
    row_count_table=session.table(tableName) # load the raw data table to snowspark df
    row_count_df=row_count_table.to_pandas() # converts snowpark df to pandas df

    if row_count_df.shape[0]!=0:  # If there's existing rows in the table 
        # get the index_no of latest row
        row_count_df=row_count_df[row_count_df['INDEX_NO']==max(row_count_df['INDEX_NO'])].reset_index(drop=True)
        old_rows=row_count_df['NO_OF_ROWS'][0] # get the number of old rows in the latest record 
        df=df.sort_values(by="YEAR").reset_index(drop=True) # sort the values by year 
        df1=df.tail(df.shape[0]-old_rows) # get only the new records added since last count 
        #df1=df[(df.shape[0]-old_rows):]
    else:
        df1=df # If there's no existing rows use the entire original df
    
    print(f"shape of the new df:{df1.shape}") 
    print(f"unique dates in the new df :{df1['DATES'].unique()}")

    ### preprocessing data 
    df_notnull=df1.loc[:,df1.notnull().any()] # select all columns that has at least one non null value 
    keep_cols=['COUNTRY','MKT_NAME','DATES'] # keep columns for further processing
    df2=df_notnull[keep_cols+[col for col in df_notnull.columns if col.startswith(
        ('O_', 'H_', 'L_', 'C_', 'INFLATION_', 'TRUST_'))]] # keeping only relevant columns
    #reshaping the df
    final_component_df=df2.melt(id_vars=keep_cols,var_name='ITEM',value_name="VALUE") 
   
    # Split the variable names to get the type of data (open, high, low, close,inflation, trust)
    final_component_df.insert(loc=4,column='TYPE',value=final_component_df['ITEM'].str.split('_').str[0])
    final_component_df['TYPE']=final_component_df['TYPE'].replace({'O':'OPEN', 'H': 'HIGH', 'L': 'LOW', 'C': 'CLOSE'})
    final_component_df['ITEM']=final_component_df['ITEM'].str.split('_').str[1] # extract the item names from ITEM column

    # create a pivot table 
    pivot_df=final_component_df.pivot_table(index=['COUNTRY','MKT_NAME','DATES','ITEM'],columns='TYPE',values='VALUE').reset_index()

    # Check the column names and impute missing cols with zero
    current_cols=pivot_df.columns.tolist() #get the current columns 
    expected_cols=['COUNTRY', 'MKT_NAME', 'DATES', 'ITEM', 'CLOSE', 'HIGH','INFLATION', 'LOW', 'OPEN', 'TRUST']
    add_cols=list(set(expected_cols)-set(current_cols)) # identify missing columns 
    if add_cols:
        for col in add_cols:
            pivot_df[col]=0  # add missing columns and initialize them to zero 
            
   # select the cols for the df,after imputing missing cols with zero
    final_df=pivot_df[expected_cols]

   # cleaned dataframe 
    print(f"shape of the cleaned RAW_FOOD_DATA:{pivot_df.shape}")
    print(f"unique dates in the cleaned RAW_FOOD_DATA:{pivot_df['DATES'].unique()}")

   ## Addinng cols to RAW_COUNT table and saving the table in Snowflake 
    if row_count_df.shape[0]==0:
        d={'INDEX_NO':1,'NO_OF_ROWS':df.shape[0],'DATE':str(pd.Timestamp.now()),'NO_OF_ROWS_ADDED':df.shape[0],
        'NO_OF_ROWS_IN_TRANSFORMED_TABLE':pivot_df.shape[0]}
        session.create_dataframe(pd.DataFrame([d])).write.save_as_table(
            'ROW_COUNT',mode='append',table_type="") # create a spark df from dictionary and save it as a table in snowflake 
    else:
        # If raw_count_df exists, increment the index number and update the count 
        d={'INDEX_NO':row_count_df['INDEX_NO'][0]+1,'NO_OF_ROWS':df.shape[0],'DATE':str(pd.Timestamp.now()),
        'NO_OF_ROWS_ADDED':int(df.shape[0]-old_rows),
        'NO_OF_ROWS_IN_TRANSFORMED_TABLE':pivot_df.shape[0]}
        session.create_dataframe(pd.DataFrame([d])).write.save_as_table(
            'ROW_COUNT',mode='append',table_type="")


    # create snowspark df for final cleaned data 
    snow_df=session.create_dataframe(final_df)

    # save the cleaned data to a table 
    snow_df.write.save_as_table('CLEANED_FOOD_DATA',mode='append')

    return snow_df 


# Connection parameters for Snowflake
connection_parameters = {
"account": "", 
"user": "", 
"password": "",
"role": "ACCOUNTADMIN", 
"warehouse": "COMPUTE_WH", 
"database": "FOOD_DB", 
"schema": "PUBLIC"}
