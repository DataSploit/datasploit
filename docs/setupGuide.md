This page holds the setup guide you will need before kicking off the datasploit in your system. Please note that all the documentation is as per *nix machines, and the tool has not been thoroughly tested on Windows platform. If you would like to volunteer for the same, give us a shout at helpme@datasploit.info. Following are the quick steps to get you going:

### Step 1 - Download DataSploit to your system.

You can either use the git command line tools using the following command:
```
git clone https://github.com/upgoingstar/datasploit.git
```
, or you can simply download the zip file *([link](https://github.com/upgoingstar/datasploit/archive/master.zip))* and extract the same using unzip.
```
unzip master.zip
```

### Step 2: Install python dependencies

Go into the tool directory and install all the python libraries using the requirements.txt file. In case you encounter 'Permission Denied' error, use sudo.
```
cd master
pip install -r requirements.txt
```
### Step 3: Rename config_sample.py to config.py

Please make sure that config.py is added in your gitIgnore file so that this is not commited in any case. We care for your data too, and hence this tip. :) 
```
mv config_sample.py config.py
```
### Step 4: Generate API Keys and paste inside config_sample.py

Generate API keys using the *api Key Generation* guide at 
> http://datasploit.readthedocs.io/en/latest/apiGeneration/ 

and enter the respective values in config.py file. Leave all other key value pairs blank.

### Step 5: Install MongoDB

Datasploit uses mongoDb in the backend and hence require a running instance of mongoDb in order to save and query data. Install the mongoDb database as per the instructions from the below mentioned site:
> https://docs.mongodb.com/manual/installation

For MAC
```
brew install mongodb
```

Create a directory inside datasploit master folder for storing the db files, and Start the mongoDb service with this database path:
```
mkdir datasploitDb
mongod --dbpath datasploitDb
```

Congratulations, you are now good to go. Lets go ahead and run our automated script for OSINT on a domain. 
```
python domainOsint.py -d <domain_name>
```

If you are looking for the UI part.

### Step 6: Install RabbitMQ

Let the previous terminal open with that, open a new terminal and install RabbitMQ
> https://www.rabbitmq.com/install-homebrew.html

For MAC
```
brew install rabbitmq
PATH=$PATH:/usr/local/sbin >> .bash_profile
rabbitmq-server
```

### Step 7: Start django server

Open a new terminal, go inside your datasploit master folder

```
cd core
python manage.py runserver
```

Now it will show an ip:port mostly http://127.0.0.1:8000 once you get this then open below link to get the UI.
> 127.0.0.1:8000/osint

Now feel free to run the domain osint using UI.


