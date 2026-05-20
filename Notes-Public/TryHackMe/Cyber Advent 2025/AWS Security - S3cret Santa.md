Amazon Web Services utilises the Identity and Access Management (IAM) service to manage users and their access to various resources, including the actions that can be performed against those resources. Therefore, it is crucial to ensure that the correct access is assigned to each user according to the requirements.

Misconfiguring IAM has led to several high-profile security incidents in the past, giving attackers access to resources they were not supposed to access. Companies like Toyota, Accenture and Verizon have been victims of such attacks in the past, often exposing customer data or sensitive documents.
## IAM Users

A user represents a single identity in AWS. Each user has a set of credentials, such as passwords or access keys, that can be used to access resources. Furthermore, permissions can be granted at a user level, defining the level of access a user might have.
## IAM Groups

Multiple users can be combined into a group. This can be done to ease the access management for multiple users. 
## IAM Roles

An IAM Role is an assumed identity by a user, services or external accounts to get certain permissions.
## IAM Policies

Access provided to any user, group or role is controlled through IAM policies. A policy is a JSON document that defines the following:

- What action is allowed (Action)
- On which resources (Resource)
- Under which conditions (Condition)
- For whom (Principal)

## Practical: Enumerating a User's Permissions

 Enumerating Users:
 We can do so by running the following command in the terminal:

`aws iam list-users`

Policies can be inline or attached. Inline policies are assigned directly in the user (or group/ role) profile and hence will be deleted if the identity is deleted. Attached policies can be considered reusable, they only require one change in the policy and every identity that policy is attached to will inherit that change automatically.
Let's see what inline policies are assigned to Sir Carrotbane by running the following command.

`aws iam list-user-policies --user-name sir.carrotbane`

Great! We can see an inline policy in the results. Let's take note of its name for later.

Maybe, Sir Carrotbane has some policies attached to their account. We can find out by running the following command.

`aws iam list-attached-user-policies --user-name sir.carrotbane`

Hmmm, not much here. Perhaps we can check if Sir Carrotbane is part of a group. Let's run this command to do that.

`aws iam list-groups-for-user --user-name sir.carrotbane`

Looks like **sir.carrotbane** is not a part of any group.

Let's get back to the inline policy we found for Sir Carrotbane's account. Let's see what permissions this policy grants by running the following command (replace `POLICYNAME` with the actual policy name you found):

`aws iam get-user-policy --policy-name POLICYNAME --user-name sir.carrotbane`

## Enumerating Roles
Let's start by listing the existing roles in the account.

`aws iam list-roles`
Bingo! There's a role named `bucketmaster`, and it can be assumed by `sir.carrotbane`. Let's find out what policies are assigned to this role. Just as users, roles can have inline policies and attached policies. To check the inline policies, we can run the following command.

`aws iam list-role-policies --role-name bucketmaster`

There is one policy assigned to this role. Before checking that policy, let's see if there are any attached policies assigned to the role as well.

`aws iam list-attached-role-policies --role-name bucketmaster`

Looks like we only have the inline policy assigned. Let's see what permissions we can get from the policy.

`aws iam get-role-policy --role-name bucketmaster --policy-name BucketMasterPolicy`

Well, what do we have here? We can see that the `bucketmaster` role can perform three different actions (ListAllBuckets, ListBucket and GetObject) on some resources of a service named S3. This might just be the breakthrough we were looking for. More on this service later.

## Assuming Role

To gain privileges assigned by the `bucketmaster` role, we need to assume it. We can use AWS STS to obtain the temporary credentials that enable us to assume this role. 

`aws sts assume-role --role-arn arn:aws:iam::123456789012:role/bucketmaster --role-session-name TBFC`

This command will ask STS, the service in charge of AWS security tokens, to generate a temporary set of credentials to assume the `bucketmaster` role. The temporary credentials will be referenced by the session-name "TBFC" (you can set any name you want for the session). Let's run the command

The output will provide us the credentials we need to assume this role, specifically the `AccessKeyID`, `SecretAccessKey` and `SessionToken`. To be able to use these, run the following commands in the terminal, replacing with the exact credentials that you received on running the `assume-role` command.
## What Is S3?

Before we continue, we need to know what exactly is S3. Amazon S3 stands for **Simple Storage Service**.  It is an object storage service provided by Amazon Web Services that can store any type of object such as images, documents, logs and backup files. Companies often use S3 to store data for various reasons, such as reference images for their website, documents to be shared with clients, or files used by internal services for internal processing.