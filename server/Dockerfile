FROM python:2.7

ADD requirements.txt /tmp/
ADD run_configurer_script.sh /tmp/
ADD run_server_script.sh /tmp/

RUN chmod +x /tmp/run_configurer_script.sh
RUN chmod +x /tmp/run_server_script.sh

RUN pip install -r /tmp/requirements.txt
