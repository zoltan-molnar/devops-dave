# Devops Dave

Devops Dave is your personal devops assistant. It can help you in your day to day job by giving a more intuitive
interface to AWS services. You can easily execute specific tasks on AWS and you can even collaborate with your
colleagues. Even if they are not programmer.

## Install

Currently, it's a slack bot (Facebook Messenger is under testing). You can easily install it by clicking here:

[<img src="https://platform.slack-edge.com/img/add_to_slack.png">](https://slack.com/oauth/authorize?&client_id=172719434563.172125638464&scope=bot,chat:write:bot,im:history,incoming-webhook)


## Usage

After installing it as a Slackbot, you can start using it. Currently, it supports the following AWS commands:
* Getting CloudWatch logs
* Restarting an EC2 instance
* Invalidating a CloudFront distribution
* Invoking an AWS Lambda
* Purging a queue

_You can ask for available commands anytime by asking for some help._

When you first try to run one of these commands, Devops Dave will ask for an AWS Access Key, Secret Key and Region.
You can also trigger this functionality by asking him to set up a config. This way, you can also add AWS config for
your team. So you can ask your support team to restart an instance for example if it's needed and you are in a holiday.
By default, Devops Dave will use your personal config, but if it can't find one, it will try to look for a team
config. These configurations are stored in DynamoDB and **encrypted at rest by AWS KMS**.

There are two additional features to help you. You can also create aliases for your AWS resources. So you don't have
to type i-23423432432 every single time when you would like to restart an instance.
You can just simply set an alias to i-23423432432 and name it as something you can remember. Like "always crashing
server".

And the last main feature is that you can schedule actions. So when your boss asks you to do the deploy at Friday
night, you can set up everything beforehand. Configure a lambda function to do everything for you. Then, You can just
set up a scheduled event to invoke your lambda function at 22:00 and another one to get your logs at 23:30 and go to
the nearest pub to have a beer. You will get your logs to your phone just in time. Then, you can sleep late Monday
morning, because remember. You had to be in the office till midnight.

_If you take a look at the code, you can see that there is another intent. I won't write down the question, because
of various reasons. However, the answer is 42._

## Notes

**The application is in Beta version. It's not recommended to manage your production environment with it.**

When AWS releases the functionality to create AWS Lex bots via CloudFormation, I will add a CloudFormation template
to the project, so anyone can deploy it and use it easily in a separated, more secure environment.

Few pieces are still missing, like automated tests, continuous integration, being able to choose between different
regions and wider range of supported services. I'm working on these, but if you feel so, feel free to join.