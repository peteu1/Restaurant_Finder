# Restaurant_Finder
Web application using the Yelp API to help find good restaurants. This is for the Capital One challenge (https://www.mindsumo.com/contests/d052bcf8-4580-4922-95ef-a9f6ceaf0f10).

Link to page: https://restaurant-finder-peteu.herokuapp.com/


> Development:

Issues:
1. Checkboxes do not work properly.
	HTML code: templates/partials/filters.html  [class='ck-button']
	CSS code: static/css/app.css  [Lines 81-119]
		> This styles the checkboxes how I'd like, but they are not actually toggling "checked" (probably because I have an onclick() call in the <input> tags in filters.html)
	JS code: templates/app.html  [<script> tags at top]
		> I've tried a ton of things (much of it commented out)
		> I can't get:
			- a callback to Python [home.py/background_process()] while having the ""check boxes"" (look like buttons) to toggle (the css is supposed to make them change color -- don't get confused with my hover settings, remove cursor after clicking to see if it changes color as intended
		> I can get:
			- some sort of callback from html/css through JS into Python, which I save in Python class attributes.

2. Location not working.
	I've deleted most of the code at this point. Tried implementing this: https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API and it did not work due to "network issues". 
	Aparently "Geolocation API" is really simple (only two methods) -- my issue could be in the browser? (I'm using firefox from Ubuntu virtualbox).
	I also wanted to make a callback to Python with the lat/lon and update home.storedData (defined main.py line 35), so that the location is saved and does not repeatedly ask the user to allow.
	JS code: templates/app.html
	HTML code: templates/app.html [attempt to call JS function line 191]


Toggle buttons for meal time (breakfast/lunch/dinner/late night)
Toggle buttons for popularity (rating, num reviews)
Get user location
Get distance user is willing to travel
Adjust min/ max distance in API request as needed
Improve efficiency of loading businesses


Maybe worth my time:
Loading screen/icon
div containers: Had to hard code b/c wasted way too much time trying to dynamically do the rows/columns to fit exactly the screen (vh/vw)


Before submission:
update readme (mention creds.py)
update gitignore (remove creds.py)


