    pytest -v tests/test_tags.py 
    pytest -v tests/test_tags.py --pdb --pdbcls=IPython.terminal.debugger:Pdb
    pytest -v --pdb --pdbcls=IPython.terminal.debugger:Pdb


    aws ec2 describe-instances --filters Name=tag-key,Values=lightswitch:timerange |grep InstanceId
