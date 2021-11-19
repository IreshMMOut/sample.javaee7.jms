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

print "------------- ENV -------------"
print "Node : "+node
print "Server : "+server
print "-------------------------------"
scope = AdminConfig.getid("/Node:%s/" % node )
print "Using scope: %s" % scope


print "Creating SSLConfiguration"
AdminTask.createSSLConfig('[-alias JMSQM1SSLConfiguration -type JSSE -scopeName (cell):%s:(node):%s -keyStoreName NodeDefaultKeyStore -keyStoreScopeName (cell):%s:(node):%s -trustStoreName NodeDefaultTrustStore -trustStoreScopeName (cell):%s:(node):%s -serverKeyAlias default ]' %(cellName, node, cellName, node, cellName, node))
AdminTask.modifySSLConfig('[-alias JMSQM1SSLConfiguration -scopeName (cell):%s:(node):%s -keyStoreName NodeDefaultKeyStore -keyStoreScopeName (cell):%s:(node):%s -trustStoreName NodeDefaultTrustStore -trustStoreScopeName (cell):%s:(node):%s -jsseProvider IBMJSSE2 -sslProtocol SSL_TLSv2 -clientAuthentication false -clientAuthenticationSupported false -securityLevel CUSTOM -enabledCiphers SSL_RSA_WITH_AES_256_CBC_SHA256 ]' % (cellName, node, cellName, node, cellName, node))
AdminTask.retrieveSignerFromPort('[-keyStoreName NodeDefaultTrustStore -keyStoreScope (cell):%s:(node):%s -host mq -port 1414 -certificateAlias qmgr-jmsqm1 -sslConfigName NodeDefaultSSLSettings -sslConfigScopeName (cell):%s:(node):%s ]' % (cellName, node, cellName, node))



print "Creating QueueConnectionFactory %s " % jmsQConnFac
AdminJMS.createWMQQueueConnectionFactory(scope, jmsQConnFac, jmsQConnFac, [["qmgrName", queueManager], ["qmgrHostname", hostName], ["qmgrPortNumber", port], ["qmgrSvrconnChannel", channel], ["wmqTransportType", "CLIENT"], ["sslType", "SPECIFIC"], ["sslConfiguration", "JMSQM1SSLConfiguration"]]) 

print "Creating JMSQueue %s " % jmsQueueOnNode1
AdminJMS.createWMQQueue(scope, jmsQueueOnNode1, jmsQueueOnNode1, queueName, "qmgr=%s" % queueManager)

AdminConfig.save( )
