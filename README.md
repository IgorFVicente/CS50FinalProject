# CS50 FINAL PROJECT - Study Timer Web App

My project is a webpage where you can record the time you spent studying, define a time goal for daily study and manage your records.

The project was made using: HTML, CSS, Javascript and Python (Flask)

The web app doesn't require you to be logged in to use the stopwatch, but you're required to be logged in to record the time, define goals and see how you've doing.

You need to provide a username, email and password to register. All of the fields are validated through both the html required attribute and also through the backend, with a min and max length to both the username and password and requiring the password to have at least a letter and a number.

The database has two tables: 

- The first for the user data, with an unique and auto generated id, unique username, unique email, password (stored after a hash function has been applied to it), the user daily goal of study time, the user current streak (how long the user has satisfied the daily goal), the days the user defined that should be considered study days, the last day he reached the goal, the total time recorded through the app and the longest streak the user has ever reached.

- The second for the study time records, with an unique and auto generated id, the id of the user who saved the record, registers for the date and time the record was made (using timezone) and how many hours, minutes and seconds of study for that record.

The pages are:
The index, were the stopwatch can be started, paused and stopped and where you can save a register of study time (if you are logged in).

The "My history", where you can see all the registers you saved.

The "about" page where there's a little introduction about the meaning of the web app.

The "Sign In" and "Sign Up" pages if you are logged off, for you to register a new account or to login with one you already created (you can login using either your username or e-mail).

The "Account" page where you can change your username, daily goal and also the days that should be counted as study days (if you don't study in a "non-study day" the app won't reset your current streak). You can also acces a page through this one to change your login information, as long as you provide your current password.
