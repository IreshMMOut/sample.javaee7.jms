import sys

cellName = sys.argv[0]
node = sys.argv[1]
server = sys.argv[2]
queueName = "DEV.QUEUE.1"
jmsQConnFac = "jndi_JMS_BASE_QCF"
queueManager = "JMSQM1"
hostName = "mq"
port = "1414"
channel = "DEV.APP.SVRCONN"
sslConfiguration = "JMSQM1SSLConfiguration"
jmsQueueOnNode1 = "jndi_INPUT_Q"
appPath = sys.argv[3]

print "------------- ENV -------------"
print "Node : "+node
print "Server : "+server
print "-------------------------------"
scope = AdminConfig.getid("/Node:%s/" % node )
print "Using scope: %s" % scope

print "Install the application %s" % appPath
AdminApp.install(appPath, '[ -appname sample_javaee7_jms_war -contextroot sample.javaee7.jms -MapResRefToEJB [[ JMS20_Samples_P2PTEST "" sample.javaee7.jms.war,WEB-INF/web.xml jndi_JMS_BASE_QCF javax.jms.QueueConnectionFactory jndi_JMS_BASE_QCF ]] -MapModulesToServers [[ JMS20_Samples_P2PTEST sample.javaee7.jms.war,WEB-INF/web.xml WebSphere:cell='+cellName+',node='+node+',server='+server+' ]] -MapResEnvRefToRes [[ JMS20_Samples_P2PTEST "" sample.javaee7.jms.war,WEB-INF/web.xml jndi_INPUT_Q javax.jms.Queue jndi_INPUT_Q ]]]' )

AdminConfig.save( )

print "Starting application"
appManager = AdminControl.queryNames('cell=%s,node=%s,type=ApplicationManager,process=%s,*' % (cellName, node, server))
AdminControl.invoke(appManager, 'startApplication', "sample_javaee7_jms_war")

AdminConfig.save( )
