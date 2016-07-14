# Welcome to the DataSploit wiki!!!
## Overview

* Performs automated OSINT on a domain / email / username / phone and find out relevant information from different sources. 
* Useful for Pen-testers, Cyber Investigators, Product companies, defensive security professionals, etc. 
* Correlates and collaborate the results, show them in a consolidated manner. 
* Tries to find out credentials, api-keys, tokens, subdomains, domain history, legacy portals, etc. related to the target.
* Available as single consolidating tool as well as standalone scripts. 
* Available in both GUI and Console. 

## Why DataSploit???

Data! Data! Data! I can't make bricks without clay". This quote by fictional detective Sherlock Holmes certainly suits every InfoSec professional's daily struggle. Irrespective of whether you are attacking a target or defending one, you need to have a clear picture of the threat landscape before you get in. This is where DataSploit comes into the picture. Utilizing various Open Source Intelligence (OSINT) tools and techniques that we have found to be effective, DataSploit brings them all into one place, correlates the raw data captured and gives the user, all the relevant information about the domain / email / phone number / person, etc. It allows you to collect relevant information about a target which can expand your attack/defence surface very quickly. Sometimes it might even pluck the low hanging fruits for you without even touching the target and give you quick wins. Of course, a user can pick a single small job (which do not correlates obviously), or can pick up the parent search which will launch a bunch of queries, call other required scripts recursively, correlate the data and give you all juicy information in one go.

## Tool Background 

Created using our beloved Python, MongoDb and Django, DataSploit simply requires the bare minimum data (such as domain name, email ID, person name, etc.) before it goes out on a mining spree. Once the data is collected, firstly the noise is removed, after which data is correlated and after multiple iterations it is stored locally in a database which could be easily visualised on the UI provided. The sources that have been integrated are all hand picked and are known to be providing reliable information. We have used them previously during different offensive as well as defensive engagements and found them helpful.

## Setup

Worried about setup? Well, there are two major requirements here: 

* Setting up the db, django, libraries, etc. We have got a script which will automate this for you, so can just go ahead and shoot the OSINT job. 
* Feeding specific API keys for few specific sources. We are going to have a knowledge base where step by step instructions to generate these API keys will be documented. Sweet deal? 
* [Click here to check step by step setup guide](Setup-Guide)

## Roadmap

Apart from this, in order to make it more useful in daily life of a pen-tester, we are working to make the tool as an extension of the other tools that pen-testers commonly use such as Burp Suite, Maltego etc. so that you can feel at home during the usage.
