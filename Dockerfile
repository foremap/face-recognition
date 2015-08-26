FROM opencv/32bit
MAINTAINER Sean Chuang <sean_chuang@htc.com>

# add flask-server folder
RUN pip install Flask
ADD flask-server /opt/flask-server
ADD omron /opt/omron

# run server
EXPOSE 8888
WORKDIR /opt/flask-server
CMD ["python", "server.py"]

# cleanup
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*