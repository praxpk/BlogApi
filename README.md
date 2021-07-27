This app requires Flask
Download the files to a folder and run the following command
```
python app.py
```
Open a web browser and connect to local host via port 5000
The api takes 3 parameters
localhost:5000/ping => returns a success:True with 200 response code
localhost:5000/posts?tags=history,tech,health => returns posts with tags of history, health and tech.
localhost:5000/posts?tags=politics,health&sortBy=likes => returns posts with the mentioned tags and sorts them by the number of likes in ascending order
