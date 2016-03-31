#!/bin/bash

DIR=$(dirname "${BASH_SOURCE[0]}")
FULL_DIR="$(cd "$DIR" && pwd)"
BASE_DIR=$(dirname "${FULL_DIR}")
RECIPIENTS=carstena@magenta.dk

# Check if process manager is running or not.
PSS=$(pgrep -f process_)

if [ -z "${PSS}" ]; 
then
    echo "Not running, starting ..."
    sudo -u www-data -b "${BASE_DIR}/scrapy-webscanner/start_process_manager.sh"
    sleep 30
    cat | mail -t ${RECIPIENTS} -s "Process manager genstartet"  << EOF 

    Process manager k�rte ikke p� $HOSTNAME og er genstartet.

    I �jeblikket k�rer f�lgende process_manager-processer:

    $(ps aux | grep process_)

    med venlig hilsen
    Kron-d�monen p� ${HOSTNAME}.

EOF

else 
    echo "Running"
fi
# Log file must be placed in /var/ dir from Django settings.
#VAR_DIR=$(${BASE_DIR}/webscanner_site/manage.py get_var_dir)
#LOG_FILE="${VAR_DIR}/logs/summary_report_dispatch.log"
