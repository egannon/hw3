#!/bin/bash 
export PYTHONHASHSEED=0 
python3 mutate.py avl.py 10 
if [ -f 1.py ] ; then 
  echo -n "Number of Mutants produced (out of 10): " ; ls [0-9]*.py | wc -l
  rm -f avl.py
  echo -n "Running mutant 0 visibly (look at output carefully):" 
  cp 0.py avl.py 
  python3 privatetest-a.py 
  echo -n "Now running all mutants:" 
  for mutant in [0-9]*.py ; do rm -rf *pycache* *.pyc ; cp $mutant avl.py ; python3 privatetest-a.py ; done >& test.output ; grep FAILED test.output | wc -l > privatetest-a.score 
  for mutant in [0-9]*.py ; do rm -rf *pycache* *.pyc ; cp $mutant avl.py ; python3 privatetest-b.py ; done >& test.output ; grep FAILED test.output | wc -l > privatetest-b.score 
  for mutant in [0-9]*.py ; do rm -rf *pycache* *.pyc ; cp $mutant avl.py ; python3 privatetest-c.py ; done >& test.output ; grep FAILED test.output | wc -l > privatetest-c.score 
  echo -n "Your Mutation Score for Private Test Suite A: " ; cat privatetest-a.score
  echo -n "Your Mutation Score for Private Test Suite B: " ; cat privatetest-b.score
  echo -n "Your Mutation Score for Private Test Suite C: " ; cat privatetest-c.score
else 
  echo "=============================================" 
  echo "= Your mutate.py did not run on the server. ="
  echo "=============================================" 
  echo "Inspect the output nearby carefully to debug the problem." 
fi 
