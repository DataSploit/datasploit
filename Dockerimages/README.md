# Datasploit dockerimages

### You will need to provide config.py file for both these images!

### Grab Coffee :coffee: on build it takes about ~5 minutes

## Development image: 
### This image allows you test source code changes
```bash 

$ cp $EDITED_SOURCE_CODE_DIR src/
$ docker build -t="dasploit/datasploit" -f Dockerfile.dev  .
$ docker run -d --name="datasploit"  datasploit/datasploit
$ docker exec -it datasploit bash
root@61e05f5b7776:/datasploit#

```


## Working docker image 
### This image clones from the master branch

```bash
$ docker build -t="datasploit/datasploit" -f Dockerfile .
$ docker run -d --name="datasploit"  datsploit/datasploit
$ docker exec -it datasploit bash
k4ch0w@5722c53edc24:/datasploit$ python domainOsint.py

	  ____/ /____ _ / /_ ____ _ _____ ____   / /____  (_)/ /_
	  / __  // __ `// __// __ `// ___// __ \ / // __ \ / // __/
	 / /_/ // /_/ // /_ / /_/ /(__  )/ /_/ // // /_/ // // /_
	 \__,_/ \__,_/ \__/ \__,_//____// .___//_/ \____//_/ \__/
	                               /_/

         	   Open Source Assistant for #OSINT
                     website: www.datasploit.info

[-] Invalid argument passed.
Usage: domainOsint.py [options]

Options:
  -h,		--help			show this help message and exit
  -d DOMAIN,	--domain=DOMAIN		Domain name against which automated Osint is to be performed.
k4ch0w@5722c53edc24:/datasploit$
```



