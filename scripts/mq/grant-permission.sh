#!/bin/bash

setmqaut -m JMSQM1 -t qmgr -g mqclient +connect +inq
setmqaut -m JMSQM1 -t queue -n 'DEV.**' -g mqclient +put +get +browse +inq
