
#!/bin/bash

QMGR_NAME=$1
CERT_LABEL=$(echo $QMGR_NAME | awk '{print tolower($0)}')
if [ -z $QMGR_NAME ]; then
    echo "QMGR name is needed!"
    exit 1
fi

source /opt/mqm/bin/setmqenv -s

cd /var/mqm/qmgrs/${QMGR_NAME}/ssl

runmqakm -keydb -create -db key.kdb -pw app12345 -stash

runmqakm -cert -create -db key.kdb -stashed -sigalg SHA256WithRSA -dn "cn=qmgr,o=ireshorg,c=lk" \
    -label ibmwebspheremq${CERT_LABEL}

runmqakm -cert -extract -label ibmwebspheremq${CERT_LABEL} -db key.kdb \
    -stashed -file "${QMGR_NAME}.cert"

chmod 640 *
