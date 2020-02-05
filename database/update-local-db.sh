  
# to update database

# grab the files and adds them to mysql-scripts
./get-staging-db.sh

# append to the top of the file
printf "Updating sat-local-db pipelineStaging ...\n"
echo 'DROP DATABASE IF EXISTS `pipelineStaging`;\nCREATE DATABASE  IF NOT EXISTS `pipelineStaging` /*!40100 DEFAULT CHARACTER SET latin1 */;\nUSE `pipelineStaging`;' | \
        cat - ./mysql-scripts/pipelineStaging.sql > temp && mv temp ./mysql-scripts/pipelineStaging.sql

# mysql --defaults-group-suffix=local < /database/mysql-scripts/dockEventsStaging.sql

status=$?

if [ "$status" -eq "0" ]; then
    
    pv ./mysql-scripts/pipelineStaging.sql | mysql --defaults-group-suffix=local
    printf "dumping of pipelineStaging Successful!\n"
else
    printf "FAILLED!!!"
    exit 1
fi 

# append to the top of the file
printf "Updating sat-local-db dockv5Staging ...\n"
echo 'DROP DATABASE IF EXISTS `dockv5Staging`;\nCREATE DATABASE  IF NOT EXISTS `dockv5Staging` /*!40100 DEFAULT CHARACTER SET latin1 */;\nUSE `dockv5Staging`;' | \
        cat - ./mysql-scripts/dockv5Staging.sql > temp && mv temp ./mysql-scripts/dockv5Staging.sql

# mysql --defaults-group-suffix=local < /database/mysql-scripts/dockEventsStaging.sql

status=$?

if [ "$status" -eq "0" ]; then
    
    pv ./mysql-scripts/dockv5Staging.sql | mysql --defaults-group-suffix=local
    printf "dumping of dockv5Staging Successful!\n"
else
    printf "FAILLED!!!"
    exit 1
fi 

# append to the top of the file
printf "Updating sat-local-db dockEventsStaging ...\n"
echo 'DROP DATABASE IF EXISTS `dockEventsStaging`;\nCREATE DATABASE  IF NOT EXISTS `dockEventsStaging` /*!40100 DEFAULT CHARACTER SET latin1 */;\nUSE `dockEventsStaging`;' | \
        cat - ./mysql-scripts/dockEventsStaging.sql > temp && mv temp ./mysql-scripts/dockEventsStaging.sql

# mysql --defaults-group-suffix=local < /database/mysql-scripts/dockEventsStaging.sql

status=$?

if [ "$status" -eq "0" ]; then
    
    pv ./mysql-scripts/dockEventsStaging.sql | mysql --defaults-group-suffix=local
    printf "dumping of dockEventsStaging Successful!\n"
else
    printf "FAILLED!!!"
    exit 1
fi 





exit $status