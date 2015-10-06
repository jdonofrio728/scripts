#!/bin/sh

# Author: Jacob D'Onofrio
# Date: May 2015

if [ -z ${JAVA_HOME} ]; then
	echo "Please set JAVA_HOME!"
	exit 1
fi

${JAVA_HOME}/bin/java org.python.util.jython fibTest.py
exit $?

