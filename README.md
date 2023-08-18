# shininglegend.github.io
This is Titus Murphy's Final Project for CS-50. 
[Here's a video intro!](https://youtu.be/sRbCkBJYrXc)
[Here's the github!](https://github.com/shininglegend/shininglegend.github.io)
(If any files seem missing, check the github.)

The project is meant to be a mostly developed standalone web page used for clients to journal in and for the admins to be able to respond to the journals. It makes use of the following:
- Python
- HTML/CSS
- SQLite3
(There is a js file, but it's currently unused.)
I also rely heavily on:
- Bootstrap formatting
- Flask for rendering templates and running my server

## Usage:
The site is not meant to allow just anyone to register - users must have a key + email preregistered in the database by an admin before they can register. 
The register page is located at [/register](http://127.0.0.1:5000/register) (details as to why in DESIGN.md)
Here are 2 sample user accounts that have not but will work to register and use to access the logged-in portions. 
(Emails are not currently validated, so don't worry about accessing the emails themselves.) 

*There are also two more in notes.txt that have been registered, if the ones above fail to register.*

Please note that while I often refer to sites by their direct address (like /clients), they should all be accessible via the navbar. 

### Client Account usage
Once logged in, you can use the navbar to navigate between pages. The homepage shows all of your journal entries. You can press the button at the top to make a new entry - this will redirect you to a new journal page (and add that entry to the database.) You can then save your draft as via the buttons at the bottom of the page. Once you are ready to submit, you can also submit it via those buttons.
If you go back to the homepage, you might notice that your new journal has been stored there. If an admin responds to your journal, you will also be able to view the response. The journals each have a "Go to" button which links you to the Journal page. (Please note that the creation time and such is not 100% accurate due to timezones, it is only meant to be approximate.)

### Admin Account usage
Admins have the ability to view other people's submitted journals, in addition to their own. 
The other people's journals are stored in /client-journals. This will be a list - at the top are the ones that have not been responded to (including drafts), then at the bottom are the ones that have been responded to (and the response has been submitted).
If you go to the response page for a journal, a second textbox appears in which you can type up a response to the person. The buttons at the bottom then correspond to the response and not the person's entry. Admins can not edit other people's entry, even if they do so by modifying the html to allow them to, it will not change the database.

Admins also have the ability to view a list of user accounts and add new users. This is via the /clients page. That page will allow them to view all current user accounts and any codes that have been added for unregistered accounts. They can also go to the /add-client page to add new clients, which will then generate and flash them a code. (In the future, this will email that client with an invite to register.)

## Installation: 
Requirements: 
- VS code or other IDE
- Python 3.10.11
- Pip

### Steps:
1) Download and unzip all project files to a new folder. 
2) [Create a new virtual enviroment](https://code.visualstudio.com/docs/python/environments)
3) Activate said virtual enviroment. This varies per OS, check the guide linked above.
4) Run `pip install -r requirements.txt` within the enviroment. 
5) If no errors, run `flask run` (still within the venv) to start the server.
6) Flask should give you a website by which my project ui can be accessed. 