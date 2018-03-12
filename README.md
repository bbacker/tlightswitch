# taglightswitch

power EC2 instances on/off based on tag schedule contents

## Goals:

1. allow EC2 instance to be turned off at nights for cost control
1. minimize required interaction with AWS by the users of the EC2 instances
1. allow check power states vs schedule action to be executed by cron, jenkins, lambda, or command line
1. keep scheduled actions for instances with the instances, not a separate data store that needs to be kept in sync
    - allow cloud formation template or newly generated instance to opt in to schedule power by tagging their instance
    - allow EC2 user to opt out by removing or modifying the instance tags
1. allow a dry run mode where power changes are explained but not actually performed

## Tagging format - simple range of time during the given day

Ex. applying a tag to EC2 instance

        "Key": "lightswitch:offhours", "Value": "start=19:00,end=07:00",

means you would like the instance to be powered off after 19:00 (7pm), powered back on at 07:00 (7AM).
These ranges bound when the power on/off happens, but they power is done by
the script. That means if the script was run every 10 minutes, say at 6:45AM, 6:55AM, 7:05AM,
7:15AM, etc, the executions at 7:05AM, 7:15AM, etc would power on the server if it was off.
Similarly the executions at 6:45AM and 6:55AM would have turned the server off if it
was on during that time since those times fall within the "lightswitch:offhours".

The time in the range is evaluated vs the supplied target time without timezones.
That means you if you intend a given set of ranges to be Pacific Standard Time,
the execute the command with a target time in PST.


See tagged instances

    $ export AWS_PROFILE=myaccountprofile
    $ aws ec2 describe-instances --filters Name=tag-key,Values=lightswitch:offhours

see tagged instances ids and power states only, requires [jq](https://stedolan.github.io/jq/tutorial/).

    $ export AWS_PROFILE=myaccountprofile
    $ aws ec2 describe-instances --filters Name=tag-key,Values=lightswitch:offhours \
        | jq '.Reservations | .[] | .Instances | .[] | .InstanceId,.State'

# Setup

 The tools do not have arguments for aws roles, keys, profiles, etc but rely on either the
executing environment (e.g. a jenkins instance's EC2 role or 
[environment variables](http://boto3.readthedocs.io/en/latest/guide/configuration.html#environment-variables)
) to provide access. 

## Power 'advise' usage

To give advice for right now on which should be on or off.

    $ export AWS_PROFILE=myaccountprofile
    $ ./lightswitch_check_schedule.py

or

    $ export AWS_PROFILE=myaccountprofile
    $ ./lightswitch_check_schedule.py -a advise

To give advice for which should be on or off at 9pm tonight

    $ export AWS_PROFILE=myaccountprofile
    $ ./lightswitch_check_schedule.py -t 21:00

## Power 'correct' usage

To have the script take action (power on or off) for instances not matching their desired power state.

    $ export AWS_PROFILE=myaccountprofile
    $ ./lightswitch_check_schedule.py -a correct

## TODO:
     * mock boto3 calls so tests can can include platform agnostic find and boto3 failure mode tests
     * implement mode to turn off instances, leave them off, give users means to turn back on
     * output results of real power actions to SNS
     * test and document use of timezones in offhours parsing
