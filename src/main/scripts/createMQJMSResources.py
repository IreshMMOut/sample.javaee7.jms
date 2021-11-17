import sys

busName = "DEFAULT"
cellName = sys.argv[0]
node = sys.argv[1]
server = sys.argv[2]
queueName = "Queue1"
topicspaceName = "TS1"
jmsQConnFac = "jndi_JMS_BASE_QCF"
jmsTConnFac = "jmsTCF"
jmsQueueOnNode1 = "jndi_INPUT_Q"
jmsTopicOnNode1 = "jmsTopic"
topicName = "topicDest"
clientID = "client1"
appPath = sys.argv[3]
print "------------- ENV -------------"

print "Node : "+node

print "Server : "+server

print "-------------------------------"

scope = AdminConfig.getid("/Node:%s/" % node )

print "Using scope: %s" % scope

print "Creating QueueConnectionFactory %s " % jmsQConnFac

params = "-name %s -jndiName %s" % (jmsQConnFac, jmsQConnFac)
AdminTask.createWMQConnectionFactory(scope, params)

print "Creating TopicConnectionFactory %s " % jmsTConnFac

durableSubHome = node +"."+server+"-"+busName
print durableSubHome
params = "-name %s -jndiName %s" % (jmsTConnFac, jmsTConnFac)
AdminTask.createSIBJMSConnectionFactory(scope, params )

print "Creating JMSQueue %s " % jmsQueueOnNode1

params = "-name %s -queueName %s -jndiName %s" % (jmsQueueOnNode1, queueName, jmsQueueOnNode1)
AdminTask.createSIBJMSQueue(scope, params )

print "Creating JMSTopic %s " % jmsTopicOnNode1

params = "-name %s -jndiName %s -topicName %s" % (jmsTopicOnNode1, jmsTopicOnNode1, topicName)
AdminTask.createSIBJMSTopic(scope, params )

print "Install the application %s" % appPath

AdminApp.install(appPath, '[ -appname sample_javaee7_jms_war -contextroot sample.javaee7.jms -MapResRefToEJB [[ JMS20_Samples_P2PTEST "" sample.javaee7.jms.war,WEB-INF/web.xml jndi_JMS_BASE_QCF javax.jms.QueueConnectionFactory jndi_JMS_BASE_QCF ][ JMS20_Samples_P2PTEST "" sample.javaee7.jms.war,WEB-INF/web.xml jmsTCF javax.jms.TopicConnectionFactory jmsTCF ]] -MapModulesToServers [[ JMS20_Samples_P2PTEST sample.javaee7.jms.war,WEB-INF/web.xml WebSphere:cell='+cellName+',node='+node+',server='+server+' ]] -MapResEnvRefToRes [[ JMS20_Samples_P2PTEST "" sample.javaee7.jms.war,WEB-INF/web.xml jndi_INPUT_Q javax.jms.Queue jndi_INPUT_Q ][ JMS20_Samples_P2PTEST "" sample.javaee7.jms.war,WEB-INF/web.xml jmsTopic javax.jms.Topic jmsTopic ]]]' )

AdminConfig.save( )