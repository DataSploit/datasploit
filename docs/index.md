# Datasploit

## Overview of the tool
* Performs OSINT on a domain / email / username / phone and find out information from different sources.
* Correlates and collaborate the results, show them in a consolidated manner. 
* Tries to find out credentials, api-keys, tokens, subdomains, domain history, legacy portals, etc. related to the target. 
* Use specific script / launch automated OSINT for consolidated data.
* Available in both GUI and Console.
 
Following API configs are mandatory for proper results in domainOsint.py:
* shodan_api
* censysio_id
* censysio_secret
* zoomeyeuser
* zoomeyepass
* clearbit_apikey
* emailhunter

Other modules:
* github_access_token
* instagram_token
* instagram_client_id
* instagram_client_secret
* jsonwhois


## Before running the program, please make sure that you have
* Changed the name of the file `config_sample.py` to `config.py`
* Entered all the required APIs in `config.py` file, as mentioned above. 
* Installed MongoDb and the mongodb is running. [Refer to documentation](https://docs.mongodb.com/manual/installation/) 


## Usage
To launch an automated OSINT on domain, shoot following query:

```bash
python domainOsint.py <domain_name>
```
You can also run an standalone script, e.g.you might want to only run the subdomain finding script and avoid all other modules. In such case, use below mentioned command. *All the files starting with domain_ requires a domain name to be passed as first argument. Same follows for email, ip, etc.*

```bash
python domain_subdomain.py <domain_name>
```

To launch an automated OSINT on domain, shoot following query:

```bash
python domainOsint.py <domain_name>
```

## Setup and Contribution
* Change config_sample.py to config.py
```bash
mv config_sample.py config.py
```
* Configure respective API keys. Documentation for generating these keys will be shared very shortly. Believe us, we are working hard to get things in place. 
* Sources for which API keys are missing, will be simply skipped for the search. 

### Config files

### Python dependencies

```
pip install -r requirements.txt
```

If you have updated the code and want to push the pip dependencies in the requirements.txt 

```
pip freeze > requirements.txt
```

