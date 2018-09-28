## Overview

* Performs automated OSINT on a domain / email / username / IP and find out relevant information from different sources. 
* Easy to contribute OSINT Framework. 
* Code for Banner, Main and Output function. Datasploit automagically do rest of the things for you.
* Useful for Pen-testers, Bug Bounty Hunters, Cyber Investigators, Product companies, Security Engineers, etc.
* Collaborate the results, show them in a consolidated manner. 
* Tries to find out credentials, api-keys, tokens, subdomains, domain history, legacy portals, usernames, dumped accounts, etc. related to the target.
* Can be used as library, automated scripts or standalone scripts. 
* Can generate lists which can be feeded to active scan tools.
* Generates HTML, along with text files.  

## Why DataSploit???

Irrespective of whether you are attacking a target or defending one, you need to have a clear picture of the threat landscape before you get in. This is where DataSploit comes into the picture. Utilizing various Open Source Intelligence (OSINT) tools and techniques that we have found to be effective, DataSploit brings them all into one place, correlates the raw data captured and gives the user, all the relevant information about the domain / email / IP / person, etc. It allows you to collect relevant information about a target which can expand your attack/defence surface very quickly. Sometimes it might even pluck the low hanging fruits for you without even touching the target and give you quick wins. Of course, a user can pick a single small job (which do not correlates obviously), or can pick up the parent search which will launch a bunch of queries, call other required scripts recursively, correlate the data and give you all juicy information in one go.


## Tool Background 

Created using our beloved Python, DataSploit simply requires the bare minimum data (such as domain name, email ID, person name, etc.) before it goes out on a mining spree. Once the data is collected, firstly the noise is removed, after which data is correlated and after multiple iterations it is stored locally in a database which could be easily visualised on the UI provided. The sources that have been integrated are all hand picked and are known to be providing reliable information. We have used them previously during different offensive as well as defensive engagements and found them helpful.

Apart from being a tool, DataSploit is an easy to use OSINT framework where people can contribute other modules and help the community with cutting edge researches. 
People can either write modules for DataSploit or can simpley import datasploit as library and write their own tools.


## Setup

Worried about setup? We got you. You should be worried about two things:

* Install dependencies
    - Python dependencies: Either use requirements.txt (`pip install -r requirements.txt`) if installed with `git clone` or simply `pip install datasploit` to install everything needed as a library.
    - System dependencies: PhantomJS, Chrome or Firefox needs to be installed for certain modules to render javascript heavy websites.
* Feeding specific API keys for few specific sources. We are going to have a knowledge base where step by step instructions to generate these API keys will be documented. Sweet deal? 
* [Click here to check step by step setup guide](/setupGuide/)

## Roadmap

1. While focusing on new modules, we didnt paid much attention to Exception handling. This is something we are keen to work on. Any contibutors? We already love you. 
2. Apart from this, in order to make it more useful in daily life of a pen-tester, we are working to active scripts which can get data from datasploit and use the OSINT data agregated from multiple sources. 
