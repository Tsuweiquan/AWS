import boto3
import csv

MAX_ITEMS = 300
PATH_PREFIX = ''
MARKER = ''
FILENAME = "TEST.csv"
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

    def list_user_managed_policies(self, username):
        response = client.list_attached_user_policies(
            UserName=username,
            # PathPrefix='string',
            # Marker='string',
            MaxItems=MAX_ITEMS
        )
        managedPolicyList = response['AttachedPolicies']
        if len(managedPolicyList):
            listOfValues = extractValueFromListDictionaryPair(managedPolicyList, 'PolicyName')
            return concatListToString(listOfValues)
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
        writer.writerow(['UserName', 'UserId', 'Arn', 'CreateDate', 'PasswordLastUsed', 'PermissonsBoundaryType', 'PermissonsBoundaryArn', 'Tags', 'Inline Policies', 'Managed Policies', 'Groups', 'Number of SSH Keys', 'Public Key IDs', 'Public Key Status', 'Public Key Upload Dates', 'Number of MFA Devices', 'MFA Devices', 'MFA Devices Enabled Date', 'Number of Signed Certs', 'Certs Ids', 'Certs Body', 'Certs Status', 'Certs Upload Date'])
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
                myGroups = self.list_groups_for_user(userName)
                numOfAccessKeys, publicKeyIds, publicKeyIdStatus, publicKeyCreationDates = self.list_access_public_keys(userName)
                numOfMFADevices, MFADevices, MFADevicesEnabledDate = self.list_my_mfa_devices(userName)
                numSignedCerts, certificateIds, certificateBody, certificateStatus, certificateUploadDate = self.list_user_signing_certificates(userName)
                writer.writerow([userName, userId, arn, createDate, passwordLastUsed, permissionBoundaryType, permissionBoundaryArn, tags, myInlinePolicies, myManagedPolicies, myGroups, numOfAccessKeys, publicKeyIds, publicKeyIdStatus, publicKeyCreationDates, numOfMFADevices, MFADevices, MFADevicesEnabledDate, numSignedCerts, certificateIds, certificateBody, certificateStatus, certificateUploadDate])
        else:
            writer.writerow(['EMPTY']*18)

        writer.writerow([])   # Write an empty row at end
   
# class Groups:

# class Policies:

# class Roles:



if __name__ == "__main__":
    client = boto3.client('iam')
    with open(FILENAME, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        user = User(client, writer)
        allUsers = user.list_all_users()
        user.list_all_users_info_to_csv(allUsers)
        print("Saved to " + FILENAME)    
    print ("Extraction Complete")

