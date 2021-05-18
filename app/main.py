from connector import stream_connection
from simple_ddl_parser import DDLParser

if __name__ == '__main__':
    stream_connection.start_consumer()
    # statement = 'CREATE TABLE `addresses` (`id` int(11) NOT NULL AUTO_INCREMENT,`customer_id` int(11) NOT NULL,`street` varchar(255) NOT NULL,`city` varchar(255) NOT NULL,`state` varchar(255) NOT NULL,`zip` varchar(255) NOT NULL,PRIMARY KEY (`id`),KEY `address_customer` (`customer_id`),CONSTRAINT `addresses_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`)) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1';
    # statement = statement.replace('`', '"')
    # statement = statement.replace('\n', '')
    # statement = statement.replace('AUTO INCREMENT', '')
    # statement = statement.replace('AUTO_INCREMENT', '')
    # statement = statement.replace('DEFAULT NULL', '')
    # statement = statement.replace('NOT NULL', '')
    # start_pos = statement.find("ENGINE=InnoDB")
    # statement = statement[0:start_pos]
    # while(statement.find("CONSTRAINT") > 0):
    #     start_pos_1 = statement.find("CONSTRAINT") -1
    #
    #     next_pos_comma = statement.find(",", start_pos_1+1) if statement.find(",", start_pos_1+1)  > 0 else len(statement)+1
    #     next_pos_bracket = statement.find(")", start_pos_1+1)-1
    #     statement = statement.replace(
    #         statement[start_pos_1: next_pos_comma if next_pos_comma < next_pos_bracket else next_pos_bracket], "")
    #
    # # statement = 'CREATE TABLE "customers" (  "id" int(11) NOT NULL AUTO_INCREMENT,  "first_name" varchar(255) NOT NULL,  "last_name" varchar(255) NOT NULL,  "email" varchar(255) NOT NULL,  PRIMARY KEY ("id"), "email" varchar(255)) '
    # result = DDLParser(statement).run(output_mode="mysql")
    # primary_key = ','.join(result[0]["primary_key"])
    # print(f"Result from ddl parsing : {primary_key}")

