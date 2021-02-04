# Finishers

## Data-centric Development Milestone Project

<hr>

Welcome to Finishers. 

This is a web app that contains user-generated workouts or "Finishers", which are intended to be used at the end of a training session to really push a trainee.

The app was delopyed using Heroku and can be found here: [Finishers](https://the-finisher.herokuapp.com).

The goals of the app are, in no particular order:

- build up a user-generated library of short, intense workouts for people to use in their exercise routines
- allow a user to contribute to the database by adding their own finishers and/or reviewing finishers by others
- create an intuitive interface for users to add a finisher easily
- allow a user to browse the finishers by category, meaning they can quickly find something that appeals to them
- give the user a profile and dashboard page that displays finishers they have authored and ones that they have favourited (starred)

This project is my third milestone project for Code Institute.

<hr>

## User Experience

<hr>

### Strategy

The app is a minimal and simplistic design. This is to ensure that it takes only a single click to begin browsing or creating content.

### Scope

Although the primary reason for this project is for my diploma, the app could easily be a useful tool for personal trainers looking for inspiration, for keen gym goers who want some new workout ideas or for someone to record any new circuit training routines they come up with.

### Structure

The app has a simple structure with only a few views. The design is intended to be intuitive, so very little instruction is needed.

### Skeleton

The app was designed in Balsamiq, a few of the views are shown below:

1. Dashboard 

![Dashboard on desktop](/wireframes/home-desktop.jpg) ![Dashboard on Mobile](/wireframes/home-mobile.jpg)

2. Browse page 

![Browse on desktop](/wireframes/browse-desktop.jpg) ![Browse on mobile](/wireframes/browse-mobile.jpg)

3. Create page 

![Create on desktop](/wireframes/create-desktop.jpg) ![Create on mobile](/wireframes/create-mobile.jpg)

### Surface

A bright colour scheme gives some visual interest to the simple design, and Materialize CSS cards are used to display individual finishers

<hr>

## Current Features

1. A user login system - all functionality is login-protected
2. Users can create finishers, update and duplicate finishers, delete their own finishers and browse a user-generated library
3. Users can review finishers and up or downvote them. The votes and reviews are displayed on the individual finisher page
4. Admin user can add exercises to the exercise collection in the MongoDB database, which is used to autocomplete fields on the add finisher form
5. Users can star finishers by other users. These then appear on a user's dashboard and can also be removed from their dashboard
6. Finishers can be browsed by category or searched for by exercise name

## Future Features

1. User profile pages, allowing a user to see all finishers created by that user
2. More categories can be added by Admin users, and tweaks in the structure of the browse page to allow for more categories
3. Further functionality for user profiles, such as being able to update passwords 
4. Incorporation of images to help add visual interest
5. The admin user cannot currently delete exercises or finishers from the database, this will be updated in the future to give them more control
6. Further tweaks to some of the functionality - for example, when a user clones a finisher it will, in future, also show the original in a link
7. Proper performance of all aspects of the app in horizonal orientation on mobile devices

<hr>

## Data Structures

The app uses four collections in a single MongoDB database/cluster. There is a collection for user profiles to be stored, a collection for individual finishers and collections for categories and exercises.

The **users** collection data structure is as follows:

```javascript
{
    _id: ObjectID("stringofcharacters"),
    username: "string",
    password: "string",
    library: [
        0: ObjectID("stringofcharacters_1"),
        1: ObjectID("stringofcharacters_2"),
        ...
    ],
    is_admin: false
}
```

In each collection, the ```_id``` key and value is automatically created by MongoDB. 

The username and password is user-generated, with the password being hashed on registration. The library array holds the ```_id``` of finishers that a user has starred and is used in their dashboard view to retrieve and display those finishers. The ```is_admin``` key is automatically set to false as a security measure, meaning that the user cannot make any changes to the exercise collection as an admin would be able to.

The **exercises** collection data structure is as follows:

```javascript
{
    _id: ObjectID("stringofcharacters"),
    Exercise name: null
}
```

This very simple struture is dictated by the data structure that Materialize autocomplete fields expect. The null value could be a link to a thumbnail image of the exercise being selected, but left as null means there is no image linked on the frontend.

Here is the structure for the **categories** collection:

```javascript
{
    _id: ObjectID("stringofcharacters"),
    category_name: "string",
    category_description: "string"
}
```

In this collection the value for ```category_name``` is used in the dropdown menu when a user creates a finisher. The ```category_description``` is used with Materialize tooltips to help a new user understand the different categories when browsing all finishers. This collection cannot currently be updated on the front end of the app.

The **finishers** collection required the most complex of the data structures:

```javascript
{
    _id: ObjectID("stringofcharacters"),
    finisher_name: "string",
    category_name: "string",
    // up to 10 exercises can be added to this array
    // set_type is a dropdown menu when inputting a finisher
    exercises: [
        {
            exercise_name: "string",
            set: "integer",
            set_type: "string"
        },
        {
            exercise_name: "string",
            set: "integer",
            set_type: "string"
        },
        ...
    ],
    // time_limit_toggle can be "on" or "off"
    time_limit_toggle: "on",
    time_limit: "integer",
    instructions: "string",
    reviews: [
        {
            review: "string",
            reviewed_by: "string"
        },
        {
            review: "string",
            reviewed_by: "string"
        },
    ],
    // votes are added when reviewing a finisher,
    // a value of 100 means an upvote and 0 means a downvote
    // this is then averaged to give a score on the individual finisher view
    votes: [
        "integer", "integer", ...
    ],
    // this is automatically input by the app.py code
    created_by: "string" 
}
```

This data structure allows for finishers of varying length. The ```time_limit_toggle``` and ```time_limit``` are optional fields when creating a finisher and a minimum of one exercise can be added. 

<hr>

## User Story

The app is aimed squarely at people who love exercise. 

1. On arriving to the landing page, the user is prompted to register
2. On registration the user is logged in and taken to their dashboard, which then prompts them to either create a finisher or browse existing finishers
3. Some users might browse, star and review finishers and not create any, while others might create more than they star or review - as it stands, the app would serve both types of user
4. When logging out, all the views and functions are protected so the user must log in again to use the app

<hr>

## Testing

Throughout the development process, defensive design has been a key consideration. I have, so far, been unable to trigger any errors or unexpected behaviours by using the app normally or by attempting to get around the defensive measures.

The app relies on several third party packages for security, a full list can be found in the requirements.txt file.

Below is a table that details the key defensive design tests performed on the app and their outcomes. 

| Element/function to test | Expected outcome | Result |
| --- | --- | --- |
| Protection of links in navbar | The user should only be able to see a link to register or login if they are not logged in | Passed |
| Protection of all views | If a user is not logged in, an attempt to access a protected view should redirect them to the login page and flash a message prompting them to login | Passed |
| Protection of admin specific view, link and functionality | If a non-admin user attempts to access the view and function that allows the admin user to add exercises to the database, they should be redirected back to their dashboard if logged in, or redirected to the login page if not logged in. Non-admin users cannot see the link to the protected view | Passed |
| Deleted finishers cannot be accessed | If a user tries to go to a url containing the ID of a deleted finisher, a 404 error should be returned | Passed |
| Users can only delete finishers that they have authored | Any attempt by a user to delete a finisher that they have not authored will result in a redirect to the dashboard and a flashed message informing them that they cannot delete that finisher | Passed |

All HTML and CSS was validated on the [W3C Markup Validation service](https://validator.w3.org/). All Python code was checked for syntax on [ExtendsClass](https://extendsclass.com/python-tester.html). javascript code was tested on [Esprima](https://esprima.org/demo/validate.html). No errors were shown in the HTML, CSS, JS or Python code.

The app has been tested on a variety of different devices and browsers. One currently unfixable problem, however, is that I haven't been able to find a solution that locks the website in vertical orientation on mobile devices. It doesn't work properly or look good currently in horizontal orientation - this will be addressed in future updates

1. iPhone XR

    - The app was tested on Safari, Firefox and Chrome and perfomed as intended vertical orientation. 

2. iPad Pro

    - The website was tested on Safari and performed as intended in both orientations

3. 21.5 inch iMac with 1080p display

    - The website performed as intended on Chrome and Safari

4. iPhone 5, 6/7/8, 6/7/8 plus, iPad, various android phones, laptops and a 4K monitor were all simulated in Chrome Developer Tools to check for responsiveness

    - All performed as intended; with simlutated mobile devices working well in vertical orientation

<hr>

## Deployment

The project was created in Gitpod and the repository is stored at Github. If you would like to clone the project to run locally on your machine, please follow the steps below:

1. [Going to the repository on Github](https://github.com/allyporwal/data-centric-development)
2. Clicking on the "Code" button at the top right
3. The link to be copied will then be displayed
4. In your IDE, ensure you are in the correct directory and then type "git clone" followed by pasting the link
5. The repository will then be cloned into your chosen directory.

The project is hosted by [Heroku](https://www.heroku.com), and these are the steps I took to get it running.

1. Logged into Heroku and navigated to my [dashboard](https://dashboard.heroku.com/apps)
2. Clicked on "New" in the top right corner and selected "Create new app"
3. Named the app and selected the correct geographical region
4. Clicked on the "Deploy" tab and selected the Github deployment method
5. Ensured my Heroku and Github accounts were linked
6. Entered the name of my repository into the field, searched for the repository and connected it to the app
7. Clicked on the settings tab and then "Reveal Config Vars"
8. Input the config vars from the ```env.py``` file (IP, PORT, SECRET_KEY, MONGO_URI and MONGO_DBNAME)
9. Navigated back to the "Deploy" tab and clicked "Enable Automatic Deploys" (this was automatically linked to the master branch as it was the only one at the time)
10. Finally, I clicked on "Deploy Branch" and the Heroku app was deployed

The repository contains the ```requirements.txt``` and ```Procfile``` necessary for deployment to Heroku. The terminal command to generate the requirements file was ```$ pip3 freeze --local > requirements.txt``` and the Procfile was created with the command ```echo web: python app.py > Procfile```

If you are going to clone this repository and set up the app hosting with Heroku following the steps above, you will also need an ```env.py``` file. The structure of this file is detailed below:

```python
import os

os.environ.setdefault("IP", "0.0.0.0")
os.environ.setdefault("PORT", "5000")
os.environ.setdefault("SECRET_KEY", "**YOUR SECRET KEY HERE**")
os.environ.setdefault("MONGO_URI", "**YOUR MONGODB URI HERE**")
os.environ.setdefault("MONGO_DBNAME", "**YOUR MONGODB DATABASE NAME HERE**")
```
Your MongoDB databse must be correctly configured as well:

1. Within your cluster, navigate to the "Collections" tab
2. Create a new database named "the_finisher"
3. Create the appropriately named collections (detailed above)
4. Follow the data models above and input some documents to get started
5. On the left of the screen there is a link under the Security section titled "Database Access"
6. Ensure that you have a user created with the ability to read and write to any database
7. Navigate back to the overview of your clusters and click "Connect" on the right of the screen
8. Click "Connect your application" and select the Python driver and correct version
9. Copy the connection string, taking care to update the password and database name
10. Paste this string in the ```env.py``` file in the ```"MONGO_URI"``` section
11. Input your database name in the ```"MONGO_DBNAME"``` section

Your app should now be deployed on Heroku and talking to MongoDB correctly.

You must also ensure that you have all the necessary modules installed in your IDE. This project relies heavily on third party modules for key functionality, and they are all listed below:

1. [Flask](https://flask.palletsprojects.com/en/1.1.x/) is the micro framework the project relies heavily upon - in the terminal use: ```$ pip3 install Flask```
2. [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/index.html) integrates Flask and WTForms - in the terminal use: ```$ pip3 install Flask-WTF```
3. [WTForms](https://wtforms.readthedocs.io/en/2.3.x/) is used in most forms for backend validation - in the terminal use: ```$ pip3 install WTForms```
4. [Flask-Login](https://flask-login.readthedocs.io/en/latest/) is used to manage loggin in and out and to protect views and functions - in the terminal use: ```$ pip3 install flask-login```
5. [Flask-PyMongo](https://flask-pymongo.readthedocs.io/en/latest/) is to integrate Flask and MongoDB - in the terminal use: ```$ pip3 install Flask-PyMongo```
6. [dnspython](https://pypi.org/project/dnspython/) is to enable usage of MongoDB connection string - in the terminal use: ```$ pip3 install dnspython```
7. [Werkzeug](https://werkzeug.palletsprojects.com/en/1.0.x/utils/) is used to debug during development and to generate hashed passwords - it comes as part of Flask so no extra installation commands are necessary

<hr>

## Technologies Used

This project uses the following technologies:

1. HTML and CSS
2. [Jquery](https://jquery.com/) was used to dynamically load forms and hide Flashed messages
3. Javascript was used to fetch data from MongoDB for autocomplete fields in forms and to enable the workings of Materialize components
4. [Materialize CSS](https://materializecss.com/) was used for styling and responsive design
5. [Gitpod](https://www.gitpod.io/) was the IDE used for the project
6. [Balsamiq](https://balsamiq.cloud/) was used to create the basic wireframes
7. [Github](https://www.github.com/) was used for version control
8. [MongoDB](https://www.mongodb.com/) stored all the data generated in the app
9. Python was used to write the app

<hr>

## Attributions and Acknowledgements

Several developers far more talented and experienced than I were vital in helping me get this app working.

- [This thread](https://stackoverflow.com/questions/53401996/attributeerror-dict-object-has-no-attribute-is-active-pymongo-and-flask) on Stack Overflow has an answer from user Vinsce that helped me create my User class and get Flask-Login working correctly. Some of his code for the User class and ```@login_manager.user_loader``` is used in ```app.py```
- The list comprehension code in the ```def add_finisher()``` function as well as the other similar functions was kindly answered in [this thread](https://stackoverflow.com/questions/64822476/how-to-turn-2-d-list-into-a-list-of-dictionaries-in-python) by user Aplet123 when I asked on Stack Overflow
- [Pretty Printed](https://www.youtube.com/channel/UC-QDfvrRIDB6F0bIO4I4HkQ) on Youtube was instrumental in helping me understand backend form validation
- User Furas detailed how to get all data from a form with similar name fields in [this thread](https://stackoverflow.com/questions/58160006/how-to-get-multiple-elements-from-a-form-using-request-form-get) on Stack Overflow
- Materialize tabs weren't working correctly, they weren't displaying more than 4 in a row. [This answer](https://stackoverflow.com/questions/45153376/materializecss-tabs-not-displaying-more-than-4-tabs) on Stack Overflow from user Saurabh Yadav fixed the issue
- [Andrew Healey's](https://healeycodes.com/javascript/python/beginners/webdev/2019/04/11/talking-between-languages.html) work helped me get the Materialize autocomplete working with data from MongoDB and Python
- Materialize Select doesn't work on iOS - [this fix](https://stackoverflow.com/questions/52850091/materialize-select-and-dropdown-touch-event-selecting-wrong-item) by user Akintomiwa Opemipo solved the bug 

Big thank you to my Code Institute mentor, Brian Macharia, for his help in getting this project done. His ability to break anything I build in less than 10 seconds has really helped me learn. Thanks, Brian.
































