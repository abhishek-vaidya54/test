printf "Dumping pipelineStaging Database to ./mysql-scripts..."
mysqldump --defaults-group-suffix=staging \
            --where="1 limit 500" \
            pipelineStaging | pv -W > ./mysql-scripts/pipelineStaging.sql

status=$?

if [ "$status" -eq "0" ]; then
    printf "Dumped Successfully!\n"

else
    printf "Dump failed\n"
    exit 1
fi 

printf "Dumping dockv5Staging Database to ./mysql-scripts...\n"
mysqldump   --defaults-group-suffix=staging \
            --where="1 limit 1000" \
            dockv5Staging | pv -W > ./mysql-scripts/dockv5Staging.sql

status=$?

if [ "$status" -eq "0" ]; then
    printf "Dumped Successfully!\n"
else
    printf "Dump failed\n"
    exit 1
fi 

printf "Dumping dockEventsStaging Database to ./mysql-scripts..."
mysqldump   --defaults-group-suffix=staging \
            --where="1 limit 1000" \
            dockEventsStaging | pv -W > ./mysql-scripts/dockEventsStaging.sql

status=$?

if [ "$status" -eq "0" ]; then
    printf "Dumped Successfully!\n"
else
    printf "Dump failed\n"
    exit 1
fi 

exit $status