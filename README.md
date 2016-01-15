# bball_reference

This program will parse boxscores from basketball reference and store them in a sqlite database. The next step is to add add a user interface where users can query the db. Also add automatic updates to the database.

The current db stored in this repository contains all NBA boxscore data up to 01/13/2016. To add rows to the db, update/use the getRange function in the parser code.    

Getting Started
---------------
To query current database, first unzip the .db file and then run the following commands:

    sqlite3 bball-ref_dataset.db

    (.schema will reveal the schema)

To run parser code: 

    pip install virtualenv

    virtualenv env

    . env/bin/activate

    pip install -r requirements.txt

    python bball_ref.py

Reference
---------
Requests -
http://docs.python-requests.org/en/latest/

Beautiful Soup - 
http://www.crummy.com/software/BeautifulSoup/bs4/doc/

