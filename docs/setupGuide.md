# Setting up DataSploit

The setup is quite easy.

**Make sure you have Python 2.7.x installed in your system.**

## Step 1

* Download DataSploit to your system.

**Procedure 1:** 

* Git way (Make sure you have Git up and running in your system).
```bash
git clone https://github.com/upgoingstar/datasploit.git
```

**Procedure 2:**

* Download the zip file.
* [Click here to download](https://github.com/upgoingstar/datasploit/archive/master.zip).
* Extract the zip file.

## Step 2

* Installing python dependencies (Make sure pip is installed in your system).
```bash
pip install -r requirements.txt
```

## Step 3

* Generate API Keys and paste inside **config_sample.py**.
* [Click here to check step by step guide to generate API keys](API-Generation).

## Step 4

* Setup the config file to run the tool.
```bash
mv config_sample.py config.py
```

## Step 5

* Install MongoDB and make sure its up and running.
* [Click here for MongoDB documentation](https://docs.mongodb.com/manual/installation/) 

## Step 6

* You are ready to roll.

```bash
python domainOsint.py <domain_name>
```
