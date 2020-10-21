### Table of Contents
- [Deploying a dashboard on AWS by using Lambda functions, RDS and Grafana](#deploying-a-dashboard-on-aws-by-using-lambda-functions-rds-and-grafana)
	- [EC2](#ec2)
		- [Launch instance](#launch-instance)
		- [Install Grafana](#install-grafana)
	- [RDS](#rds)
		- [Create a MySQL DB Instance](#create-a-mysql-db-instance)
		- [Connect to the DB and create a table](#connect-to-the-db-and-create-a-table)
	- [Lambda](#lambda)
	- [IoT Core](#iot-core)
	- [Dashboard](#dashboard)
		- [Add database to Grafana](#add-database-to-grafana)
		- [Create Dashboard](#create-dashboard)

# Deploying a dashboard on AWS by using Lambda functions, RDS and Grafana

The current document explains how to deploy a dashboard following the architecture of the next image.

![pic](pictures/schematics/AWS_iot_lambda_rds_grafana_architecture.png)

Data from temperature and humidity sensors are sent to a 'thing' in the AWS IoT core. It triggers a Lambda function which stores data on an RDS database. Finally, data is shown on a Grafana Dashboard which is deployed on an EC2 instance.


[![pic](pictures/utils/arrow_up.png)](#table-of-contents)
## EC2

Firstly, we launch an Ubuntu EC2 instance to install Grafana. What is Grafana? It's open source visualization and analytics software. It allows you to query, visualize, alert on, and explore your metrics no matter where they are stored.


[![pic](pictures/utils/arrow_up.png)](#table-of-contents)
### Launch instance

1. Follow the steps of the following tutorial to launch an Ubuntu EC2 instance:
    * [Launch an Ubuntu EC2 Instance](https://telefonicaid.github.io/iot-activation/#/AWS_Launch_EC2.md)

2. Open the port 3000 because it's used by Grafana. Open your instance. Click the Security tab and open the Security groups.
![pic](pictures/AWS/AWS_ec2_open_port.png)

3. Click Edit inbound rules
![pic](pictures/AWS/AWS_ec2_open_port2.png)

4. Add a new rule and configure the port 3000 as follow.
![pic](pictures/AWS/AWS_ec2_open_port3.png)


[![pic](pictures/utils/arrow_up.png)](#table-of-contents)
### Install Grafana

The steps to install Grafana on a Ubuntu system are explained in their documentation.

* [Install on Ubuntu](https://grafana.com/docs/grafana/latest/installation/debian/)

We summarize them:

1. Access to the EC2 instance via SSH.
```bash
sudo ssh -i "YOUR_CERT.pem" ubuntu@<Public IPv4 DNS>
```

2. Download and install Grafana.
```bash
sudo apt-get install -y apt-transport-https
sudo apt-get install -y software-properties-common wget
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
```

```bash
# Add this repository for stable releases
echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
```

```bash
# Install
sudo apt-get update
sudo apt-get install grafana
```

3. Start the server.
```bash
# To start the service and verify that the service has started
sudo systemctl daemon-reload
sudo systemctl start grafana-server
sudo systemctl status grafana-server
```

```bash
# Configure the Grafana server to start at boot
sudo systemctl enable grafana-server.service
```

4. Grafana Dashboard login. Open your browser and enter 'http://< Public IPv4 DNS >:3000'. By default, Grafana username and password are admin and admin. From the next screen, you can get the option to change your password.
![pic](pictures/Grafana/Grafana_login.png)

![pic](pictures/Grafana/Grafana_new_pass.png)

![pic](pictures/Grafana/Grafana_home_screen.png)


[![pic](pictures/utils/arrow_up.png)](#table-of-contents)
## RDS

Amazon Relational Database Service (Amazon RDS) is a web service that makes it easier to set up, operate, and scale a relational database in the AWS Cloud. It provides cost-efficient, resizable capacity for an industry-standard relational database and manages common database administration tasks.


[![pic](pictures/utils/arrow_up.png)](#table-of-contents)
### Create a MySQL DB Instance
A MySQL database is created to store data from the temperature and humidity sensors.

1. Open de Amazon RDS Console.

2. In the Create database section, choose Create database.
![pic](pictures/AWS/AWS_rds_create_db.png)

3. You now have options to select your engine.  For this tutorial, click the MySQL icon, leave the default value of edition and engine version, and select the Free Tier template.

![pic](pictures/AWS/AWS_rds_engine_options.png)

4. You will now configure your DB instance. Just configure the DB instance identifier, username and password.
![pic](pictures/AWS/AWS_rds_db_config2.png)

5. Go to the Connectivity section and set Public access to Yes.
![pic](pictures/AWS/AWS_rds_db_config_connectivity.png)

6. Finally, click **Create database**. Your DB Instance is now being created.  Click **View Your DB Instances**. Depending on the DB instance class and storage allocated, it could take several minutes for the new DB instance to become available.


[![pic](pictures/utils/arrow_up.png)](#table-of-contents)
### Connect to the DB and create a table
Once the database instance creation is complete and the status changes to available, you can connect to a database on the DB instance using any standard SQL client. In this step, we will download MySQL Workbench, which is a popular SQL client.

1. Download and install MySQL Workbench from their [website](https://dev.mysql.com/downloads/workbench/).

2. Launch the MySQL Workbench application and go to Database > Connect to Database. Enter the connection settings according to your RDS instance.
![pic](pictures/AWS/AWS_rds_workbench.png)

3. Click **Create a new schema in the connected server** to create a new database. In our case, it's named sensorData.
![pic](pictures/MySQL/Workbench_create_schema.png)

![pic](pictures/MySQL/Workbench_create_schema2.png)

4. Click **Create a new table in the active schema in connected server** to create a new table. In our example, we store data from a temperature and humidity sensor, so we create the table as follow.
![pic](pictures/MySQL/mysql_schema.png)

![pic](pictures/MySQL/mysql_schema_command.png)


[![pic](pictures/utils/arrow_up.png)](#table-of-contents)
## Lambda

AWS Lambda is a compute service that lets you run code without provisioning or managing servers.  AWS Lambda runs your code only when needed and scales automatically, from a few requests per day to thousands per second.

We use AWS Lambda to run code in response to events. The Lambda function runs when a message is received on a topic and stores the temperature and humidity values on a database.

1. Open the AWS Lambda console and click **Create a function**.
![pic](pictures/AWS/AWS_lambda_create_function.png)

2. Choose the latest Python version and click **Create a function**.
![pic](pictures/AWS/AWS_lambda_create_function2.png)

3. Download the code from [Github](https://github.com/telefonicaid/iot-activation/tree/master/scripts/AWS_IoT_Lambda_Grafana).

4. Upload the code as a .zip file.
![pic](pictures/AWS/AWS_lambda_upload_zip.png)

![pic](pictures/AWS/AWS_lambda_upload_zip2.png)

5. Configure the RDS credentials in the **rds_config.py** file.
![pic](pictures/AWS/AWS_lambda_config_rds.png)

6. Create a test to verify if the code works properly.
![pic](pictures/AWS/AWS_lambda_config_test.png)

7. Use a JSON message reported on a shadow accepted topic.
```json
{
  "state": {
    "reported": {
      "temp": 22.5,
      "hum": 45
    }
  },
  "metadata": {
    "reported": {
      "temp": {
        "timestamp": 1602692954
      },
      "hum": {
        "timestamp": 1602692954
      }
    }
  },
  "version": 4,
  "timestamp": 1602692954
}
```
![pic](pictures/AWS/AWS_lambda_config_test2.png)

7. Deploy the Lambda function and test it by clicking the Test button.
![pic](pictures/AWS/AWS_lambda_deploy_test.png)

8. The temperature and humidity data from the test JSON message should be stored on the MySQL DB.
![pic](pictures/MySQL/mysql_select.png)


[![pic](pictures/utils/arrow_up.png)](#table-of-contents)
## IoT Core

In this part of the tutorial, a new "thing" is created in the AWS IoT core to receive data from temperature and humidity sensor. The Lambda function created earlier fires when new values are received on this 'thing'.

1. Create a thing following the steps of this tutorial:
    * [Create device thing in AWS-IoT](https://telefonicaid.github.io/iot-activation/#/AWS_create_new_thing.md)

2. Go to Act -> Rules in the AWS IoT Console and click **Create**.
![pic](pictures/AWS/AWS_rule_create.png)

3. Insert a rule name and set the following rule requirement statement.
```sql
SELECT * FROM '$aws/things/<YOUR_THING_NAME>/shadow/update/accepted'
```

4. Click **Add action**, choose **Send a message to a Lambda function** and click **Configure action**.
![pic](pictures/AWS/AWS_rule_message_to_lambda.png)

5. Choose the Lambda function created in the [Lambda](#lambda) section. Click **Add action**.
![pic](pictures/AWS/AWS_rule_lambda_name.png)

6. Now the rule is configured as follow. Click **Create rule** to finish.
![pic](pictures/AWS/AWS_rule_settings.png)


[![pic](pictures/utils/arrow_up.png)](#table-of-contents)
## Dashboard

Finally, we a dashboard on Grafana is created to visualize the temperature and humidity data.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)
### Add database to Grafana

1. Open your browser and access Grafana 'http://< Public IPv4 DNS EC2 >:3000'.

2. Click **Configuration** icon and then **Data Sources**.
![pic](pictures/Grafana/Grafana_add_db.png)

3. Choose MySQL.
![pic](pictures/Grafana/Grafana_add_mysql_db.png)

4. Configure the database credentials and click **Save & Test**.
![pic](pictures/Grafana/Grafana_db_config.png)


[![pic](pictures/utils/arrow_up.png)](#table-of-contents)
### Create Dashboard

1. Click **Create** icon and select **Dashboard**.

![pic](pictures/Grafana/Grafana_new_dashboard.png)

2. Click **Add new panel** to create a graph.
![pic](pictures/Grafana/Grafana_new_dashboard2.png)

3. Create a query to select the temperature values. Click **Toggle text edit mode** to create the query manually.
![pic](pictures/Grafana/Grafana_query.png)

4. Copy the following SQL query.
```sql
SELECT
  timestamp AS "time",
    CAST(temp as SIGNED integer) as value,
    'temp' as metric
FROM data
WHERE
  $__timeFilter(timestamp)
ORDER BY timestamp
```

5. Add a new **Query** to visualize the humidity values in the same graph.
![pic](pictures/Grafana/Grafana_new_query.png)

6. Add the mysql query.
```sql
SELECT
  timestamp AS "time",
    CAST(hum as SIGNED integer) as value,
    'hum' as metric
FROM data
WHERE
  $__timeFilter(timestamp)
ORDER BY timestamp
```

7. Click **Apply** to close the edit mode.

8. The dashboard is showed like this.
![pic](pictures/Grafana/Grafana_dashboard.png)

9. Save dashboard.

![pic](pictures/Grafana/Grafana_save_dashboard.png)

You can find more information about Grafana capabilities on their [website](https://grafana.com/docs/grafana/latest/).

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)
