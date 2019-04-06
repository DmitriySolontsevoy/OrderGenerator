# Order Generator
A generator of order history with multiple services written in python
It is tasked with generating data for order history, writing it to file, messaging and inserting to a database

Python version: 3.7.2

# Requirements
Following python modules have to be included:
* pika 0.13.0 - for RabbitMQ
* protobuf 3.7.1 - ProtoBuf
* mysql-connector 2.1.6 - for MySQL

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
This app uses a certain table format to correctly store data, use code from database_script.sql in root of the project
