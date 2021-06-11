FROM adoptopenjdk/openjdk11:ubi
RUN yum install -y make
COPY kotlin*.jar gateway.jar
RUN ["chmod", "+x", "/gateway.jar"]
ENTRYPOINT ["java","-jar","gateway.jar"]
