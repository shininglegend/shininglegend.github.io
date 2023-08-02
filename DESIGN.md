# Scope/ Outcomes reached
This project met all but one of my "Better" outcomes (and tbh that one that I didn't hit should've been under "best" outcome). It also met one of my best outcomes (more secure login/registration), though the other two were not met. 

### Time breakdown
I spent around 22 hours on this project, which equates to about 2.5 psets worth of work for me. 2-3 hours were spent on initial setup (ie: get layout.html the way I wanted, factor out files to /helpers as needed, set up initial database.) I also spent about 1h writing the Readme and Design documents. The rest of the time was spent in coding the project itself. 

## Tools used
I designed this project using python and html because I was pretty decent in python and knew hardly anything about html, so the two balanced each other nicely. I also decided to use flask (Due to having used it before and knowing it would work for this project), plus I wanted to learn more about it - seeing as we only touched on it briefly. I decided to stick with sqlite3 for the implementation for a few reasons, the biggest one being the difficulty that can be encountered when initially setting up a postgresql database, and when transferring a database to another person. 

# Big picture setup:
- App.py is what flask runs. This then imports the helper functions (which define all the routes) for flask as well as the init file (see below). 
- I put the routes and the helpers into their subdirectory to keep my app looking clean. This prevents a huge app.py file and also helps me to find the relevant function very quickly.
- I use templates a LOT. The layout template is heavily modified from finance, but that's where I got a starting point. I also added a bunch of CSS (with the help of our tutor) to improve the looks of this site drastically. 

## Random under-the-hood details
### Registration
Registration was made more secure by adding the need for an admin to generate a code associated with an email address. This prevents users who are not clients from making an account - in order to bypass the system they would need to guess both the 8-digit alphanumeric code and the email associated with it (which seems highly unlikely. I may add ratelimits in the future though.) 
The alphanumeric code uses the secrets library for generation of the code in order to be more secure. The codes are also designed to be unique.

### Journal addresses
I use flask's [Variable Rules](https://flask.palletsprojects.com/en/2.3.x/quickstart/#variable-rules) for my journals and responses. This allows me a much simpler implementation of the responses page and also allows for the url to easily dictate which journal you get back. Only a user can access their own unsubmitted journals.
For making new journals, I have the user visit the /journal page. This page simply adds an entry to the database of journals and then redirects the user to that page. If someone else tries to access a journal that they do not own, they get redirected to this same /journal page, which then makes a new journal for them. Admittedly, this could fill up the database quite quickly, so I may eventually add functionality that only allows 3 drafts and brings them to the top of the list of journals, but that is beyond the scope of this project for now (seeing as journals without content will only "shadowsubmit" - they won't show for admins.). I marked the journal area to be required, but if the user simply navigates away it doesn't delete the journal from the database yet, as it is tough to know when the user has actually left the site and when they simply haven't finished typing. (Perhaps some JS will be helpful here in the future.)

### Contact us page
The contact us page only redirects to our main website - since there is better spam filtering and email monitering there, I prefer to send them there. 

### init file
When putting the functions for the different parts of the site into different files, I ran into the problem of circular dependancies - since the helper files needed the "app" file, and the app.py needed the helper files. So I made an init file that initializes the databases and starts the server properly - and both the helper functions and app.py reference it as needed. 

### Tables.sql 
This is simply meant to keep track of my CREATE TABLE commands - which make it much easier to modify them as needed and to write my queries, since I didn't have to run .schema constantly. Plus it's nicely formatted!