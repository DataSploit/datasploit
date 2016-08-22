# Overview of the tool:

* Performs OSINT on a domain / email / username / phone and find out information from different sources.
* Correlates and collaborate the results, show them in a consolidated manner.
* Tries to find out credentials, api-keys, tokens, subdomains, domain history, legacy portals, etc. related to the target.
* Use specific script / launch automated OSINT for consolidated data.
* Available in both GUI and Console.
 
## Basic Usage:

```

	   ____/ /____ _ / /_ ____ _ _____ ____   / /____   (_)/ /_
	  / __  // __ `// __// __ `// ___// __ \ / // __ \ / // __/
	 / /_/ // /_/ // /_ / /_/ /(__  )/ /_/ // // /_/ // // /_  
	 \__,_/ \__,_/ \__/ \__,_//____// .___//_/ \____//_/ \__/  
	                               /_/                        
						
         	   Open Source Assistant for #OSINT            
                 website: www.datasploit.info               
	
Usage: domainOsint.py [options]

Options:
  -h,	    	--help			    show this help message and exit
  -d DOMAIN,	--domain=DOMAIN		Domain name against which automated Osint 
                                    is to be performed.

```

## Required Setup:

* Bunch of Python libraries (use requirements.txt)
* MongoDb, Django, Celery and RabbitMq (Refer to setup guide).
* Ubuntu requires `brew`, `libxml2-dev`, `libxslt1-dev` and `zlib1g-dev` to be installed

## Detailed Tool Documentation:

> [http://datasploit.readthedocs.io/en/latest/](http://datasploit.readthedocs.io/en/latest/)


