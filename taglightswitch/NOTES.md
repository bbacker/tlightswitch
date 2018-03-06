# run tests
    pytest -v tests/

# run tests, stop in debugger on failures
    pytest -v --pdb --pdbcls=IPython.terminal.debugger:Pdb


# list instances with lightswitch tags
    aws ec2 describe-instances --filters Name=tag-key,Values=lightswitch:timerange \
        | grep InstanceId

# use jq to filter out just instance IDs and states
    aws ec2 describe-instances --filters Name=tag-key,Values=lightswitch:timerange \
        | jq '.Reservations | .[] | .Instances | .[] | .InstanceId,.State'
