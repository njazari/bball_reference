# bball_reference

Current State
-------------
* Working on parsing basketball reference box scores to store in a database. Eventually want to make a UI to query the DB. 
* Currently can parse a day's worth of games. Need to extend this out to the entire season and more.
* Code is still very static. Mostly experimenting and trying out different ideas. 

Getting Started
---------------
pip install virtualenv
virtualenv env
. env/bin/activate
pip install -r requirements.txt
python bball_ref.py

ToDo
------
> Decide what kind of db to store data in
> Add abstraction layer to code
> Parse multiple seasons. 

Reference
---------
Requests
> http://docs.python-requests.org/en/latest/
Beautiful Soup
> http://www.crummy.com/software/BeautifulSoup/bs4/doc/
