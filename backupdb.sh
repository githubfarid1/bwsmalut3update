#!/bin/bash
# Shell script to backup MySQL database

# Set these variables
MyUSER="root"   # DB_USERNAME
MyPASS="workshop21"     # DB_PASSWORD
MyDB="arsipserverdb2" # DB_HOSTNAME

# Backup Dest directory
DEST="/home/arsip/nas-media/db_backup" # /home/username/backups/DB

# Linux bin paths
MYSQL="$(which mysql)"
MYSQLDUMP="$(which mysqldump)"
GZIP="$(which gzip)"

# Get date in dd-mm-yyyy format
NOW="$(date +"%d-%m-%Y_%s")"

# Create Backup sub-directories
MBD="$DEST/$NOW/mysql"
install -d $MBD

FILE="$MBD/arsipserverdb2.sql"
$MYSQLDUMP -u $MyUSER -p$MyPASS $MyDB > $FILE

# Archive the directory, send mail and cleanup
cd $DEST
tar -cf $NOW.tar $NOW
$GZIP -9 $NOW.tar

rm -rf $NOW

