# MASS DOWNLOAD FROM SCEYE  
qlik sense API reference is available at https://qlik.dev/apis/

>> main.py tries to use JSON API to mass download visualizations from SANOFI's SCEYE APP.
The code works in the following manner:

1. Fetch the doc_list (app_list)
2. Select the app, since we have only one app we choose index as 0
3. Create a session object (I saw Qlik Engine on Dev Hub exhibiting this behavior which is why I executed this step)
4. Get the layout of the app
5. Select the sheet, since we have one sheet we choose index as 0
6. Iterate through the visualizations and print their names
