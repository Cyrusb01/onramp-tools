

```
Folder PATH listing for volume Local Disk

�   .gitignore
�   alembic.ini           # Creates Database, must enter correct link though that relates to DB 
�   Procfile
�   README.md
�   requirements.txt
�   runtime.txt
�   wsgi.py               # RUN THIS TO RUN APP 
�   
����alembic             #Helps to set up DB 
�   �   env.py
�   �   README
�   �   script.py.mako
�   �   
�   ����versions
�   �   �   82e085f67433_test.py
�            
����datafiles           #Full of CSVs, I think when we populate DB we also update them, not sure why
�       
����tools_app           #Tools_app folder contains the flask app 
�   �   routes.py         #Flask Routes to markets page etc
�   �   __init__.py
�   �   
�   ����assets          #PLotly Dash CSS 
�   �       001_roboto.css
�   �       002_bootstrap-4.4.1.css
�   �       003_corporate-style.css
�   �       favicon.ico
�   �       onramp-logo-small.png
�   �       
�   ����plotlydash                   #This folder contains the Plotly Dash App 
�   �   �   alembic.ini                 #Dont think this needs to be here since its in the main directory 
�   �   �   bt_algos.py                  #Contains homemade BT algos for the strategies 
�   �   �   callbacks.py                 # All the callbacks for the pages 
�   �   �   compute_slider_data.py       # Does Automatic Calculations for slider page, but is not being used yet, needs to be integrated with the DB first 
�   �   �   db_to_csv_transformer.py     # This creates all the getter functions to get data from DB 
�   �   �   formatting.py                # Contains graphing templates and styling for graphs 
�   �   �   helpers.py                   # Contains functions to graph charts and tables 
�   �   �   index.py                     # This is the file that sets up the dash app 
�   �   �   layouts.py                   # Contains all the layotus, mostly in dash bootstrap for now 
�   �   �   
�   �   ����alembic   #Think this folder can be removed too since its in the main directory 
�   �   �   �   env.py
�   �   �   �   README
�   �   �   �   script.py.mako
�   �   �   �   
�   �   �   ����versions
�   �   �   �       82e085f67433_test.py
�   �   �           
�   �   ����cron_db                   #These scripts fetch data from api and store in DB, not yet set up on Cron job, have just been running them manually 
�   �   �       get_historic_data.py
�   �   �       load_and_store_stock_data.py
�   �   �       
�   �   ����models                   # Models folder for the tables in the DB, Session Context is the file that opens the connection to DB 
�   �   �       close_data.py
�   �   �       cryptocurrency_pair_ohlcv.py
�   �   �       session_context.py
�   �           
�   ����static                        # CSS for Flask Pages 
�   �       style.css
�   �       
�   ����templates                     # HTML Pages for new flask stuff, niether of these tempalates are finished or look good yet
�   �       cryptoheat.html
�   �       markets.html
   
```


This app is hosted on heroku, with a $50 paid heroku DB. 

For Local Use
 Create local DB called onramp_research
 Take the link from your DB and put it into the alembic.ini 
 Take the link and store it as a an env variable DATABASE_URL, instead of "postgresql://" at the begining of your link, only do "postgres://" for env variable
 Run alembic upgrade head to create all the tables 
 Run the two scripts in the cron_db folder to populate the tables in the DB 
 Run wsgi.py to see the app 
 
 
 
NEEDS TO BE DONE 
    Cron job on heroku to automatically update data 
    Create new table and fetcher for slider data 
    Speed up pages 
    Light Mode switch 
    print the dashboard as a report 
    
    
 Long Term the app is going to possibly be converted fully into flask, which would require all dash layuouts to go into html and then new callbacks.  
 
