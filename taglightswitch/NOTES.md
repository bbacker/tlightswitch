# work on getting paths known.
kludge:
    PYTHONPATH=./src pytest -v tests/test_tags.py 
    PYTHONPATH=./src pytest -v tests/test_tags.py --pdb --pdbcls=IPython.terminal.debugger:Pdb
