# Datasploit

## Source

https://github.com/DataSploit/datasploit

## Usage

```bash
cd datasploit/
docker build -t datasploit .
docker run -it datasploit:latest -i <target>
```

## Help

```bash
usage: datasploit.py [-h] -i TARGET [-a] [-q] [-o OUTPUT]

  ____/ /____ _ / /_ ____ _ _____ ____   / /____   (_)/ /_
 / __  // __ `// __// __ `// ___// __ \ / // __ \ / // __/
/ /_/ // /_/ // /_ / /_/ /(__  )/ /_/ // // /_/ // // /_  
\__,_/ \__,_/ \__/ \__,_//____// .___//_/ \____//_/ \__/  
                              /_/                         

           Open Source Assistant for #OSINT               
               www.datasploit.info                                                           

optional arguments:
  -h, --help            show this help message and exit
  -i TARGET, --input TARGET
                        Provide Input
  -a, --active          Run Active Scan attacks
  -q, --quiet           Run scans in automated manner accepting default
                        answers
  -o OUTPUT, --output OUTPUT
                        Provide Destination Directory

              Connect at Social Media: @datasploit
```