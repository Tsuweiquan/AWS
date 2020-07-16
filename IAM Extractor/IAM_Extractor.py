# Written by Tsu Wei Quan
# Run this script in python3
# Requires boto3 installation with pip3
import boto3
import csv

MAX_ITEMS = 300

AWS_POLICY_NAMES = [
    'APIGatewayServiceRolePolicy', 
    'AWSAccountActivityAccess', 
    'AWSAccountUsageReportAccess', 
    'AWSAgentlessDiscoveryService',
    'AWSAppMeshEnvoyAccess', 
    'AWSAppMeshFullAccess', 
    'AWSAppMeshPreviewEnvoyAccess', 
    'AWSAppMeshPreviewServiceRolePolicy',
    'AWSAppMeshReadOnly', 
    'AWSAppMeshServiceRolePolicy', 
    'AWSAppSyncAdministrator', 
    'AWSAppSyncInvokeFullAccess', 
    'AWSAppSyncPushToCloudWatchLogs',
    'AWSAppSyncSchemaAuthor', 
    'AWSApplicationAutoScalingCustomResourcePolicy', 
    'AWSApplicationAutoscalingAppStreamFleetPolicy',
    'AWSApplicationAutoscalingComprehendEndpointPolicy',
    'AWSApplicationAutoscalingDynamoDBTablePolicy',
    'AWSApplicationAutoscalingEC2SpotFleetRequestPolicy',
    'AWSApplicationAutoscalingECSServicePolicy',
    'AWSApplicationAutoscalingEMRInstanceGroupPolicy',
    'AWSApplicationAutoscalingLambdaConcurrencyPolicy',
    'AWSApplicationAutoscalingRDSClusterPolicy',
    'AWSApplicationAutoscalingSageMakerEndpointPolicy',
    'AWSApplicationDiscoveryAgentAccess',
    'AWSApplicationDiscoveryServiceFullAccess',
    'AWSArtifactAccountSync',
    'AWSAutoScalingPlansEC2AutoScalingPolicy',
    'AWSB9InternalServicePolicy',
    'AWSBackupAdminPolicy',
    'AWSBackupOperatorPolicy',
    'AWSBackupServiceRolePolicyForBackup',
    'AWSBackupServiceRolePolicyForRestores',
    'AWSBatchFullAccess',
    'AWSBatchServiceEventTargetRole',
    'AWSBatchServiceRole',
    'AWSCertificateManagerFullAccess',
    'AWSCertificateManagerPrivateCAAuditor',
    'AWSCertificateManagerPrivateCAFullAccess',
    'AWSCertificateManagerPrivateCAPrivilegedUser',
    'AWSCertificateManagerPrivateCAReadOnly',
    'AWSCertificateManagerPrivateCAUser',
    'AWSCertificateManagerReadOnly',
    'AWSChatbotServiceLinkedRolePolicy',
    'AWSCloud9Administrator',
    'AWSCloud9EnvironmentMember',
    'AWSCloud9ServiceRolePolicy',
    'AWSCloud9User',
    'AWSCloudFormationFullAccess',
    'AWSCloudFormationReadOnlyAccess',
    'AWSCloudFrontLogger',
    'AWSCloudHSMFullAccess',
    'AWSCloudHSMReadOnlyAccess',
    'AWSCloudHSMRole',
    'AWSCloudMapDiscoverInstanceAccess',
    'AWSCloudMapFullAccess',
    'AWSCloudMapReadOnlyAccess',
    'AWSCloudMapRegisterInstanceAccess',
    'AWSCloudTrailFullAccess',
    'AWSCloudTrailReadOnlyAccess',
    'AWSCodeBuildAdminAccess',
    'AWSCodeBuildDeveloperAccess',
    'AWSCodeBuildReadOnlyAccess',
    'AWSCodeCommitFullAccess',
    'AWSCodeCommitPowerUser',
    'AWSCodeCommitReadOnly',
    'AWSCodeDeployDeployerAccess',
    'AWSCodeDeployFullAccess',
    'AWSCodeDeployReadOnlyAccess',
    'AWSCodeDeployRole',
    'AWSCodeDeployRoleForECS',
    'AWSCodeDeployRoleForECSLimited',
    'AWSCodeDeployRoleForLambda',
    'AWSCodePipelineApproverAccess',
    'AWSCodePipelineCustomActionAccess',
    'AWSCodePipelineFullAccess',
    'AWSCodePipelineReadOnlyAccess',
    'AWSCodeStarFullAccess',
    'AWSCodeStarNotificationsServiceRolePolicy',
    'AWSCodeStarServiceRole',
    'AWSConfigMultiAccountSetupPolicy',
    'AWSConfigRemediationServiceRolePolicy',
    'AWSConfigRole',
    'AWSConfigRoleForOrganizations',
    'AWSConfigRulesExecutionRole',
    'AWSConfigServiceRolePolicy',
    'AWSConfigUserAccess',
    'AWSConnector',
    'AWSControlTowerServiceRolePolicy',
    'AWSDataExchangeFullAccess',
    'AWSDataExchangeProviderFullAccess',
    'AWSDataExchangeReadOnly',
    'AWSDataExchangeSubscriberFullAccess',
    'AWSDataLifecycleManagerServiceRole',
    'AWSDataPipelineRole',
    'AWSDataPipeline_FullAccess',
    'AWSDataPipeline_PowerUser',
    'AWSDataSyncFullAccess',
    'AWSDataSyncReadOnlyAccess',
    'AWSDeepLensLambdaFunctionAccessPolicy',
    'AWSDeepLensServiceRolePolicy',
    'AWSDeepRacerCloudFormationAccessPolicy',
    'AWSDeepRacerRoboMakerAccessPolicy',
    'AWSDeepRacerServiceRolePolicy',
    'AWSDenyAll',
    'AWSDeviceFarmFullAccess',
    'AWSDirectConnectFullAccess',
    'AWSDirectConnectReadOnlyAccess',
    'AWSDirectoryServiceFullAccess',
    'AWSDirectoryServiceReadOnlyAccess',
    'AWSDiscoveryContinuousExportFirehosePolicy',
    'AWSEC2FleetServiceRolePolicy',
    'AWSEC2SpotFleetServiceRolePolicy',
    'AWSEC2SpotServiceRolePolicy',
    'AWSElasticBeanstalkCustomPlatformforEC2Role',
    'AWSElasticBeanstalkEnhancedHealth',
    'AWSElasticBeanstalkFullAccess',
    'AWSElasticBeanstalkMaintenance',
    'AWSElasticBeanstalkMulticontainerDocker',
    'AWSElasticBeanstalkReadOnlyAccess',
    'AWSElasticBeanstalkService',
    'AWSElasticBeanstalkServiceRolePolicy',
    'AWSElasticBeanstalkWebTier',
    'AWSElasticBeanstalkWorkerTier',
    'AWSElasticLoadBalancingClassicServiceRolePolicy',
    'AWSElasticLoadBalancingServiceRolePolicy',
    'AWSElementalMediaConvertFullAccess',
    'AWSElementalMediaConvertReadOnly',
    'AWSElementalMediaPackageFullAccess',
    'AWSElementalMediaPackageReadOnly',
    'AWSElementalMediaStoreFullAccess',
    'AWSElementalMediaStoreReadOnly',
    'AWSEnhancedClassicNetworkingMangementPolicy',
    'AWSFMAdminFullAccess',
    'AWSFMAdminReadOnlyAccess',
    'AWSFMMemberReadOnlyAccess',
    'AWSForWordPressPluginPolicy',
    'AWSGlobalAcceleratorSLRPolicy',
    'AWSGlueConsoleFullAccess',
    'AWSGlueConsoleSageMakerNotebookFullAccess',
    'AWSGlueServiceNotebookRole',
    'AWSGlueServiceRole',
    'AWSGreengrassFullAccess',
    'AWSGreengrassReadOnlyAccess',
    'AWSGreengrassResourceAccessRolePolicy',
    'AWSHealthFullAccess',
    'AWSIQContractServiceRolePolicy',
    'AWSIQFullAccess',
    'AWSIQPermissionServiceRolePolicy',
    'AWSImportExportFullAccess',
    'AWSImportExportReadOnlyAccess',
    'AWSIoT1ClickFullAccess',
    'AWSIoT1ClickReadOnlyAccess',
    'AWSIoTAnalyticsFullAccess',
    'AWSIoTAnalyticsReadOnlyAccess',
    'AWSIoTConfigAccess',
    'AWSIoTConfigReadOnlyAccess',
    'AWSIoTDataAccess',
    'AWSIoTDeviceDefenderAddThingsToThingGroupMitigationAction',
    'AWSIoTDeviceDefenderAudit',
    'AWSIoTDeviceDefenderEnableIoTLoggingMitigationAction',
    'AWSIoTDeviceDefenderPublishFindingsToSNSMitigationAction',
    'AWSIoTDeviceDefenderReplaceDefaultPolicyMitigationAction',
    'AWSIoTDeviceDefenderUpdateCACertMitigationAction',
    'AWSIoTDeviceDefenderUpdateDeviceCertMitigationAction',
    'AWSIoTEventsFullAccess',
    'AWSIoTEventsReadOnlyAccess',
    'AWSIoTFullAccess',
    'AWSIoTLogging',
    'AWSIoTOTAUpdate',
    'AWSIoTRuleActions',
    'AWSIoTSiteWiseConsoleFullAccess',
    'AWSIoTSiteWiseFullAccess',
    'AWSIoTSiteWiseMonitorServiceRolePolicy',
    'AWSIoTSiteWiseReadOnlyAccess',
    'AWSIoTThingsRegistration',
    'AWSKeyManagementServiceCustomKeyStoresServiceRolePolicy',
    'AWSKeyManagementServicePowerUser',
    'AWSLakeFormationDataAdmin',
    'AWSLambdaBasicExecutionRole',
    'AWSLambdaDynamoDBExecutionRole',
    'AWSLambdaENIManagementAccess',
    'AWSLambdaExecute',
    'AWSLambdaFullAccess',
    'AWSLambdaInvocation-DynamoDB',
    'AWSLambdaKinesisExecutionRole',
    'AWSLambdaReadOnlyAccess',
    'AWSLambdaReplicator',
    'AWSLambdaRole',
    'AWSLambdaSQSQueueExecutionRole',
    'AWSLambdaVPCAccessExecutionRole',
    'AWSLicenseManagerMasterAccountRolePolicy',
    'AWSLicenseManagerMemberAccountRolePolicy',
    'AWSLicenseManagerServiceRolePolicy',
    'AWSMarketplaceFullAccess',
    'AWSMarketplaceGetEntitlements',
    'AWSMarketplaceImageBuildFullAccess',
    'AWSMarketplaceManageSubscriptions',
    'AWSMarketplaceMeteringFullAccess',
    'AWSMarketplaceProcurementSystemAdminFullAccess',
    'AWSMarketplaceRead-only',
    'AWSMarketplaceSellerFullAccess',
    'AWSMarketplaceSellerProductsFullAccess',
    'AWSMarketplaceSellerProductsReadOnly',
    'AWSMigrationHubDMSAccess',
    'AWSMigrationHubDiscoveryAccess',
    'AWSMigrationHubFullAccess',
    'AWSMigrationHubSMSAccess',
    'AWSMobileHub_FullAccess',
    'AWSMobileHub_ReadOnly',
    'AWSOpsWorksCMInstanceProfileRole',
    'AWSOpsWorksCMServiceRole',
    'AWSOpsWorksCloudWatchLogs',
    'AWSOpsWorksFullAccess',
    'AWSOpsWorksInstanceRegistration',
    'AWSOpsWorksRegisterCLI_EC2',
    'AWSOpsWorksRegisterCLI_OnPremises',
    'AWSOpsWorksRole',
    'AWSOrganizationsFullAccess',
    'AWSOrganizationsReadOnlyAccess',
    'AWSOrganizationsServiceTrustPolicy',
    'AWSPriceListServiceFullAccess',
    'AWSPrivateMarketplaceAdminFullAccess',
    'AWSPrivateMarketplaceRequests',
    'AWSQuickSightDescribeRDS',
    'AWSQuickSightDescribeRedshift',
    'AWSQuickSightIoTAnalyticsAccess',
    'AWSQuickSightListIAM',
    'AWSQuicksightAthenaAccess',
    'AWSResourceAccessManagerFullAccess',
    'AWSResourceAccessManagerServiceRolePolicy',
    'AWSResourceGroupsReadOnlyAccess',
    'AWSRoboMakerFullAccess',
    'AWSRoboMakerReadOnlyAccess',
    'AWSRoboMakerServicePolicy',
    'AWSRoboMakerServiceRolePolicy',
    'AWSSSODirectoryAdministrator',
    'AWSSSODirectoryReadOnly',
    'AWSSSOMasterAccountAdministrator',
    'AWSSSOMemberAccountAdministrator',
    'AWSSSOReadOnly',
    'AWSSSOServiceRolePolicy',
    'AWSSavingsPlansFullAccess',
    'AWSSavingsPlansReadOnlyAccess',
    'AWSSchemasServiceRolePolicy',
    'AWSSecurityHubFullAccess',
    'AWSSecurityHubReadOnlyAccess',
    'AWSSecurityHubServiceRolePolicy',
    'AWSServiceCatalogAdminFullAccess',
    'AWSServiceCatalogAdminReadOnlyAccess',
    'AWSServiceCatalogEndUserFullAccess',
    'AWSServiceCatalogEndUserReadOnlyAccess',
    'AWSServiceRoleForAmazonEKSNodegroup',
    'AWSServiceRoleForEC2ScheduledInstances',
    'AWSServiceRoleForIoTSiteWise',
    'AWSServiceRoleForLogDeliveryPolicy',
    'AWSServiceRoleForSMS',
    'AWSShieldDRTAccessPolicy',
    'AWSStepFunctionsConsoleFullAccess',
    'AWSStepFunctionsFullAccess',
    'AWSStepFunctionsReadOnlyAccess',
    'AWSStorageGatewayFullAccess',
    'AWSStorageGatewayReadOnlyAccess',
    'AWSSupportAccess',
    'AWSSupportServiceRolePolicy',
    'AWSSystemsManagerAccountDiscoveryServicePolicy',
    'AWSTransferLoggingAccess',
    'AWSTrustedAdvisorServiceRolePolicy',
    'AWSVPCS2SVpnServiceRolePolicy',
    'AWSVPCTransitGatewayServiceRolePolicy',
    'AWSWAFFullAccess',
    'AWSWAFReadOnlyAccess',
    'AWSXRayDaemonWriteAccess',
    'AWSXrayFullAccess',
    'AWSXrayReadOnlyAccess',
    'AWSXrayWriteOnlyAccess',
    'AdministratorAccess',
    'AlexaForBusinessDeviceSetup',
    'AlexaForBusinessFullAccess',
    'AlexaForBusinessGatewayExecution',
    'AlexaForBusinessNetworkProfileServicePolicy',
    'AlexaForBusinessPolyDelegatedAccessPolicy',
    'AlexaForBusinessReadOnlyAccess',
    'AmazonAPIGatewayAdministrator',
    'AmazonAPIGatewayInvokeFullAccess',
    'AmazonAPIGatewayPushToCloudWatchLogs',
    'AmazonAppStreamFullAccess',
    'AmazonAppStreamReadOnlyAccess',
    'AmazonAppStreamServiceAccess',
    'AmazonAthenaFullAccess',
    'AmazonChimeFullAccess',
    'AmazonChimeReadOnly',
    'AmazonChimeServiceRolePolicy',
    'AmazonChimeUserManagement',
    'AmazonChimeVoiceConnectorServiceLinkedRolePolicy',
    'AmazonCloudDirectoryFullAccess',
    'AmazonCloudDirectoryReadOnlyAccess',
    'AmazonCognitoDeveloperAuthenticatedIdentities',
    'AmazonCognitoIdpEmailServiceRolePolicy',
    'AmazonCognitoPowerUser',
    'AmazonCognitoReadOnly',
    'AmazonConnectFullAccess',
    'AmazonConnectReadOnlyAccess',
    'AmazonConnectServiceLinkedRolePolicy',
    'AmazonDMSCloudWatchLogsRole',
    'AmazonDMSRedshiftS3Role',
    'AmazonDMSVPCManagementRole',
    'AmazonDRSVPCManagement',
    'AmazonDocDBConsoleFullAccess',
    'AmazonDocDBFullAccess',
    'AmazonDocDBReadOnlyAccess',
    'AmazonDynamoDBFullAccess',
    'AmazonDynamoDBFullAccesswithDataPipeline',
    'AmazonDynamoDBReadOnlyAccess',
    'AmazonEC2ContainerRegistryFullAccess',
    'AmazonEC2ContainerRegistryPowerUser',
    'AmazonEC2ContainerRegistryReadOnly',
    'AmazonEC2ContainerServiceAutoscaleRole',
    'AmazonEC2ContainerServiceEventsRole',
    'AmazonEC2ContainerServiceFullAccess',
    'AmazonEC2ContainerServiceRole',
    'AmazonEC2ContainerServiceforEC2Role',
    'AmazonEC2FullAccess',
    'AmazonEC2ReadOnlyAccess',
    'AmazonEC2ReportsAccess',
    'AmazonEC2RolePolicyForLaunchWizard',
    'AmazonEC2RoleforAWSCodeDeploy',
    'AmazonEC2RoleforDataPipelineRole',
    'AmazonEC2RoleforSSM',
    'AmazonEC2SpotFleetAutoscaleRole',
    'AmazonEC2SpotFleetTaggingRole',
    'AmazonECSServiceRolePolicy',
    'AmazonECSTaskExecutionRolePolicy',
    'AmazonECS_FullAccess',
    'AmazonEKSClusterPolicy',
    'AmazonEKSServicePolicy',
    'AmazonEKSWorkerNodePolicy',
    'AmazonEKS_CNI_Policy',
    'AmazonEMRCleanupPolicy',
    'AmazonESCognitoAccess',
    'AmazonESFullAccess',
    'AmazonESReadOnlyAccess',
    'AmazonElastiCacheFullAccess',
    'AmazonElastiCacheReadOnlyAccess',
    'AmazonElasticFileSystemFullAccess',
    'AmazonElasticFileSystemReadOnlyAccess',
    'AmazonElasticFileSystemServiceRolePolicy',
    'AmazonElasticMapReduceEditorsRole',
    'AmazonElasticMapReduceFullAccess',
    'AmazonElasticMapReduceReadOnlyAccess',
    'AmazonElasticMapReduceRole',
    'AmazonElasticMapReduceforAutoScalingRole',
    'AmazonElasticMapReduceforEC2Role',
    'AmazonElasticTranscoderRole',
    'AmazonElasticTranscoder_FullAccess',
    'AmazonElasticTranscoder_JobsSubmitter',
    'AmazonElasticTranscoder_ReadOnlyAccess',
    'AmazonElasticsearchServiceRolePolicy',
    'AmazonEventBridgeFullAccess',
    'AmazonEventBridgeReadOnlyAccess',
    'AmazonFSxConsoleFullAccess',
    'AmazonFSxConsoleReadOnlyAccess',
    'AmazonFSxFullAccess',
    'AmazonFSxReadOnlyAccess',
    'AmazonFSxServiceRolePolicy',
    'AmazonForecastFullAccess',
    'AmazonFreeRTOSFullAccess',
    'AmazonFreeRTOSOTAUpdate',
    'AmazonGlacierFullAccess',
    'AmazonGlacierReadOnlyAccess',
    'AmazonGuardDutyFullAccess',
    'AmazonGuardDutyReadOnlyAccess',
    'AmazonGuardDutyServiceRolePolicy',
    'AmazonInspectorFullAccess',
    'AmazonInspectorReadOnlyAccess',
    'AmazonInspectorServiceRolePolicy',
    'AmazonKinesisAnalyticsFullAccess',
    'AmazonKinesisAnalyticsReadOnly',
    'AmazonKinesisFirehoseFullAccess',
    'AmazonKinesisFirehoseReadOnlyAccess',
    'AmazonKinesisFullAccess',
    'AmazonKinesisReadOnlyAccess',
    'AmazonKinesisVideoStreamsFullAccess',
    'AmazonKinesisVideoStreamsReadOnlyAccess',
    'AmazonLaunchWizardFullaccess',
    'AmazonLexFullAccess',
    'AmazonLexReadOnly',
    'AmazonLexRunBotsOnly',
    'AmazonMQApiFullAccess',
    'AmazonMQApiReadOnlyAccess',
    'AmazonMQFullAccess',
    'AmazonMQReadOnlyAccess',
    'AmazonMSKFullAccess',
    'AmazonMSKReadOnlyAccess',
    'AmazonMachineLearningBatchPredictionsAccess',
    'AmazonMachineLearningCreateOnlyAccess',
    'AmazonMachineLearningFullAccess',
    'AmazonMachineLearningManageRealTimeEndpointOnlyAccess',
    'AmazonMachineLearningReadOnlyAccess',
    'AmazonMachineLearningRealTimePredictionOnlyAccess',
    'AmazonMachineLearningRoleforRedshiftDataSourceV2',
    'AmazonMacieFullAccess',
    'AmazonMacieHandshakeRole',
    'AmazonMacieServiceRole',
    'AmazonMacieServiceRolePolicy',
    'AmazonMacieSetupRole',
    'AmazonManagedBlockchainConsoleFullAccess',
    'AmazonManagedBlockchainFullAccess',
    'AmazonManagedBlockchainReadOnlyAccess',
    'AmazonMechanicalTurkFullAccess',
    'AmazonMechanicalTurkReadOnly',
    'AmazonMobileAnalyticsFinancialReportAccess',
    'AmazonMobileAnalyticsFullAccess',
    'AmazonMobileAnalyticsNon-financialReportAccess',
    'AmazonMobileAnalyticsWriteOnlyAccess',
    'AmazonPersonalizeFullAccess',
    'AmazonPollyFullAccess',
    'AmazonPollyReadOnlyAccess',
    'AmazonQLDBConsoleFullAccess',
    'AmazonQLDBFullAccess',
    'AmazonQLDBReadOnly',
    'AmazonRDSBetaServiceRolePolicy',
    'AmazonRDSDataFullAccess',
    'AmazonRDSDirectoryServiceAccess',
    'AmazonRDSEnhancedMonitoringRole',
    'AmazonRDSFullAccess',
    'AmazonRDSPreviewServiceRolePolicy',
    'AmazonRDSReadOnlyAccess',
    'AmazonRDSServiceRolePolicy',
    'AmazonRedshiftFullAccess',
    'AmazonRedshiftQueryEditor',
    'AmazonRedshiftReadOnlyAccess',
    'AmazonRedshiftServiceLinkedRolePolicy',
    'AmazonRekognitionFullAccess',
    'AmazonRekognitionReadOnlyAccess',
    'AmazonRekognitionServiceRole',
    'AmazonRoute53AutoNamingFullAccess',
    'AmazonRoute53AutoNamingReadOnlyAccess',
    'AmazonRoute53AutoNamingRegistrantAccess',
    'AmazonRoute53DomainsFullAccess',
    'AmazonRoute53DomainsReadOnlyAccess',
    'AmazonRoute53FullAccess',
    'AmazonRoute53ReadOnlyAccess',
    'AmazonRoute53ResolverFullAccess',
    'AmazonRoute53ResolverReadOnlyAccess',
    'AmazonS3FullAccess',
    'AmazonS3ReadOnlyAccess',
    'AmazonSESFullAccess',
    'AmazonSESReadOnlyAccess',
    'AmazonSNSFullAccess',
    'AmazonSNSReadOnlyAccess',
    'AmazonSNSRole',
    'AmazonSQSFullAccess',
    'AmazonSQSReadOnlyAccess',
    'AmazonSSMAutomationApproverAccess',
    'AmazonSSMAutomationRole',
    'AmazonSSMDirectoryServiceAccess',
    'AmazonSSMFullAccess',
    'AmazonSSMMaintenanceWindowRole',
    'AmazonSSMManagedInstanceCore',
    'AmazonSSMReadOnlyAccess',
    'AmazonSSMServiceRolePolicy',
    'AmazonSageMakerFullAccess',
    'AmazonSageMakerNotebooksServiceRolePolicy',
    'AmazonSageMakerReadOnly',
    'AmazonSumerianFullAccess',
    'AmazonTextractFullAccess',
    'AmazonTextractServiceRole',
    'AmazonTranscribeFullAccess',
    'AmazonTranscribeReadOnlyAccess',
    'AmazonVPCCrossAccountNetworkInterfaceOperations',
    'AmazonVPCFullAccess',
    'AmazonVPCReadOnlyAccess',
    'AmazonWorkLinkFullAccess',
    'AmazonWorkLinkReadOnly',
    'AmazonWorkLinkServiceRolePolicy',
    'AmazonWorkMailEventsServiceRolePolicy',
    'AmazonWorkMailFullAccess',
    'AmazonWorkMailReadOnlyAccess',
    'AmazonWorkSpacesAdmin',
    'AmazonWorkSpacesApplicationManagerAdminAccess',
    'AmazonWorkSpacesSelfServiceAccess',
    'AmazonWorkSpacesServiceAccess',
    'AmazonZocaloFullAccess',
    'AmazonZocaloReadOnlyAccess',
    'ApplicationAutoScalingForAmazonAppStreamAccess',
    'ApplicationDiscoveryServiceContinuousExportServiceRolePolicy',
    'AutoScalingConsoleFullAccess',
    'AutoScalingConsoleReadOnlyAccess',
    'AutoScalingFullAccess',
    'AutoScalingNotificationAccessRole',
    'AutoScalingReadOnlyAccess',
    'AutoScalingServiceRolePolicy',
    'Billing',
    'ClientVPNServiceRolePolicy',
    'CloudFrontFullAccess',
    'CloudFrontReadOnlyAccess',
    'CloudHSMServiceRolePolicy',
    'CloudSearchFullAccess',
    'CloudSearchReadOnlyAccess',
    'CloudTrailServiceRolePolicy',
    'CloudWatch-CrossAccountAccess',
    'CloudWatchActionsEC2Access',
    'CloudWatchAgentAdminPolicy',
    'CloudWatchAgentServerPolicy',
    'CloudWatchAutomaticDashboardsAccess',
    'CloudWatchEventsBuiltInTargetExecutionAccess',
    'CloudWatchEventsFullAccess',
    'CloudWatchEventsInvocationAccess',
    'CloudWatchEventsReadOnlyAccess',
    'CloudWatchEventsServiceRolePolicy',
    'CloudWatchFullAccess',
    'CloudWatchLogsFullAccess',
    'CloudWatchLogsReadOnlyAccess',
    'CloudWatchReadOnlyAccess',
    'CloudwatchApplicationInsightsServiceLinkedRolePolicy',
    'ComprehendDataAccessRolePolicy',
    'ComprehendFullAccess',
    'ComprehendMedicalFullAccess',
    'ComprehendReadOnly',
    'ConfigConformsServiceRolePolicy',
    'DAXServiceRolePolicy',
    'DataScientist',
    'DatabaseAdministrator',
    'DynamoDBCloudWatchContributorInsightsServiceRolePolicy',
    'DynamoDBReplicationServiceRolePolicy',
    'EC2InstanceConnect',
    'ElastiCacheServiceRolePolicy',
    'ElasticLoadBalancingFullAccess',
    'ElasticLoadBalancingReadOnly',
    'ElementalAppliancesSoftwareFullAccess',
    'FMSServiceRolePolicy',
    'FSxDeleteServiceLinkedRoleAccess',
    'GlobalAcceleratorFullAccess',
    'GlobalAcceleratorReadOnlyAccess',
    'GreengrassOTAUpdateArtifactAccess',
    'IAMAccessAdvisorReadOnly',
    'IAMFullAccess',
    'IAMReadOnlyAccess',
    'IAMSelfManageServiceSpecificCredentials',
    'IAMUserChangePassword',
    'IAMUserSSHKeys',
    'KafkaServiceRolePolicy',
    'LakeFormationDataAccessServiceRolePolicy',
    'LexBotPolicy',
    'LexChannelPolicy',
    'LightsailExportAccess',
    'MigrationHubDMSAccessServiceRolePolicy',
    'MigrationHubSMSAccessServiceRolePolicy',
    'MigrationHubServiceRolePolicy',
    'NeptuneConsoleFullAccess',
    'NeptuneFullAccess',
    'NeptuneReadOnlyAccess',
    'NetworkAdministrator',
    'PowerUserAccess',
    'QuickSightAccessForS3StorageManagementAnalyticsReadOnly',
    'RDSCloudHsmAuthorizationRole',
    'ReadOnlyAccess',
    'ResourceGroupsandTagEditorFullAccess',
    'ResourceGroupsandTagEditorReadOnlyAccess',
    'SecretsManagerReadWrite',
    'SecurityAudit',
    'ServerMigrationConnector',
    'ServerMigrationServiceLaunchRole',
    'ServerMigrationServiceRole',
    'ServiceQuotasFullAccess',
    'ServiceQuotasReadOnlyAccess',
    'ServiceQuotasServiceRolePolicy',
    'SimpleWorkflowFullAccess',
    'SupportUser',
    'SystemAdministrator',
    'TagPoliciesServiceRolePolicy',
    'TranslateFullAccess',
    'TranslateReadOnly',
    'VMImportExportRoleForAWSConnector',
    'ViewOnlyAccess',
    'WAFLoggingServiceRolePolicy',
    'WAFRegionalLoggingServiceRolePolicy',
    'WAFV2LoggingServiceRolePolicy',
    'WellArchitectedConsoleFullAccess',
    'WellArchitectedConsoleReadOnlyAccess',
    'WorkLinkServiceRolePolicy'
]

# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html

def concatTagValues(dataList):
    for i in dataList:
        Key = i['Key']
        Value = i['Value']
        KeyValuePair = Key + ":" + Value
        myTags = myTags + KeyValuePair + ", "
    return myTags

def concatListToString(policyList):
    separator = ', '
    return separator.join(policyList)

def concatListToStringForced(List):
    separator = ', '
    return separator.join(map(str, List))

# Input: List of dictionaries | Output: List of values from 'PolicyName' Key
def extractValueFromListDictionaryPair(policyList, Key):
    newPolicyList = []
    for i in policyList:
        newPolicyList.append(i[Key])
    return newPolicyList

class User:
    def __init__(self, client, csvWriter):
        self.client = client
        self.csvWriter = csvWriter
    
    def list_all_users(self):
        response = self.client.list_users(
            # PathPrefix=PATH_PREFIX,
            # Marker=MARKER,
            MaxItems=MAX_ITEMS
        )
        return response

    def list_groups_for_user(self, username):
        response = client.list_groups_for_user(
            UserName=username,
            # Marker='string',
            MaxItems=MAX_ITEMS
        )
        userGroups = response['Groups']
        if len(userGroups):
            listOfGroups = extractValueFromListDictionaryPair(userGroups, 'GroupName')
            listOfGroups = concatListToString(listOfGroups)
        else:
            listOfGroups = "EMPTY"
        return listOfGroups

    
    def list_user_inline_policies(self, username):
        response = client.list_user_policies(
            UserName=username,
            # Marker='string',
            MaxItems=MAX_ITEMS
        )
        inlinePolicyList = response['PolicyNames']
        if len(inlinePolicyList):
            return concatListToString(inlinePolicyList)
        else:
            return "EMPTY"

    # this function obtains the User's individual customer managed policies + AWS managed policies
    def list_user_managed_policies(self, username):
        response = client.list_attached_user_policies(
            UserName=username,
            # PathPrefix='string',
            # Marker='string',
            MaxItems=MAX_ITEMS
        )
        managedPolicyList = response['AttachedPolicies']
        if len(managedPolicyList):
            listOfPolicies = extractValueFromListDictionaryPair(managedPolicyList, 'PolicyName')
            return listOfPolicies
        else:
            return "EMPTY"

    def get_AWS_managed_policies(self, listOfPolicies):
        if listOfPolicies != "EMPTY":
            awsManagedPolicies = list(set(AWS_POLICY_NAMES).intersection(listOfPolicies))
            if not awsManagedPolicies:
                return "EMPTY"
            else:
                return concatListToString(awsManagedPolicies)
        else:
            return "EMPTY"

    def get_customer_managed_policies(self, listOfPolicies):
        if listOfPolicies != "EMPTY":
            AWS_POLICY_SET = set(AWS_POLICY_NAMES)
            customerManagedPolicies = (item for item in listOfPolicies if item not in AWS_POLICY_SET)
            if not customerManagedPolicies:
                return "EMPTY"
            else:
                return concatListToString(customerManagedPolicies)
        else:
            return "EMPTY"

    def list_access_public_keys(self, username):
        response = client.list_access_keys(
            UserName=username,
            # Marker='string',
            MaxItems=MAX_ITEMS
        )
        myAccessKeys = response['AccessKeyMetadata']
        if len(myAccessKeys):
            numOfAccessKeys = len(myAccessKeys)
            listOfAccessKeyId = extractValueFromListDictionaryPair(myAccessKeys, 'AccessKeyId')
            listOfAccessKeyIdStatus = extractValueFromListDictionaryPair(myAccessKeys, 'Status')
            listOfAccessKeyCreationDate = extractValueFromListDictionaryPair(myAccessKeys, 'CreateDate')
            publicKeyIds = concatListToString(listOfAccessKeyId)
            publicKeyIdStatus = concatListToString(listOfAccessKeyIdStatus)
            publicKeyCreationDates = concatListToStringForced(listOfAccessKeyCreationDate)
            return numOfAccessKeys, publicKeyIds, publicKeyIdStatus, publicKeyCreationDates
        else:
            return 0, "EMPTY", "EMPTY", "EMPTY"

    def list_my_mfa_devices(self, username):
        response = client.list_mfa_devices(
            UserName=username,
            # Marker='string',
            MaxItems=MAX_ITEMS
        )
        myMFADevices = response['MFADevices']
        if len(myMFADevices):
            numMFADevices = len(myMFADevices)
            listOfMFADevices = extractValueFromListDictionaryPair(myMFADevices, 'SerialNumber')
            listOfMFAEnabledDate = extractValueFromListDictionaryPair(myMFADevices, 'EnableDate')
            MFADevices = concatListToString(listOfMFADevices)
            MFADevicesEnabledDate = concatListToStringForced(listOfMFAEnabledDate)
            return numMFADevices, MFADevices, MFADevicesEnabledDate
        else:
            return 0, "EMPTY", "EMPTY"

    def list_user_signing_certificates(self, username):
        response = client.list_signing_certificates(
            UserName=username,
            # Marker='string',
            MaxItems=MAX_ITEMS
        )
        mySignedCerts = response['Certificates']
        if len(mySignedCerts):
            numSignedCerts = len(mySignedCerts)
            listOfCertificateId = extractValueFromListDictionaryPair(mySignedCerts, 'CertificateId')
            listOfCertificateBody = extractValueFromListDictionaryPair(mySignedCerts, 'CertificateBody')
            listOfCertificateStatus = extractValueFromListDictionaryPair(mySignedCerts, 'Status')
            listOfCertificateUploadDate = extractValueFromListDictionaryPair(mySignedCerts, 'UploadDate')
            certificateIds = concatListToString(listOfCertificateId)
            certificateBody = concatListToString(listOfCertificateBody)
            certificateStatus = concatListToString(listOfCertificateStatus)
            certificateUploadDate = concatListToString(listOfCertificateUploadDate)
            return numSignedCerts, certificateIds, certificateBody, certificateStatus, certificateUploadDate
        else:
            return 0, "EMPTY", "EMPTY", "EMPTY", "EMPTY"

    def list_all_users_info_to_csv(self, response):
        writer.writerow(['UserName', 'UserId', 'Arn', 'CreateDate', 'PasswordLastUsed', 'PermissonsBoundaryType', 'PermissonsBoundaryArn', 'Tags', 'Inline Policies', 'AWS Managed Policies', 'Customer Managed Policies', 'Groups', 'Number of SSH Keys', 'Public Key IDs', 'Public Key Status', 'Public Key Upload Dates', 'Number of MFA Devices', 'MFA Devices', 'MFA Devices Enabled Date', 'Number of Signed Certs', 'Certs Ids', 'Certs Body', 'Certs Status', 'Certs Upload Date'])
        allUserInfo = response['Users']
        if len(allUserInfo):
            for i in allUserInfo:
                userName = i['UserName']
                userId = i['UserId']
                arn = i['Arn']
                createDate = i['CreateDate']

                try:
                    passwordLastUsed = i['PasswordLastUsed']
                except KeyError:
                    passwordLastUsed = "N/A"

                try:
                    permissionBoundaryType = i['PermissionsBoundary']['PermissionsBoundaryType']
                    permissionBoundaryArn = i['PermissionsBoundary']['PermissionsBoundaryArn']
                except KeyError:
                    permissionBoundaryType = "EMPTY"
                    permissionBoundaryArn = "EMPTY"
                try:
                    tagsList = i['Tags']
                    tags = concatTagValues(tagsList)
                except KeyError:
                    tags = "EMPTY"

                myInlinePolicies = self.list_user_inline_policies(userName)
                myManagedPolicies = self.list_user_managed_policies(userName)
                myAWSManagedPolicies = self.get_AWS_managed_policies(myManagedPolicies)
                myCustomerManagedPolicies = self.get_customer_managed_policies(myManagedPolicies)
                myGroups = self.list_groups_for_user(userName)
                numOfAccessKeys, publicKeyIds, publicKeyIdStatus, publicKeyCreationDates = self.list_access_public_keys(userName)
                numOfMFADevices, MFADevices, MFADevicesEnabledDate = self.list_my_mfa_devices(userName)
                numSignedCerts, certificateIds, certificateBody, certificateStatus, certificateUploadDate = self.list_user_signing_certificates(userName)
                writer.writerow([userName, userId, arn, createDate, passwordLastUsed, permissionBoundaryType, permissionBoundaryArn, tags, myInlinePolicies, myAWSManagedPolicies, myCustomerManagedPolicies, myGroups, numOfAccessKeys, publicKeyIds, publicKeyIdStatus, publicKeyCreationDates, numOfMFADevices, MFADevices, MFADevicesEnabledDate, numSignedCerts, certificateIds, certificateBody, certificateStatus, certificateUploadDate])
        else:
            writer.writerow(['EMPTY']*24)

        writer.writerow([])   # Write an empty row at end
   
