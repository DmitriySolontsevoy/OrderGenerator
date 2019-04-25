# Order Generator
A generator of order history with multiple services written in python.
An order is a currency pair trade operation with multiple records for each of possible status, that this operation follows.
This program is tasked with generating a configurable amount of these order records, messaging them to RabbitMQ, consuming them from this same broker and inserting received messages to a MySQL database

  Python version: 3.7.2

# Requirements
Additional software, required for this program includes:
* MySQL server v. 5.7.15: https://downloads.mysql.com/archives/installer/
* RabbitMQ server 3.7.12: https://www.rabbitmq.com/download.html

Following python modules have to be included:
* pika 0.13.0 - for RabbitMQ
* protobuf 3.7.1 - ProtoBuf
* mysql-connector 2.1.6 - for MySQL
* numpy 1.16.1 - SciPy requirement
* scipy 1.2.1 - for generating

# Database creation
This app uses a certain table format to correctly store data, use code from database_script.sql in root of the project. Copy it to your SQL Editor and make sure every query has been properly executed

# Preparations
First of all you need to clone this program to your machine. Make sure you have .git installed on your machine. Navigate to a desired location and then execute following command:

```bash
git clone https://github.com/DmitriySolontsevoy/OrderGenerator.git
```

Next, you need to setup needed python environment. You can install all libs manually, or alternatively you can install them by running this command:

```bash
pip install -r ./requirements.txt 
```

# Configure the project
In the Configs\Configurable\ there's a file, called config.json. This file configurates parameters for RMQ, MySQL connections, regulates generation rules, and also sets targets and levels for logging.

Currently, logging can target a text file or console:
* For console output:
  * Enable with "CONSOLE_LOGGING" set to 1, disable with 0
  * Set console logging level with "CONSOLE_LOG_LEVEL":
    * 1 - ERROR
    * 2 - WARN
    * 3 - INFO
    * 4 - DEBUG   
* For text file output:
  * Enable with "TEXT_LOGGING" set to 1, disable with 0
  * Set console logging level with "TXT_LOG_LEVEL":
    * 1 - ERROR
    * 2 - WARN
    * 3 - INFO
    * 4 - DEBUG  

As for the number of orders to generate you can use "BATCH_SIZE" to set the size of a single orders batch, then use "BATCH_AMOUNT" to set an amount of these batches. The total amount of orders will be a product of these two settings

# Launch
To start an application, run a file, called Launcher.py in the root of the project:

```bash
python Launcher.py
```
