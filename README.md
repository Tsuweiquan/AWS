# AWS
This repo contains some AWS script that was written during my internship. The scipts are using the boto3 python API from AWS which are quite easily written. I might not have a good coding practice but I will try to write it to follow the S.O.L.I.D Principle. Data are stored into CSV upon extraction completion. 

## Pre-requesite
Before running the scripts, you should have aws-cli installed on your host and an access key pair to the AWS account. 
The access key pair should have at least a ReadOnlyAccess permission given for data extraction. 
Furthermore, it is required to install boto3 by running `pip install boto3`[https://pypi.org/project/boto3/].

This script only extract information and does not write into the AWS account. To be extra safe, please provision a read-only access to the user who is executing this script.

## Files
- IAM Extractor/IAM_Extractor.py

The IAM Info Extractor will extract IAM Users, Groups and Permission Sets information for each user.
Upon executing the script by using `python IAM_Extractor.py`, the program will prompt for an filename for the csv output file.
 

