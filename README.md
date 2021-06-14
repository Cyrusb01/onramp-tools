# onramp-tools

#### FILE STRUCTURE

/Onramp Tools   #Full Repo 
|--/datafiles   #csv files for data
|--/tools-app   #app module 
    |--init.py
    |--routes.py
    |--/assets   #css for plotly dash 
    |--/plotlydash
       |--bt_algos.py   #creates some bt algos 
       |--callbacks.py  #creates all the callback for dash app 
       |--formatting.py #contains the styling templates for graphs 
       |--helpers.py    #contains helper functions for getting data and graphing 
       |--index.py      #initalizes dash apps layouts and callbacks
       |--layouts.py    #contains the layouts for each page 

|--wsgi.py # Runs the app 
