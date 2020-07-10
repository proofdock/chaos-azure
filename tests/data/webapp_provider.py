from pdchaosazure.machine.constants import RES_TYPE_VM


def default():
    return {
        'name': 'chaos-webapp',
        'resourceGroup': 'rg',
        'type': RES_TYPE_VM,
    }


def real_world_sample():
    return {
        'id': '/subscriptions/05aaaafa-6951/resourceGroups/webapps/providers/Microsoft.Web/sites/proofdock',
        'sku': None, 'name': 'proofdock', 'type': 'microsoft.web/sites', 'kind': 'app,linux,container', 'plan': None,
        'tags': {}, 'location': 'westeurope',
        'properties': {
            'name': 'proofdock', 'privateEndpointConnections': [], 'enabled': True,
            'hostingEnvironmentProfile': None, 'state': 'Running', 'domainVerificationIdentifiers': None,
            'hostingEnvironmentId': None,
            'possibleOutboundIpAddresses': '13.69.68.43,13.94.143.214,13.94.150.186,13.94.151.22,13.69.121.116,'
                                           '13.94.137.26,40.68.188.89,13.94.142.40,13.94.144.225,104.214.221.75',
            'functionExecutionUnitsCache': None, 'storageRecoveryDefaultState': 'Running',
            'hostingEnvironment': None,
            'customDomainVerificationId': '382B835A0928C92D189B91C902B9F56BD64CEDA26CF89382AC8B51C8B5280CE4',
            'possibleInboundIpAddresses': '13.69.68.43', 'runtimeAvailabilityState': 'Normal',
            'contentAvailabilityState': 'Normal', 'clientCertExclusionPaths': None,
            'trafficManagerHostNames': None, 'inProgressOperationId': None, 'clientAffinityEnabled': False,
            'dailyMemoryTimeQuota': 0, 'lastModifiedTimeUtc': '2020-05-25T13:04:03.0730000Z',
            'outboundIpAddresses': '13.69.68.43,13.94.143.214,13.94.150.186,13.94.151.22,13.69.121.116',
            'resourceGroup': 'webapps', 'scmSiteAlsoStopped': False, 'siteDisabledReason': 0,
            'repositorySiteName': 'proofdock', 'maxNumberOfWorkers': None, 'targetBuildVersion': None,
            'serverFarmId': '/subscriptions/05aaaafa-6951/resourceGroups/webapps/providers/Microsoft.Web/serverfarms'
                            '/ASP-webapps-b9e0',
            'hostNameSslStates': [
                {
                    'name': 'proofdock.azurewebsites.net', 'toUpdateIpBasedSsl': None, 'ipBasedSslResult': None,
                    'ipBasedSslState': 'NotConfigured', 'thumbprint': None, 'virtualIP': None,
                    'hostType': 'Standard', 'sslState': 'Disabled', 'toUpdate': None},
                {
                    'name': 'proofdock.scm.azurewebsites.net', 'toUpdateIpBasedSsl': None,
                    'ipBasedSslResult': None, 'ipBasedSslState': 'NotConfigured', 'thumbprint': None,
                    'virtualIP': None, 'hostType': 'Repository', 'sslState': 'Disabled', 'toUpdate': None
                }
            ],
            'availabilityState': 'Normal', 'hostNamesDisabled': False, 'clientCertEnabled': False,
            'sslCertificates': None, 'geoDistributions': None, 'inboundIpAddress': '13.69.68.43',
            'enabledHostNames': ['proofdock.azurewebsites.net', 'proofdock.scm.azurewebsites.net'],
            'computeMode': None, 'defaultHostName': 'proofdock.azurewebsites.net', 'sku': 'Free',
            'siteProperties': {
                'properties': [
                    {'name': 'LinuxFxVersion', 'value': 'DOCKER|nginx'},
                    {'name': 'WindowsFxVersion', 'value': None}
                ],
                'metadata': None,
                'appSettings': None
            },
            'redundancyMode': 'None', 'targetSwapSlot': None,
            'clientCertMode': 'Required', 'slotSwapStatus': None, 'suspendedTill': None, 'containerSize': 0,
            'deploymentId': 'proofdock', 'buildVersion': None,
            'ftpsHostName': 'ftps://waws-prod-am2-311.ftp.azurewebsites.windows.net/site/wwwroot',
            'adminEnabled': True, 'webSpace': 'webapps-WestEuropewebspace',
            'ftpUsername': 'proofdock\\$proofdock', 'cloningInfo': None, 'reserved': True, 'siteMode': None,
            'siteConfig': {
                'functionsRuntimeScaleMonitoringEnabled': None,
                'customAppPoolIdentityTenantState': None,
                'scmIpSecurityRestrictionsUseMain': None, 'customAppPoolIdentityAdminState': None,
                'detailedErrorLoggingEnabled': None, 'acrUseManagedIdentityCreds': False,
                'metadata': None, 'scmIpSecurityRestrictions': None,
                'xManagedServiceIdentityId': None, 'azureMonitorLogCategories': None,
                'acrUserManagedIdentityID': None, 'managedServiceIdentityId': None,
                'appSettings': None, 'remoteDebuggingVersion': None,
                'preWarmedInstanceCount': None, 'logsDirectorySizeLimit': None,
                'remoteDebuggingEnabled': None, 'fileChangeAuditEnabled': None,
                'ipSecurityRestrictions': None, 'runtimeADUserPassword': None,
                'use32BitWorkerProcess': None, 'requestTracingEnabled': None,
                'numberOfWorkers': None, 'javaContainerVersion': None,
                'virtualApplications': None, 'apiManagementConfig': None,
                'netFrameworkVersion': None, 'managedPipelineMode': None,
                'publishingPassword': None, 'winAuthTenantState': None,
                'publishingUsername': None, 'httpLoggingEnabled': None, 'powerShellVersion': None,
                'connectionStrings': None, 'localMySqlEnabled': None, 'winAuthAdminState': None,
                'webSocketsEnabled': None, 'autoSwapSlotName': None, 'windowsFxVersion': None,
                'defaultDocuments': None, 'websiteTimeZone': None, 'healthCheckPath': None,
                'autoHealEnabled': None, 'handlerMappings': None, 'linuxFxVersion': None,
                'tracingOptions': None, 'appCommandLine': None, 'runtimeADUser': None,
                'apiDefinition': None, 'minTlsVersion': None, 'pythonVersion': None,
                'javaContainer': None, 'autoHealRules': None, 'loadBalancing': None,
                'http20Enabled': None, 'routingRules': None, 'documentRoot': None,
                'nodeVersion': None, 'javaVersion': None, 'experiments': None, 'phpVersion': None,
                'machineKey': None, 'ftpsState': None, 'vnetName': None, 'alwaysOn': None,
                'scmType': None, 'limits': None, 'cors': None, 'push': None}, 'serverFarm': None,
            'usageState': 'Normal', 'hostNames': ['proofdock.azurewebsites.net'], 'isXenon': False,
            'httpsOnly': False,
            'selfLink': 'https://waws-prod-am2-311.api.azurewebsites.windows.net:454/subscriptions/05aaaafa-6951'
                        '/webspaces/webapps-WestEuropewebspace/sites/proofdock',
            'homeStamp': 'waws-prod-am2-311', 'hyperV': False, 'kind': 'app,linux,container', 'tags': {},
            'owner': None, 'csrs': [], 'cers': None}, 'resourceGroup': 'webapps',
        'subscriptionId': '05aaaafa-6951', 'managedBy': '', 'identity': None, 'zones': None,
        'tenantId': 'feaaaa37-5aa7-4cd9-ad12-d2b6c0751f29'}
