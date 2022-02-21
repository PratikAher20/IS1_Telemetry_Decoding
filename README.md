# CUBESAT Satnogs Data Download Utility

Small utility program for downloading packets from the Satnogs Database. This queries data for a specified satellite 
and generates a file containing packet data present on the Satnogs DB.

## Setup

To setup for a new mission either edit cuteds/cfg/default_config.yml or copy 
this file to create a new config file which can then be passed in as a command line argument.

The following items must be edited in the config file to download data:

satnogs:prod:token: This should be set to the Satnogs DB API token for a user. This is accessible through the user profile.

satnogs:prod:norad_id: This should be set to the Norad ID of the satellite. This can be found under the Satnogs page for the satellite.

satnogs_rawfiles:prod:location: Absolute path to the directory where data files should be saved.

runtime:mission: Name of the mission being processed, used as part of file name.

## Database for tracking previously downloaded data

In order to track what data has been downloaded the code relies on a simple postgres database to track 
which packets have been downlinked. Use of this database is not strictly required but if it is not used then 
ALL mission data will be downloaded every time the program is run.

Note if database is enabled the needed tables will be automatically created on the first run.
To enable the database set the following in the config file:

database:postgresql:prod:enabled: True
database:postgresql:prod:dbname: The name of the postgres database
database:postgresql:prod:user: The user name of a user with write access to the DB
database:postgresql:prod:password: The password of the above user
database:postgresql:prod:port: The port of the DB
database:postgresql:prod:host: The host name of the DB

## Running program

To run with default_config.yml simply run: 
cutesat_satnogs/main.py

To run with a specific config file run:
cubesat_satnogs/main.py --config /path/to/config/foo_config.yml

Data will be downloaded and output to the file listed under satnogs_rawfiles in the config file.