class Groups:
    def __init__(self, client, csvWriter):
        self.client = client
        self.csvWriter = csvWriter
    
    def list_all_groups(self):
        response = client.list_groups(
            # PathPrefix='string',
            # Marker='string',
            MaxItems = MAX_ITEMS
        )
        return response

    def list_of_group_inline_policies(self, groupname):
        response = client.list_group_policies(
            GroupName = groupname,
            # Marker='string',
            MaxItems = MAX_ITEMS
        )
        allMyInlinePolicies = response['PolicyNames']
        if len(allMyInlinePolicies):
            return concatListToString(allMyInlinePolicies)
        else:
            return "EMPTY"

    def list_of_group_managed_policies(self, groupname):
        response = client.list_attached_group_policies(
            GroupName=groupname,
            # PathPrefix='string',
            # Marker='string',
            MaxItems=MAX_ITEMS
        )
        allMyManagedPolicies = response['AttachedPolicies']
        if len(allMyManagedPolicies):
            managedPoliciesPolicyName = extractValueFromListDictionaryPair(allMyManagedPolicies, 'PolicyName')
            return concatListToString(managedPoliciesPolicyName)
        else:
            return "EMPTY"

    def list_all_groups_to_csv(self, response):
        writer.writerow(['Group Name', 'Group ID', 'Group Arn', 'Group Create Date', 'Group Inline Policies', 'Group Managed Policies'])
        allGroups = response['Groups']
        if len(response):
            for i in allGroups:
                groupName = i['GroupName']
                groupId = i['GroupId']
                groupArn = i['Arn']
                groupCreateDate = i['CreateDate']
                # Inline Policies
                groupInlinePolicies = self.list_of_group_inline_policies(groupName)
                # Managed Policies
                groupManagedPolicies = self.list_of_group_managed_policies(groupName)
                
                writer.writerow([groupName, groupId, groupArn, groupCreateDate, groupInlinePolicies, groupManagedPolicies])
        else:
            writer.writerow(['EMPTY']*6)
        writer.writerow([]) # write a empty row at end



