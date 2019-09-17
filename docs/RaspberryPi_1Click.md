## Table of Contents
- [Publish in the Cloud in one Step](#publish-in-the-cloud-in-one-step)
  * [Download the code](#download-the-code)
  * [Run the Script](#run-the-script)
    - [Option 1 : Publish in AWS](#option-1--publish-in-aws)

# Publish in the Cloud in one Step

## Download the code

Access our Github [folder](https://github.com/telefonicaid/iot-activation/tree/master/scripts/Raspberry1Click) 
and download all the necessary scripts.

Or use the command: `wget`

```
wget https://raw.githubusercontent.com/telefonicaid/iot-activation/master/scripts/Raspberry1Click/Raspberry1Click.zip
```

Copy the above scripts together with the resources folders in your Raspberry.
You can use the Desktop path as an example.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


## Run the Script

Go to the path of the scripts you have downloaded on your Raspberry and execute the next script.

```
sudo sh configure.sh
```
This script will launch the rest of the script in the correct order.

The first step will be to enable the SSH connection for your raspberry and assign a static IP to the ethernet port (192.168.0.10)
So, you can access remotely.

Once this step is completed, the libraries will be installed to be able to configure the 3G Modem and enjoy Telefónica's connectivity.
For this, you will be asked by console to enter the APN of the SIM card you are using.

You can select the default APN [iotactivation.movistar.es] by pressing Enter

Once it's set up. You will connect the USB dongle with the SIM. You will have to wait a few seconds until 
the Internet connection is established.

Congrats!! Now your Raspberry is an IoT device.

The following steps allow you to configure the public cloud you want to report to.

A menu will appear in which you can select the cloud

```
SELECT CLOUD

1. AWS
0. Exit
Enter option:
```

### Option 1 : Publish in AWS

To select this option, type "1" and press enter.

The self-provisioning script will be launched automatically.

The tasks of this script are:
1- Register the thing in AWS IoT-Core with the name: **MyRaspberry_IoT_Activation**
2- Generate/Save certificates for device connection.
3- Associate a policy with IoT-Core permissions

To do this you will need the AWS access keys of a User with permissions on the IoT-Core:
**Access key ID** and **Secret access key**

&#x1F4CD;
These keys will not be stored

You will also need to know both the **Region** of the AWS server you are going to use and the IoT-Core **broker** 
(during the execution you will be able to log into the AWS console and check)

The first step is to select a region for your AWS server. To do this, choose a option from the following menu (Number from 1 to 12).

```
     1. US East (Ohio)
     2. US East (N. Virginia)
     3. US West (Oregon)
     4. Asia Pacific (Mumbai)
     5. Asia Pacific (Seoul)
     6. Asia Pacific (Singapore)
     7. Asia Pacific (Sydney)
     8. Asia Pacific (Tokyo)
     9. China (Beijing)
    10. EU (Frankfurt)
    11. EU (Ireland)
    12. EU (London)

What is your region in the AWS cloud?
```

The next step is to setup an AWS user with access to the IoT-Core.
You can use a previous user or create a new user login in the AWS console (open in a window)

```
Copy your Access key ID: xxxxxxxxxxxxxxxxxxxx
Copy your Secret access key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

To create a new user, you can follow the AWS documentation on the browser:
this user requires the following permissions:

- AWSIoTFullAccess

And the following custom policy to create a dashboard from Cloudformation:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "iam:GenerateCredentialReport",
                "iam:GetAccountPasswordPolicy",
                "iam:GetServiceLastAccessedDetailsWithEntities",
                "iam:ListServerCertificates",
                "iam:GenerateServiceLastAccessedDetails",
                "iam:ListPoliciesGrantingServiceAccess",
                "iam:GetServiceLastAccessedDetails",
                "iam:ListVirtualMFADevices",
                "iam:SimulateCustomPolicy",
                "iam:CreateAccountAlias",
                "iam:GetAccountAuthorizationDetails",
                "iam:DeleteAccountAlias",
                "iam:GetCredentialReport",
                "sns:*",
                "iam:ListPolicies",
                "iam:DeleteAccountPasswordPolicy",
                "iam:ListSAMLProviders",
                "s3:*",
                "cloudformation:*",
                "iam:ListRoles",
                "iam:GetContextKeysForCustomPolicy",
                "iam:UpdateAccountPasswordPolicy",
                "iam:ListOpenIDConnectProviders",
                "lambda:*",
                "iam:ListAccountAliases",
                "iam:ListUsers",
                "iam:ListGroups",
                "iam:GetAccountSummary"
            ],
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "iam:*",
            "Resource": [
                "arn:aws:iam::*:policy/*",
                "arn:aws:iam::*:role/*"
            ]
        }
    ]
}
```


Then, you only have to configure the broker MQTT.
Copy the address from the new tab that will open.

```
Copy your AWS broker from the web:  xxxxxxxxxxxxxx-ats.iot.xx-xxxxx-x.amazonaws.com
```

Now the device will register on the IoT-Core and download its certificates for secure access.


Last but not least, if you have configured your server in the Region of Ireland. 
You can choose to create a dashboard from which to view the data report.

```
Would you like to create a New Dashboard? [y/N]
```

Use the URL that will be shown to you during the process to access through any browser.

```
Copy the next URL for display your dashboard
"http://MyRaspberry_IoT_Activationxxxxxxxxxxxxxxxxxxx-west-1.amazonaws.com
Attention, this may take a few minutes.
```

If you want to learn more about how it works, access to the following [tutorial](AWS_dashboard.md)

Once the device has been registered, the sending of data to the broker is executed.
Additionally you can configure your Raspberry to start publishing data each time it is turned on.

```
Do you want to publish in AWS every time you turn on the device? [y/N] 
```

After these steps your Raspberry will start publishing in the Cloud




[![pic](pictures/utils/arrow_up.png)](#table-of-contents)

