# bball_reference

This program will parse boxscores from basketball reference and store them in a sqlite database. The current db stored in this repository is for the 2015-16 NBA season up to 1/8. This database makes querying for certain NBA statistics very quick and easy.  

Getting Started
---------------
To query current database:
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
