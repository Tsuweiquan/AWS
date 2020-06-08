# Combine Multiple CustomerManagePolicies in a Single permission Set
# while loop
    # Input GroupName that is attached with Customer Managed Policy
    # while loop
        # Collect all the policies ARN & Name   //list_attached_group_policies
        # Use the policy arn to get the policy document out //get_policy, get_policy_version
    # combine all policies and output 1 JSON string of the policy
# Input -> String of GroupName
    # EG: "admin_group, CodeDeploy, link-infra, proficiogroup"
# Output -> write to CSV in rows of GroupName, Combined JSON Policy Text
# Written by TsuWeiQuan

import boto3
import csv

MAXIMUM_ITEMS = 300
FILENAME = "combined-group-policies-into-One-JSON.csv"
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html

def combineJSONPolicies (PolicyArnToDocSet):
    versionKey = "Version"
    versionValue = "2012-10-17"
    statementKey = "Statement"
    statementValue = []
    for x in PolicyArnToDocSet:
        obj = PolicyArnToDocSet[x]
        statementList = obj[statementKey]
        statementValue = statementValue + statementList
    
    combinePolicy = {}
    combinePolicy.update({versionKey:versionValue})
    combinePolicy.update({statementKey:statementValue})
    return combinePolicy

if __name__ == "__main__":
    client = boto3.client('iam')
    # Setup CSV
    with open(FILENAME, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        print ("Enter the String of Group Names that exist in IAM to consolidate all Customer Managed Policies into a Single JSON: ")
        stringOfGroupName = input()
        # Convert string of group name to a List
        listOfGroupName = stringOfGroupName.split(", ")
        print (listOfGroupName)
        
        for groupName in listOfGroupName:
            try:
                response = client.list_attached_group_policies(
                    GroupName=groupName,
                    MaxItems=MAXIMUM_ITEMS
                )
            except Exception as e:
                print(e)
                exit(-1)

            PolicyNameToARNSet = {}
            PolicyArnToDocSet = {}
                # Extract Policy Name and Policy ARN
            for i in response['AttachedPolicies']:
                myPolicyName = i['PolicyName']
                myPolicyARN = i['PolicyArn']
                PolicyNameToARNSet.update({myPolicyName:myPolicyARN})
                
                # Get Version in order to get Document
                response = client.get_policy(
                    PolicyArn=myPolicyARN
                )
                response = response['Policy']
                if response['PolicyName'] == myPolicyName:
                    myPolicyVersionId = response['DefaultVersionId']        
                    # Get the Document now
                    response = client.get_policy_version(
                        PolicyArn=myPolicyARN,
                        VersionId=myPolicyVersionId
                    )
                    response = response['PolicyVersion']
                    myPolicyDocument = response['Document']    # Dictionary
                    PolicyArnToDocSet.update({myPolicyARN:myPolicyDocument})
                    print ("Found -> " + myPolicyName + ":" + myPolicyARN)
                    print ("=============================================")
                else:
                    print ("Policy conflicited. Same ARN with unequal Policy Name")
                    exit(-1)
            
            # print (PolicyArnToDocSet)
            combinePolicy = combineJSONPolicies(PolicyArnToDocSet)
            writer.writerow([groupName, combinePolicy])
            print ("Combination of the policies for Group " + groupName +" above completed!")
            print ("=============================================")

