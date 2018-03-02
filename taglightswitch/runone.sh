#!/bin/sh -x
export AWS_PROFILE=archproto
export PYTHONPATH=./src 
pytest -v tests/test_tags.py --pdb --pdbcls=IPython.terminal.debugger:Pdb
