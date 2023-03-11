# twitter_bot
### collect twitter threads (twitt and reply) and show data with django web server  

this source code fetch data from twitter with requests lib in python like console browser
1. clone repository  
`git clone https://github.com/sadng11/twitter_bot`
2. copy `.env.sample`  file to `.env` and set mysql database and twitter api in it.
3. create virtual environment for project
4. install python lib in `requirements.txt` file  
`pip install -r requirements.txt`
5. run `runner.py` file for each username that collected data  
`python runner.py`


#### this file save tweet in db and make thread for each tweet reply


See demo :

- end point list:  
http://82.115.16.114:8003/

- twitter tracked user list:  
http://82.115.16.114:8003/tw-users/?format=json

- twitter conversation thread:  
http://82.115.16.114:8003/tweets/?format=json

- twitter filter conversation thread by author id:  
http://82.115.16.114:8003/tweets/?tw_author_id=813286&format=json

- tweet reply list:  
http://82.115.16.114:8003/reply/?format=json

- tweet reply filter by tweet_id:  
http://82.115.16.114:8003/reply/?twee_id=1630615307759894638&format=json

- user's active audience:  
http://82.115.16.114:8003/audience/?format=json
