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

2. Location not working.<br/>
	UPDATE 3/6/20: The location work is read from Windows after pushing to Heroku. Only problem is efficient testing will be tricky.
	I've deleted most of the code at this point. Tried implementing this: https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API and it did not work due to "network issues".<br/>
	Aparently "Geolocation API" is really simple (only two methods) -- my issue could be in the browser? (I'm using firefox from Ubuntu virtualbox).
	I also wanted to make a callback to Python with the lat/lon and update home.storedData (defined main.py line 35), so that the location is saved and does not repeatedly ask the user to allow.<br/>
	JS code: templates/app.html<br/>
	HTML code: templates/app.html [attempt to call JS function line 191]<br/>


Toggle buttons for meal time (breakfast/lunch/dinner/late night)<br/>
Toggle buttons for popularity (rating, num reviews)<br/>
Get user location<br/>
Get distance user is willing to travel<br/>
Adjust min/ max distance in API request as needed<br/>
Improve efficiency of loading businesses<br/>
<br/>

Maybe worth my time:<br/>
Loading screen/icon<br/>
div containers: Had to hard code b/c wasted way too much time trying to dynamically do the rows/columns to fit exactly the screen (vh/vw)<br/>


Before submission:
update readme (mention creds.py)
update gitignore (remove creds.py)


