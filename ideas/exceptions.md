## Handling datatype column changes Exception cases
Case 1 : AutoIncrement 
This information is not needed at the postgres side. Reason being the data from mysql 
will be blindly inserted in to postgres including the column which has autoincrement feature 
configured. So replaced the value with ""
Case2 : Alter table changing autoincrement start value 
Again this is also not needed at the postgres side. Ref the previous explanation.