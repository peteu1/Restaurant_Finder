# Restaurant_Finder
Web application using the Yelp API to help find good restaurants. This is for the Capital One challenge (https://www.mindsumo.com/contests/d052bcf8-4580-4922-95ef-a9f6ceaf0f10).

Link to page: https://restaurant-finder-peteu.herokuapp.com/


> Development:

Issues:
1. Checkboxes do not work properly.
	HTML code: templates/partials/filters.html  [class='ck-button']<br/>
	CSS code: static/css/app.css  [Lines 81-119]<br/>
		> This styles the checkboxes how I'd like, but they are not actually toggling "checked" (probably because I have an onclick() call in the <input> tags in filters.html)<br/>
	JS code: templates/app.html  [<script> tags at top]<br/>
		> I've tried a ton of things (much of it commented out)  
		> I can't get:<br/>
			- a callback to Python [home.py/background_process()] while having the ""check boxes"" (look like buttons) to toggle (the css is supposed to make them change color -- don't get confused with my hover settings, remove cursor after clicking to see if it changes color as intended<br/>
		> I can get:<br/>
			- some sort of callback from html/css through JS into Python, which I save in Python class attributes.<br/>

2. Location potential issues.<br/>
	LITTTT!  Location works from Heroku link. And I think I have the data storage thing figure out so it only asks once.<br/>
	Possible Issues:<br/>
		> Requesting yelp API for default (hard-coded) location (Blacksburg) -- inefficient -- before client location is requested. Need to implement a way to load the template (and get client location) before hitting the API; and/or implement a loading screen/wrapper until location is received and proper API results are acquired.
		> home.py.StoredData() class: Not sure about the scope of this class/variable in Heroku, I don't understand how scopes work when app is published to Heroku (probably the same as any other domain).
	Dev Issues:<br/>
		> Difficult to test efficiently, location not working in Ubuntu/localhost environment and Heroku load requires entire Python install (~60 second load)<br/>


<br/>
(Pete can [probably] do all below items)<br/>
Improve efficiency of loading businesses<br/>
Toggle buttons for meal time (breakfast/lunch/dinner/late night)<br/>
Toggle buttons for popularity (rating, num reviews)<br/>
Get distance user is willing to travel<br/>
Adjust min/ max distance in API request as needed<br/>
<br/>

Maybe worth my time:<br/>
Loading screen/icon<br/>
div containers: Had to hard code b/c wasted way too much time trying to dynamically do the rows/columns to fit exactly the screen (vh/vw)<br/>


Before submission:
update readme (mention creds.py)
update gitignore (remove creds.py)


