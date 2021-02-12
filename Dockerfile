FROM amazonlinux
RUN yum update -y

RUN yum -y update && \
    yum -y install wget && \
    yum install -y tar.x86_64 && \
    yum clean all

RUN yum -y update && yum -y install python3 python3-dev python3-pip python3-virtualenv \
	java-1.8.0-openjdk wget

RUN python -V
RUN python3 -V

ENV PYSPARK_DRIVER_PYTHON python3
ENV PYSPARK_PYTHON python3

RUN pip3 install --user --upgrade pip
RUN pip3 install numpy panda
RUN pip3 install prettytable

RUN cd /opt && wget https://apache.osuosl.org/spark/spark-2.4.7/spark-2.4.7-bin-hadoop2.7.tgz && tar -xzf spark-2.4.7-bin-hadoop2.7.tgz && rm spark-2.4.7-bin-hadoop2.7.tgz


RUN ln -s /opt/spark-2.4.7-bin-hadoop2.7 /opt/spark
RUN (echo 'export SPARK_HOME=/opt/spark' >> ~/.bashrc && echo 'export PATH=$SPARK_HOME/bin:$PATH' >> ~/.bashrc && echo 'export PYSPARK_PYTHON=python3' >> ~/.bashrc)

RUN mkdir /predict_wine
COPY TrainingDataset.csv /predict_wine/ 
COPY predict1.py /predict_wine/ 

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN /bin/bash -c "source ~/.bashrc"
RUN /bin/sh -c "source ~/.bashrc"

WORKDIR /predict_wine

ENTRYPOINT ["/opt/spark/bin/spark-submit", "--packages", "org.apache.hadoop:hadoop-aws:2.7.7", "predict1.py"]
