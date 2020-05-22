[![ToolsWatch Best Tools](https://www.toolswatch.org/badges/toptools/2016.svg)](http://www.toolswatch.org/2017/02/2016-top-security-tools-as-voted-by-toolswatch-org-readers/)

[![Arsenal-2017-EU](https://github.com/toolswatch/badges/blob/master/arsenal/europe/2017.svg)](http://www.toolswatch.org/2017/09/black-hat-arsenal-europe-2017-lineup/)

[![Arsenal-2017-US](https://github.com/toolswatch/badges/blob/master/arsenal/usa/2017.svg)](http://www.toolswatch.org/2017/06/the-black-hat-arsenal-usa-2017-phenomenal-line-up-announced/)

[![Arsenal-2017-ASIA](https://github.com/toolswatch/badges/blob/master/arsenal/asia/2017.svg)](http://www.toolswatch.org/2017/02/the-black-hat-arsenal-asia-2017-great-line-up/)

[![Arsenal-2016-EU](https://www.toolswatch.org/badges/arsenal/2016.svg)](http://www.toolswatch.org/2016/09/the-black-hat-arsenal-europe-2016-line-up/)

[![Arsenal-2016-US](https://www.toolswatch.org/badges/arsenal/2016.svg)](http://www.toolswatch.org/2016/06/the-black-hat-arsenal-usa-2016-remarkable-line-up/) 

[![DEFCON 25 ReconVillage](https://img.shields.io/badge/DEFCON%2025-Recon%20Village-red.svg)](http://reconvillage.org/) [![DEFCON 24 Demolabs](https://img.shields.io/badge/DEFCON%2024-Demo%20Labs-red.svg)](https://www.defcon.org/html/defcon-24/dc-24-demolabs.html)

[![Join Datasploit Slack](https://img.shields.io/badge/slack-open-e01563.svg)](http://datasploit.slack.com "Join our Slack community")

[![Follow Datasploit on Twitter](https://img.shields.io/twitter/follow/datasploit.svg?style=social&label=Follow%20%40datasploit)](https://twitter.com/intent/user?screen_name=datasploit "Follow Datasploit on Twitter")

# Overview of the tool:
* Performs OSINT on a domain / email / username / phone and find out information from different sources.
* Correlate and collaborate the results, show them in a consolidated manner. 
* Tries to find out credentials, api-keys, tokens, subdomains, domain history, legacy portals, etc. related to the target. 
* Use specific script / launch automated OSINT for consolidated data.
* Performs Active Scans on collected data.
* Generates HTML, JSON reports along with text files.
 
## Basic Usage:
```

	  ____/ /____ _ / /_ ____ _ _____ ____   / /____  (_)/ /_
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

# Required Setup:
* Python 2.7 (because bunch of dependencies do not support Python 3.0)
* Bunch of python libraries (use requirements.txt)
* In **Kali Linux**, please install the requirements using the command `pip install --upgrade --force-reinstall -r requirements.txt`

## Detailed Tool Documentation:
> [https://datasploit.github.io/datasploit/](https://datasploit.github.io/datasploit/)

### Lead Developers
* Shubham Mittal - https://github.com/upgoingstar
* Sudhanshu Chauhan - https://github.com/sudhanshuc
* Kunal Aggarwal - https://github.com/KunalAggarwal

### Social Media 
* [Official Website](https://datasploit.github.io/datasploit/) 
* [Twitter](https://twitter.com/datasploit)
* [Facebook](https://facebook.com/datasploit)

### TODO
* Create a file that sets if a module is enabled or not
