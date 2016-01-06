# bball_reference

Current State
-------------
* Working on parsing basketball reference box scores to store in a database. Eventually want to make a UI to query the DB. 
* Can grab any season's or day's data and store it in a list. Next step is to insert into sqlite table.

Getting Started
---------------
pip install virtualenv
virtualenv env
. env/bin/activate
pip install -r requirements.txt
python bball_ref.py

ToDo
------
* Store data in sqlite table

Reference
---------
Requests -
http://docs.python-requests.org/en/latest/

Beautiful Soup - 
http://www.crummy.com/software/BeautifulSoup/bs4/doc/
