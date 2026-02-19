hdfs dfs -mkdir -p /user/iabd/sqoop
hdfs dfs -chmod 777 /user/iabd/sqoop
sqoop import --connect jdbc:mysql://instituto.coxyc40e87w4.us-east-1.rds.amazonaws.com/retail_db?useSSL=true&requireSSL=true    \
    --username=admin --password=adminadmin \
    --table=customers --driver=org.mariadb.jdbc.Driver   \
    --target-dir=/user/iabd/sqoop/customers \
    --fields-terminated-by=',' --lines-terminated-by '\n' \
    --columns "customer_id,customer_fname,customer_lname,customer_city"