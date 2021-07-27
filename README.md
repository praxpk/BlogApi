# Blog API
This app requires Flask

Download the files to a folder and run the following command
```
python app.py
```
Open a web browser and connect to local host via port 5000

The api takes 3 parameters:
* tags
* sortBy 
  - id (default)
  - reads
  - likes
  - popularity
    
* direction (single value)
  - desc
  - asc (default)  

Tags can be multiple values but have to be comma separated

sortBy has to be single value and only those mentioned above.

direction is also single value and only those mentioned above.

>localhost:5000/ping

Returns a success:True with 200 response code
>localhost:5000/posts?tags=history,tech,health

Returns posts with tags of history, health and tech.

>localhost:5000/posts?tags=politics,health&sortBy=likes

Returns posts with the mentioned tags and sorts them by the number of likes in ascending order

>localhost:5000/posts?tags=politics,health&sortBy=reads&direction=desc

Returns posts with the mentioned tags and sorts them by the number of times they were read in descending order.