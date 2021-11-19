#!/bin/bash

useradd -p app app
groupadd mqclient
usermod -aG mqclient app
