# Finishers

## Data-centric Development Milestone Project

<hr>

Welcome to Finishers. 

This is a web app that contains user-generated workouts or "Finishers", which are intended to be used at the end of a training session to finish off a trainee.

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
2. Browse page
3. Create page
4. Individual finisher page

### Surface

A bright colour scheme gives some visual interest to the simple design, and Materialize CSS cards are used to display individual finishers

<hr>

## Current Features

1. A user login system - all functionality is login-protected
2. Users can create finishers, update and duplicate finishers, delete their own finishers and browse a user-generated library
3. Users can review finishers and up or downvote them. The votes and reviews are displayed on the individual finisher page
4. Admin user can add exercises to the exercise collection in the MongoDB database, which is used to autocomplete fields on the add finisher form
5. Users can star finishers by other users. These then appear on a user's dashboard and can be removed from their library
6. Finishers can be browsed by category or searched for by exercise name

## Future Features

1. User profile pages, allowing a user to see all finishers created by that user
2. More categories can be added by Admin users, and tweaks in the structure of the browse page to allow for more categories
3. Further functionality for user profiles, such as being able to update passwords 
4. Incorporation of images to help add visual interest
5. The admin user cannot currently delete exercises or finishers from the database, this will be updated in the future to give them more control

<hr>

## Data structures

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

This very simple struture is dictated by the data structure that Materialize autocomplete fields expect. The null value could be linked to a thumbnail image of the exercise being selected, but left as null means there is no image linked on the frontend.

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





























