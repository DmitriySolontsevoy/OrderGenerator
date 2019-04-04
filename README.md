# Order Generator
A generator of order history with multiple services written in python
It is tasked with generating data for order history, writing it to file, messaging and inserting to a database

Python version: 3.7.2

# Requirements
Following python modules have to be included:
* numpy 1.16.1
* pika 0.13.0 - for RabbitMQ
* protobuf 3.7.1 - ProtoBuf
* mysql-connector 2.1.6 - for MySQL
* scipy 1.2.1 - for generation method

# Requirements
All required libraries are included in requirements.txt file. So you can install them by running this command:

```bash
pip install -r ./requirements.txt 
```

# Launch
To start an application, run a file, called Launcher.py in the root of the project:

```bash
python Launcher.py
```

# Database creation
This app uses a certain table format to correctly store data, use this code to create needed database:

```sql
CREATE DATABASE `generator`

USE `generator`

CREATE TABLE `mytable` (
  `id` bigint(20) DEFAULT NULL,
  `cur_pair` varchar(10) DEFAULT NULL,
  `direction` varchar(5) DEFAULT NULL,
  `status` varchar(15) DEFAULT NULL,
  `date` bigint(20) DEFAULT NULL,
  `init_px` double DEFAULT NULL,
  `init_volume` double DEFAULT NULL,
  `fill_px` double DEFAULT NULL,
  `fill_volume` double DEFAULT NULL,
  `desc` varchar(4) DEFAULT NULL,
  `tags` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```
