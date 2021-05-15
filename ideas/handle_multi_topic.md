## JDBC Sink Connector creation upon create table event
```
JDBC Sink Connector is an API Call which can be triggered upon create table event in ddl change topics(dbhistory.inventory).

DDL functionalities handled as far in app code:
1. ALTER TABLE 
2. DELETE TABLE

Note 
CREATE TABLE is not handled by the app and the event is missed. Moreover the table creation is handled dynamically
by jdbc sink connector upon INSERT dml queries.

What can be done ? 
Call jdbc sink api which creates a new consumer to pull dml changes from the table . This api call is 
triggered upon the event in the kafka ddl topic.

```
- [x] Call JDBC Sink Connector dynamically
