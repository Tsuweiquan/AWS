#README
# This python script only does a READ-ONLY function using the IAM APIs.
# This python script utilize boto3 library to access AWS APIs to get IAM user information
# The script will export the following listed below into an CSV File.
# 1) All Users
# 2) Each User attached Individual Policies
# 3) Groups that the user belongs to
# 4) Each User Tags info
# 5) List out all Customer Managed Policies
# 6) Get all Customer Managed Policies Documents
# 7) List all Groups
# 8) List all policies attached to each group
#Before Running this script, ensure aws configure is setup on a ec2 instance with access to IAM
# Written by: Tsu Wei Quan

import boto3
import csv

MAXIMUM_ITEMS = 300
FILENAME = "EXTRACT_IAM_INFO.csv"
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html

def TruncateLastTwoCharacters (input):
    input = input[:-1]
    input = input[:-1]
    return input

if __name__ == "__main__":
    # Setup CSV
    with open(FILENAME, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Username', 'Direct Attached Policies', 'Groups', 'Tags'])

        client = boto3.client('iam')
        print ("########################## User Information Section ##########################")
        response = client.list_users(
            MaxItems = MAXIMUM_ITEMS
            )

        myUsers = response['Users']
        permissionSet = set()

        for i in myUsers:
            # Get User Name
            username = i['UserName']
            attachedDirectlyPoliciesResponse = client.list_attached_user_policies(
                UserName = username,
                MaxItems = MAXIMUM_ITEMS
            )
            # Get Each User Direct Attached Policies
            userPolicies = attachedDirectlyPoliciesResponse['AttachedPolicies']
            attachedDirectlyPolicies = ""
            if len(userPolicies) == 0 :   # if empty
                attachedDirectlyPolicies = "EMPTY"
            else:
                for j in userPolicies:
                    attachedDirectlyPolicies = attachedDirectlyPolicies + j["PolicyName"] + ", "
                attachedDirectlyPolicies = TruncateLastTwoCharacters(attachedDirectlyPolicies)
            
            # Add unique list of policies into a Set, to know how many permission set we should create
            permissionSet.add(attachedDirectlyPolicies)
        
            # Get Each User Groups
            userGroupsResponse = client.list_groups_for_user(
                UserName = username,
                MaxItems = MAXIMUM_ITEMS  
            )
            userGroups = ""
            response = userGroupsResponse['Groups']
            if len(response) == 0:
                userGroups = "EMPTY"
            else:
                for k in response:
                    userGroups = userGroups + k['GroupName'] + ", " 
                userGroups = TruncateLastTwoCharacters(userGroups)

            # Get Each User Tag info
            tagResponse = client.list_user_tags(
                UserName=username,
                MaxItems=MAXIMUM_ITEMS
            )
            myTags = ""
            response = tagResponse['Tags']
            if len(response) == 0:
                myTags = "EMPTY"
            else:
                for m in response:
                    Key = m['Key']
                    Value = m['Value']
                    KeyValuePair = Key + ":" + Value
                    myTags = myTags + KeyValuePair + ", "
                myTags = TruncateLastTwoCharacters(myTags)

            # Get Each User Access Key information
            response = client.list_access_keys(
                UserName=username,
                MaxItems=MAXIMUM_ITEMS
            )
            #response = response['AccessKeyMetadata']
            #if (len(response) == 0):
            #    myKeyStatus = "EMPTY"
            #else:
            #    for i in response:
            #        if username == i['UserName']:
            #            accessKeyId = i['AccessKeyId']
            #            accessKeyCreatedDate = i["CreateDate"]
            #            accessKeyStatus = i['Status']

            print ("User: " + username)
            print ("Directly Attached Policies: " + attachedDirectlyPolicies)
            print ("Groups: " + userGroups)
            print ("Tags: " + myTags)
            print ('=======================')
            print ("")
            #writer.writerow([username, attachedDirectlyPolicies, userGroups, myTags, accessKeyId, accessKeyCreatedDate, accessKeyStatus])
            writer.writerow([username, attachedDirectlyPolicies, userGroups, myTags])
        print ("########################## Policy Section ##########################")
        
        for x in range(3):
            writer.writerow([])

        # Listing out all Customer Managed Policies
        response = client.list_policies(
            Scope='Local',
            OnlyAttached=False,
            MaxItems=MAXIMUM_ITEMS
        )

        allLocalPolicies = response['Policies']
        LocalPolicies = ""
        ListOfPoliciesARN = []
        writer.writerow(["Total Customer Managed Policies: ", len(allLocalPolicies)])
        writer.writerow(["All Customer Policies"])
        if len(allLocalPolicies) == 0:
            LocalPolicies = "No Local Policies created"
        else:
            for n in allLocalPolicies:
                LocalPolicies = LocalPolicies + n['PolicyName'] + ', '
                ListOfPoliciesARN.append(n['Arn'])                          # Collect list of Policies ARN that is managed by Customers
                writer.writerow([n['PolicyName']])
            LocalPolicies = TruncateLastTwoCharacters(LocalPolicies)
        
        print ("All Customer Managed Policies are: " + LocalPolicies)
        print ('=======================')
        print ("")  
        
        for x in range(3):
            writer.writerow([])

        # Getting information for each Customer Managed Policy
        writer.writerow(["Policy Name", "Policy ARN", "Policy Version", "Policy Document"])
        for i in ListOfPoliciesARN:
            policyInfo = client.get_policy(
                PolicyArn = i
            )
            policyInfo = policyInfo['Policy']                   # Re-point/Re-use variable
            policyVersionID = policyInfo['DefaultVersionId']    # Extract Policy Version via ARN
            getPolicyDocument = client.get_policy_version(
                PolicyArn=i,
                VersionId=policyVersionID
            )
            getPolicyDocument = getPolicyDocument['PolicyVersion']  # Extract Policy Document via ARN
            print ("Policy Name: " + policyInfo['PolicyName'])
            print ("Policy ARN: " + policyInfo['Arn'])
            print ("Policy Version: " + getPolicyDocument['VersionId'])
            print ("Policy Document: ")
            print (getPolicyDocument['Document'])
            print ('=======================')
            print ("") 
            writer.writerow([policyInfo['PolicyName'], policyInfo['Arn'], getPolicyDocument['VersionId'], getPolicyDocument['Document']])

        print ("########################## Group Section ##########################")
        
        for x in range(3):
            writer.writerow([])

        response = client.list_groups(
            MaxItems=MAXIMUM_ITEMS
        )
        allGroups = response['Groups']
        allGroupsString = ""
        ListofAllGroups = []
        if len(allGroups) == 0:
            allGroupsString = "EMPTY"
        else:
            for o in allGroups:
                allGroupsString = allGroupsString + o["GroupName"] + ", "
                ListofAllGroups.append(o['GroupName'])
            allGroupsString = TruncateLastTwoCharacters(allGroupsString)

        print ("All Groups in this account: " + allGroupsString)
        writer.writerow(["Total Groups: ", len(allGroups)])
        writer.writerow(["All Groups:", allGroupsString])
        
        for x in range(3):
            writer.writerow([])

        writer.writerow(["Group Name", "Policies In Group"])
        for groupName in ListofAllGroups:
            response = client.list_attached_group_policies(
                GroupName=groupName
            )
            groupPoliciesString = ""
            groupPolicies = response['AttachedPolicies']
            if len(groupPolicies) == 0:
                groupPoliciesString = "EMPTY"
            else:
                for i in groupPolicies:
                    groupPoliciesString = groupPoliciesString + i['PolicyName'] + ", "
                groupPoliciesString = TruncateLastTwoCharacters(groupPoliciesString)
            print ("Group Name: " + groupName)
            print ("Group Policies: " + groupPoliciesString)    
            writer.writerow([groupName, groupPoliciesString])
        
        for x in range(3):
            writer.writerow([])
        
        print ("########################## Roles Section ##########################")
        
        writer.writerow(["Role", "Role's Policies", "Role Tags"])
        response = client.list_roles(
            MaxItems=MAXIMUM_ITEMS
        )
        allRoles = response['Roles']
        for x in allRoles:
            myRoleName = x['RoleName']
            
            # obtain all policies attached to the roles
            response = client.list_attached_role_policies(
                RoleName=myRoleName,
                MaxItems=MAXIMUM_ITEMS
            )
            StringOfPoliciesInRole = ""
            listOfPoliciesInRole = response['AttachedPolicies']
            if len(listOfPoliciesInRole) == 0:
                StringOfPoliciesInRole = "EMPTY"
            else:
                for i in listOfPoliciesInRole:
                    StringOfPoliciesInRole = StringOfPoliciesInRole + i['PolicyName'] + ', '
                StringOfPoliciesInRole = TruncateLastTwoCharacters(StringOfPoliciesInRole)

            # Obtain the tags attached to the roles
            roleTagResponse = client.list_role_tags(
                RoleName = myRoleName,
                MaxItems=MAXIMUM_ITEMS
            )
            myRoleTags = ""
            tagResponse = roleTagResponse['Tags']
            if len(tagResponse) == 0:
                myRoleTags = "EMPTY"
            else:
                for m in tagResponse:
                    Key = m['Key']
                    Value = m['Value']
                    KeyValuePair = Key + ":" + Value
                    myRoleTags = myRoleTags + KeyValuePair + ", "
                myRoleTags = TruncateLastTwoCharacters(myRoleTags)

            print ("Role Name: " + myRoleName)
            print ("Role's Policies: " + StringOfPoliciesInRole)
            print ("Role's Tag: " + myRoleTags)
            writer.writerow([myRoleName, StringOfPoliciesInRole, myRoleTags])

        print (permissionSet)
        print ("Number of Permission Sets: " + str(len(permissionSet)))
        for x in range(3):
            writer.writerow([])
        
        writer.writerow(['Potential Unique Permissions Set that can be created: ', len(permissionSet)])
        for i in permissionSet:
            writer.writerow([i])

        print ("Extraction Completed")
