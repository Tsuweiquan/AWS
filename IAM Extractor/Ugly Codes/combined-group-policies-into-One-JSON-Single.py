# Combine Multiple CustomerManagePolicies in a Single permission Set
# while loop
    # Input GroupName that is attached with Customer Managed Policy
    # while loop
        # Collect all the policies ARN & Name   //list_attached_group_policies
        # Use the policy arn to get the policy document out //get_policy, get_policy_version
    # combine all policies and output 1 JSON string of the policy
# Written by TsuWeiQuan
# Input -> Single Group Name
# Output -> write to CSV in rows of GroupName, Combined JSON Policy Text

import boto3
import csv

MAXIMUM_ITEMS = 300
FILENAME = "combined-C-M-P.csv"
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
    
        while True:
            while True:
                print ("Enter an Group Name that exist in IAM to consolidate all Customer Managed Policies into a Single JSON: ")
                groupName = input()

                try:
                    response = client.list_attached_group_policies(
                        GroupName=groupName,
                        MaxItems=MAXIMUM_ITEMS
                    )
                    break
                except Exception as e:
                    print(e)
                    print("Please Try Again!")

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
                    # print ("Found -> " + myPolicyName + ":" + myPolicyARN)
                    print ("=============================================")
                else:
                    print ("Policy conflicited. Same ARN with unequal Policy Name")
                    exit(-1)
            
            # print (PolicyArnToDocSet)
            combinePolicy = combineJSONPolicies(PolicyArnToDocSet)
            writer.writerow([groupName, combinePolicy])
            print ("Combination of the policies listed above completed!")
            print ("=============================================")
