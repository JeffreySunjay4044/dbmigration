FROM adoptopenjdk/openjdk11:ubi
COPY kotlin*.jar gateway.jar
RUN ["chmod", "+x", "/gateway.jar"]
ENTRYPOINT ["java","-jar","gateway.jar"]
