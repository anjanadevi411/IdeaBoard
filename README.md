The idea behind this project is to do brainstorming and Evaluation on different topics and show different ideas about each topic at one place. 
Saving the efforts for meetings needed to brainstorm between team members/employees, so all can go to the app and submit their ideas and see other's 
ideas at one place.
Evaluation of topic what went well, pros and cons faced during the period can be submitted in this application.

INSTALLATION/CONFIGURATION/LAUNCHING INSTRUCTIONS
•	Creating a virtual environment
python3 -m venv environment_name
•	Installing Django in virtual environment
pip3 install django
•	Creating Django project
django-admin startproject projectname
•	For running a server
python3 manage.py runserver
•	For adding a new application
Python3 manage.py startapp appname
•	For creating a database migrations
Python3 manage.py makemigrations
Python3 manage.py migrate


MAIN SYSTEM FUNCTIONS
Navbar Contains
•	Home 
•	Brainstorms
•	Evaluations
Home
Shows the home page with description about idea board, example of brainstorm and evaluation topic.
Brainstorms
•	List form (Already existing topics)
1.	List of all topics will be showed in the form of sticky notes.
2.	Click to specific topic for details.
3.	Buttons provided to contribute more ideas and download in the pdf format.
•	Creating new topic
•	Adding new ideas to the existing topics
•	Search existing topics
Showing the topic and ideas on the front page (sample model of one brainstorm).

Evaluations
•	List form (Already existing evaluation topics)
1.	Link to specific topics for details
2.	Buttons for contributing pros and cons to specific topics or else download in the pdf format. 
•	Creating Evaluation Topic
•	Search Evaluation Topics
Showing the evaluation topic on the front page (sample model of one brainstorm).

TECHNOLOGIES USED
•	Backend Technologies – Django Framework
•	Frontend Technologies – HTML, CSS, Bootstrap
•	Deployment - Heroku

TESTS
•	 Unit testing for urls, views, models, forms in the app.
DEPLOYMENT
•	Deployed the project Idea Board to Heroku and can be accessed by this link
https://ideaboards.herokuapp.com/







