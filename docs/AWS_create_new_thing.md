## Create device thing in AWS-IoT

1. Sign in to the AWS Management Console, and then open the AWS IoT console at https://console.aws.amazon.com/iot

2. Go to the Monitor page. In the left navigation panel, choose Manage, and then choose Things.

![pic](pictures/AWS/AWS_Console.png)

3. You don't have a thing created yet. Choose Register a thing.

![pic](pictures/AWS/AWS_Console_Manage_Register.png)

4. On the Creating AWS IoT things page, choose Create a single thing.

![pic](pictures/AWS/AWS_Console_Manage_Register_things.png)

5. Enter a name for the device, leave the default values for all the other fields, and then choose Next.

![pic](pictures/AWS/AWS_Console_Manage_Register_Device.png)

6. Now you should generate the certificates.

![pic](pictures/AWS/AWS_Console_Manage_Certificates.png)

7. Download your public and private keys, certificate, and root certificate authority (CA)on your PC. 

![pic](pictures/AWS/AWS_Console_Manage_Certificates_Download.png)

8. Download your root certificate authority, a new window will open for select a CA to download.

![pic](pictures/AWS/AWS_Console_Manage_Certificates_Download_CA.png)

9. Don't forget to save these files, you need them to set the connection

10. Returns to the previous window and **Activate** 

11. Select **Attach a policy**

![pic](pictures/AWS/AWS_Console_Manage_Certificates_Download.png)

12. Close this window. Before, you need to create and attach a new policy to the certificate

![pic](pictures/AWS/AWS_Console_Manage_Certificates_AttachPolicy.png)

13. Open the AWS IoT console again https://console.aws.amazon.com/iot

14. In the left navigation panel, choose **Secure**, and then choose **Policies**. 

15. Select **Create a Policy**

![pic](pictures/AWS/AWS_Console_Secure_Policies.png)

16. Enter a Name for the policy:
    - **Action**        enter **iot:***
    - **Resource ARN**  enter **\***
    - **Effect**        choose **Allow**
Select Create. This policy allows your Device to publish messages to AWS IoT.

![pic](pictures/AWS/AWS_Console_Secure_Policies_Create_Device.png)

17. In the AWS IoT console, choose **Manage**, **Things**. On the Things page, choose your Thing

![pic](pictures/AWS/AWS_Console_Manage_Things_Device.png)

18. On the thing's **Details** page, in the left navigation panel, choose **Interact**.
Make a note of the REST API endpoint. You need it to connect to your device shadow.

![pic](pictures/AWS/AWS_Console_Manage_Things_Details_Interact_Device.png)

19. Now select **Security**, and choose the certificate that you created earlier. 

![pic](pictures/AWS/AWS_Console_Manage_Things_Details_Security_Device.png)

20. In Actions, choose Attach policy

![pic](pictures/AWS/AWS_Console_Manage_Things_Details_Security_Policy_Device.png)

21. Select your new policy and then choose Attach 

![pic](pictures/AWS/AWS_Console_Manage_Things_Details_Security_Policy_Attach_Device.png)
