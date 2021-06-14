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


![filestructure](https://user-images.githubusercontent.com/78002577/121939560-c4375c80-cd12-11eb-96c9-9b00568d74f2.PNG)

(This is a picture of the file strcture from above, don't know how to format it properly in the github markdown) 
