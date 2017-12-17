We are always in process of improving Datasploit as an OSINT framework in order to serve its sole objective, help people in their jobs and make their life easier. We realized there were some issues in installation and excpetion handling and we have resolved many of them. Having said that, we still have a lot more work to do. There is surely a large number of things which we think can be improved/added in datasploit. 

Following are few of the things we are planning to work on, in near future. If you think you have some idea/suggestions, please feel free to reach us on our Slack Channel [https://datasploit.slack.com](https://datasploit.slack.com). (If you are not registered, you can use http://selfinvite.datasploit.info). 

And if you think you can pick any task out of the following features/sources/enhancements, Well, what could be better? Please do send in your Pull Requests. Cheers. 

### Features/Enhancement(s):
1. Check API keys before executing any module. This should be a framework level check. 
2. JSON/Txt outputs for every module.
3. Visualization for the data that comes in. This could be done either in JPG images locally stored. Or setup a front end with Django/Flask/etc.
4. Option to run DataSploit against a file containing a list of emails/domains/subdomains/usernames/etc. This will be an optional switch that will take file as --filename (-f) option. 
5. Dump data in Sqlite3 (keys as one column and whole json document as value), and explore this option to be used as database. Our users earlier faced a lot of problems while setting up MongoDB.


### New Source(s):
1. Locate files for a domain on search engines like Google, Yahoo etc. This could be passed to metadata_extractor module. 
2. Fetch Twitter Sleeping time of a user. More Twitter OSINT is possible. 
3. Add https://urlquery.net
4. Extract files, metadata and enumerate information from metadata
5. More sources for Username Enumeration : Include WhatsMyName by @WebBreacher
6. Module to find All Websites hosted on a domain's server.
7. Add AbuseIPDb
8. Reverse Image Search
9. Search on Darknet. 
10. Company OSINT. Use Open-Corporates for this. User can pass a keyword for which a list of companies (with few details like location, Year of Est., etc.) matching the keyword will be listed. User needs to select the company he/she is targeting for complete search. 