class Policies:
    def __init__(self, client, csvWriter):
        self.client = client
        self.csvWriter = csvWriter

    def list_all_local_policies(self):
        response = client.list_policies(
            Scope='Local',
            OnlyAttached=False,
            # PathPrefix='string',
            # PolicyUsageFilter='PermissionsPolicy'|'PermissionsBoundary',
            # Marker='string',
            MaxItems=MAX_ITEMS
        )
        return response

    def get_policy_document(self, policyArn, versionId):
        response = client.get_policy_version(
            PolicyArn = policyArn,
            VersionId = versionId
        )
        policyDetails = response['PolicyVersion']
        return policyDetails['Document']

    def list_all_local_policies_to_csv(self, response):
        allPolicies = response['Policies']
        writer.writerow(['Policy Name', 'Policy Id', 'Attachment Count', 'Policy Description', 'Policy Document'])
        if len(allPolicies):
            for i in allPolicies:
                policyName = i['PolicyName']
                policyId = i['PolicyId']
                attachmentCount = i['AttachmentCount']
                try:
                    policyDescription = i['Description']
                except KeyError:
                    policyDescription = "Empty"
                policyArn = i['Arn']
                policyVersionId = i['DefaultVersionId']
                policyDocument = self.get_policy_document(policyArn, policyVersionId)
                writer.writerow([policyName, policyId, attachmentCount, policyDescription, policyDocument])
        else:
            writer.writerow(["EMPTY"]*5)
        writer.writerow([])


# class Roles:



if __name__ == "__main__":
    client = boto3.client('iam')
    print ("Input CSV File name: ")
    FILENAME = input()
    FILENAME = FILENAME + ".csv"
    with open(FILENAME, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        print('Beginning to obtain user info...')
        user = User(client, writer)
        allUsers = user.list_all_users()
        print('Obtained Users Info Successfully!')
        user.list_all_users_info_to_csv(allUsers)
        print('Extracted User Info from AWS IAM Successfully!')

        print('Beginning to obtain group info...')
        groups = Groups(client, writer)
        allGroups = groups.list_all_groups()
        print('Obtained Groups Info Successfully!')
        groups.list_all_groups_to_csv(allGroups)
        print('Extracted Group Info from AWS IAM Successfully!')

        print('Beginning to obtain Policies info...')
        policies = Policies(client, writer)
        allPolicies = policies.list_all_local_policies()
        policies.list_all_local_policies_to_csv(allPolicies)
        print('Extracted Policies Info from AWS IAM Successfully!')

    print("Saved to " + FILENAME)
    print ("Extraction Complete")

