.. PennCycle documentation master file, created by
   sphinx-quickstart on Sat Nov 23 00:32:30 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. Welcome to PennCycle's documentation!
.. =====================================

.. Contents:

.. .. toctree::
..    :maxdepth: 2
..    Check In

Overview
========

In order to make sure nobody can maliciously modify our data,
all actions that are associated with a user require the user's
PIN as well as PennCard. For the purpose of this app, users can
be assumed to know their PIN.

All data is to be sent as JSON.

The examples use curl, some with the -i option to display the status code (200 or 400), and all with the -d option to send data.

The 400 error responses all have an ``error`` that explains the cause. All the application must do is check the status code, and if the code is 400, display the error that the server returns.

Finally, all the URLs end with a trailing slash (penncycle.org/mobile/verify/) and will give an error if they are requested without the slash.

Here are the endpoints:

Log in
======

The idea is that once a student has logged in, you can store
their authentication information and they'll never have to enter it again.
Thus, although the rest of these endpoints require this information, it should be stored on the device rather than asking for it multiple times.

- url: http;//penncycle.org/mobile/verify/

- data:

	- penncard (8 digits)

	- pin (4 digits)

	For example:

..	code-block:: javascript

	{
		"penncard": 88888888,
		"pin": 9517
	}

- returns:

	There are actually 3 options, of which you'll need at least 2.

	- The first option is that the penncard matches the pin. This will return json with the following information:

		- name: Student's name
		- can_ride: Boolean: whether or not the student can ride
		- ride_history: A list with that student's ride history (you can ignore this)
		- current_ride: Ride object of current_ride or null,
		- current_payments: A list with that student's payments (you can ignore this)

	- The second option is that the penncard is recognized but the PIN is incorrect. This gets a 400 response with an error message "Student does not exist."

	- The third option is that the penncard is not recognized. This gets a 400 response with the error message "Invalid PIN."

Example verify:
---------------

.. code-block:: bash

	$ curl -i http://penncycle.org/mobile/verify/ \
	  -d 'penncard=88888888&pin=9517'

	HTTP/1.0 200 OK
	Date: Sat, 23 Nov 2013 08:31:46 GMT
	Server: WSGIServer/0.1 Python/2.7.5
	Content-Type: text/html; charset=utf-8

	{"current_ride": {"checkin_station": null, "bike": {"status": "out", "name": "23", "location": "Rodin"}, "checkout_station": "Rodin", "checkout_time": "2013-11-23 09:38:05.822216+00:00", "checkin_time": "None"}, "ride_history": [{"checkin_station": "PSA", "bike": {"status": "out", "name": "22", "location": "Fisher"},
	...

	$ curl -i http://penncycle.org/mobile/verify/ \
		  -d 'penncard=88888888&pin=9999'

	HTTP/1.0 400 BAD REQUEST
	...
	Content-Type: application/json

	{"error": "Invalid PIN."}

	$ curl -i http://penncycle.org/mobile/verify/ \
		  -d 'penncard=44444444&pin=9999'

	HTTP/1.0 400 BAD REQUEST
	...
	Content-Type: application/json

	{"error": "Student does not exist."}


Check Out
=========

- url: http://penncycle.org/mobile/checkout/


- data:

	- penncard (8 digits)

	- pin (4 digits)

	- Bike name (1-2 digits, same names as /mobile/bike_data/)

	For example:

	{
		"penncard": 88888888,
		"pin": 9517,
		"bike": 99
	}

- returns:

	- Success with status code 200 and the bike combination, which should be displayed to the user

	- or Failure with status code 400 and an error (bike unavailable for example, which should be rare as they should only see available bikes. This could happen if 2 people check the bike out at once.)

	- or Failure with a status code 403 meaning the student's PIN did not match.

	*note that this should not happen as the PIN should be verified by now. This precaution only exists in case somebody manually submits an unauthorized request*

Example check out
-----------------

.. code-block:: bash

	$ curl -i localhost:8000/mobile/checkout/ -d 'penncard=44060511&pin=4444&bike=23'

	HTTP/1.0 200 OK
	Date: Sat, 23 Nov 2013 09:38:05 GMT
	Server: WSGIServer/0.1 Python/2.7.5
	Content-Type: application/json

	{"combo": "5720"}

	$ curl -i localhost:8000/mobile/checkout/ -d 'penncard=88888888&pin=4444&bike=22'

	HTTP/1.0 400 BAD REQUEST
	Date: Sat, 23 Nov 2013 09:36:52 GMT
	Server: WSGIServer/0.1 Python/2.7.5
	Content-Type: application/json

	{"error": "Bike 22 is unavailable with status 'out'."}

	$ curl -i http://penncycle.org/mobile/checkout/ \
  -d 'penncard=44444444&pin=9517&bike=99'

	HTTP/1.0 400 BAD REQUEST
	Date: Sat, 23 Nov 2013 09:24:35 GMT
	Server: WSGIServer/0.1 Python/2.7.5
	Content-Type: application/json

	{"error": "Student does not exist."}

	$ curl -i localhost:8000/mobile/checkout/ -d 'penncard=44444444&pin=0000&bike=99'

	HTTP/1.0 400 BAD REQUEST
	Date: Sat, 23 Nov 2013 09:27:07 GMT
	Server: WSGIServer/0.1 Python/2.7.5
	Content-Type: application/json

	{"error": "You don't currently have any PennCycle plans. Log on to penncycle.org to add one."}

	$ curl -i localhost:8000/mobile/checkout/ \
	-d 'penncard=44060511&pin=2222&bike=99'

	HTTP/1.0 403 FORBIDDEN

Check in
========

- url: http://penncycle.org/mobile/checkin/

- data:

	- penncard (8 digits)

	- pin (4 digits)

	- station name (same names as /mobile/station_data/)

	Station names are case-insensitive.

	For example:

	{
		"penncard": 88888888,
		"pin": 9517,
		"station": "Huntsman"
	}


- returns:

	- Success: 200 HTTP code

	- Failure: 400 HTTP code, and an ``error``.

Example check in
----------------

.. code-block:: bash

	$ curl -i http://penncycle.org/mobile/checkin/ \
	  -d 'penncard=88888888&pin=9517&station=huntsman'

	HTTP/1.0 200 OK
	Date: Sat, 23 Nov 2013 08:31:46 GMT
	Server: WSGIServer/0.1 Python/2.7.5
	Content-Type: text/html; charset=utf-8

.. code-block:: bash

	$ curl -i http://penncycle.org/mobile/checkin/ \
	  -d 'penncard=44060511&station=nonexistant'

	HTTP/1.0 400 BAD REQUEST
	...
	Content-Type: application/json

	{"error": "Station not found."}


Report Issue
============

The simplest request only needs the penncard and the message.

- url: http://penncycle.org/mobile/report/

- data:

	- feedback (a string)

	- penncard (8 digits)

- returns:

	200