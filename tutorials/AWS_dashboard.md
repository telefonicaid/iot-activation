---
layout: post
title:  "AWS Dashboard"
date:   2019-02-06 12:00:00 +00:00
categories: tutorial
---
### Table of Contents
- [Display your dashboard](#display-your-dashboard-in-less-than-3-minutes-one-click-away)
  * [AWS CloudFormation](#aws-cloudformation)
  * [Freeboard](#freeboard)
    + [load a freeboard](#load-a-freeboard)


# Display your dashboard in less than 3 minutes. One click away!!

Storing your values in the shade is a great solution, but sometimes your clients become far more demanding.
In these cases, you need to develop a custom dashboard.

We've thought in this case. We have this one click solution for you!!

![pic](pictures/freeboard/freeboard_init_dashboard.png)

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


## AWS CloudFormation

CloudFormation provides a common language for you to describe and provision 
all the infrastructure resources in your cloud environment.

It allows you to use a simple text file to build and rebuild your infrastructure.

To begin with, Go to CloudFormation Console:

Click on **Create Stack** button

![pic](pictures/AWS/AWS_Console_CloudFormation_Stack_create.png)

In the new window that opens, fill the form with the link below:

```
https://s3-eu-west-1.amazonaws.com/lambda-for-deploy/cloud_formartion_freeboard.txt
```

In the link you can see a public s3 bucket with our CloudFormation template.

![pic](pictures/AWS/AWS_Console_CloudFormation_Stack_create_config.png)

Click **Next**.

Select a name for your Stack and use the same for name your s3 bucket:

```
iotactivationdashboard
```

![pic](pictures/AWS/AWS_Console_CloudFormation_Stack_create_config_name.png)

Click **Next**.

In the next window, you don't need to configure any options

![pic](pictures/AWS/AWS_Console_CloudFormation_Stack_create_config_option.png)

Click **Next**.

Now the wizard will warn you about the capabilities. Just tick the boxes.

Finally, click on **Create Change Set**.

![pic](pictures/AWS/AWS_Console_CloudFormation_Stack_create_config_review.png)

Click on the **Execute** button.

It can take several minutes for deploy all the services.

![pic](pictures/AWS/AWS_Console_CloudFormation_Stack_create_running.png)

As a result, when it's finishes you will get a new link for display your dashboard.

Go to **Output** tab an click on the Website URL

![pic](pictures/AWS/AWS_Console_CloudFormation_Stack_create_ok.png)

You'll already have your freeboard created.

![pic](pictures/freeboard/freeboard_init.png)

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


## Freeboard

Freeboard is a simple dashboards for your devices.
It allow you build real-time, interactive dashboards and visualizations in minutes using the intuitive interface.

![pic](pictures/freeboard/freeboard_init_add.png)

To add a new source, you must select and set up an AWS account and fill the fields with your broker and thing topic.

![pic](pictures/freeboard/freeboard_init_aws.png)

All you have to do is add new panes. Let your imagination fly!!!

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


### load a freeboard

One simple example is the dashboard designed for this shadow.

```json
{
	"reported": {
		"raw": {
			"sensor1": 3,
			"text1": "TZEUXBZPZN",
			"sensor2": 76,
			"location": {
				"latitude": 40.431948,
				"longitude": -3.666315
			},
			"time": "Thu Mar 21 12:39:24 2019"
		}
	}
}
```

![pic](pictures/freeboard/freeboard_init_dashboard.png)

You can load it from this [file](https://github.com/telefonicaid/iot-activation/tree/master/scripts/AWS_Dashboard/freeboard.json)

![pic](pictures/freeboard/freeboard_init_load.png)

In the same way, you can export your freeboard. It is an important step to recover your configuration. 
It is lost every time you refresh the web.

&#x1F4CD;
Be careful, you don't share this file. It contains your account access key.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)

