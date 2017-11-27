FROM python:2.7-slim

WORKDIR /root
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/DataSploit/datasploit.git datasploit

WORKDIR datasploit
RUN pip install -r requirements.txt
CMD python datasploit_config.py
ENTRYPOINT ["python", "datasploit.py"]
CMD ["--help"]