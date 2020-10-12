"""
This file demonstrates a basic workflow for creating mutants. First, 
we collect a list of nodes we want to mutate, then we modify
those nodes one at a time to create mutants. There are a couple things
you should change before using this for HW3: 

1) Add a command line interface
2) Add code for writing mutants back to python source code
3) Add code to turn add nodes into multiply nodes

See lines marked with TODO
"""

import astor
import sys
import ast
import random
import copy


def main():
    # We want "randomness", but we also want it to do the same thing
    # every time (determistic execution).
    random.seed(2873465893)

    # parse command line
    arg_list = sys.argv
    file_to_read = arg_list[1]
    num_mutants = int(arg_list[2])

    with open(file_to_read, 'r') as f:
        program = ast.parse(f.read()) # convert the file into an AST
    
    collector = AddCollector()
    
    collector.visit(program) # collects all nodes that can be possibly mutated
    random.shuffle(collector.binops_to_visit) # shuffles all possibly mutated nodes
    print(collector.binops_to_visit)
    to_mutate = collector.binops_to_visit[:num_mutants] # slice x amount of nodes to work on
    print(to_mutate)

    i = 0
    while num_mutants > 0: # loop through number of mutants
        with open(file_to_read, 'r') as f:
            program = ast.parse(f.read())
        j = i % len(to_mutate)
        print('THIS IS THE NODE I WILL MUTATE', to_mutate[j])
        mutant = AddMutator(to_mutate[j]).visit(program) # will mutate based on the type of operator
        newname = str(i) + ".py"
        F = open(newname, 'w')
        F.write(astor.to_source(mutant)) # convert ast to the source code and write it
        F.close()
        num_mutants = num_mutants - 1
        i = i+1
      #  print('GOING IN HERE ONCE')


# Find all the Add nodes in the program and record them.
class AddCollector(ast.NodeVisitor):
    def __init__(self):
        self.binop_count = 0
        self.function_count = 0
        self.binops_to_visit = []
        self.comp_count = 0
        # self.comps_to_visit = []

    # For demonstration purposes: count how many functions there are,
    # then make sure to continue visiting the children.
    def visit_FunctionDef(self, node):
        # Calls visit on all the children.
        self.generic_visit(node)
        self.function_count += 1

    # This function will get called on every BinOp node in the tree.
    def visit_BinOp(self, node):
        self.generic_visit(node)
        self.binop_count += 1
        if (isinstance(node.op, ast.Add) or isinstance(node.op, ast.Sub) or isinstance(node.op, ast.Div) or isinstance(node.op, ast.Mult) 
        or isinstance(node.op, ast.FloorDiv)):
            self.binops_to_visit.append(self.binop_count) # recording eg. this is 5th bin op and it is an add operator 
    
    def visit_Compare(self,node):
        self.generic_visit(node)
        self.binop_count += 1
        self.binops_to_visit.append(self.binop_count)
        # for (i, op) in enumerate(node.ops):
        #     if(isinstance(op, ast.Gt)):
        #         print(op)
        #         self.comps_to_visit.append(self.comp_count)
    
    # def visit_Assign(self,node):
    #     self.generic_visit(node)
    #     self.binop_count += 1
    #     print('IN ASSSSSSIIGGGN', node.value)
    #     if (isinstance(node.value, ast.AnnAssign)):
    #         print('EVER GOING IN HERE???????')
    #         self.binops_to_visit.append(self.binop_count)


class AddMutator(ast.NodeTransformer):
    def __init__(self, count_of_node_to_mutate):
        self.count_of_node_to_mutate = count_of_node_to_mutate
        self.binop_count = 0
        # self.comp_count = 0

    def visit_BinOp(self, node):
        self.generic_visit(node)
        self.binop_count += 1

        # Check if this is the node we want to alter. We can accomplish this by
        # keeping track of a counter, which we increment every time encounter
        # a BinOp. Since the traversal through the AST is deterministic using the visitor
        # pattern (IT IS NOT DETERMINISTIC IF YOU USE ast.walk), we can identify AST nodes
        # uniquely by the value of the counter
        if (self.binop_count == self.count_of_node_to_mutate):
            # We make sure to use deepcopy so that we preserve all extra
            # information we don't explicitly modify
            new_node = copy.deepcopy(node)
            ast.copy_location(new_node, node)
            
            # figure out a way to randomize what operator it transforms to based on the current operator
        
            if isinstance(node.op,ast.Add):
                #randomly generate a number which will associate to a certain type of transformation
                num = random.randint(0,2)
                print('random number', num)
                if num == 0:
                    new_node.op = ast.Mult()
                if num == 1: 
                    new_node.op = ast.Sub()
                if num == 2:
                    new_node.op = ast.Div()
            if isinstance(node.op, ast.Mult):
                num = random.randint(0,3)
                if num == 0:
                    new_node.op = ast.Div()
                if num == 1: 
                    new_node.op = ast.Add()
                if num == 2:
                    new_node.op = ast.FloorDiv()
                if num == 3:
                    new_node.op = ast.Sub()
            if isinstance(node.op, ast.Div):
                num = random.randint(0,2)
                if num == 0:
                    new_node.op = ast.FloorDiv()
                if num == 1: 
                    new_node.op = ast.Mult()
                if num == 2:
                   new_node.op = ast.Add()
            if isinstance(node.op, ast.Sub):
                num = random.randint(0,2)
                if num == 0:
                    new_node.op = ast.Add()
                if num == 1: 
                    new_node.op = ast.Mult()
                if num == 2:
                    new_node.op = ast.Div()
            if isinstance(node.op, ast.FloorDiv):
                new_node.op = ast.Div()
            print('I AM CREATING A NEW NODE HERE', self.binop_count)
            return new_node
        else:
            # If we're not looking at an add node we want to change, don't modify
            # this node whatsoever
            return node

    def visit_Compare(self,node):
        self.generic_visit(node)
        self.binop_count += 1

        if (self.binop_count == self.count_of_node_to_mutate):
            new_node = copy.deepcopy(node)
            print('IN COMPARE')
            print('THIS IS THE PREVIOUS OP', node.ops)
            for (i, op) in enumerate(node.ops):
                if(isinstance(op, ast.Gt)):
                    num = random.randint(0,2)
                    if num == 0:
                        new_node.ops[i] = ast.GtE()
                    if num == 1:
                        new_node.ops[i] = ast.LtE()
                    if num == 2:
                        new_node.ops[i] = ast.Lt()
                if(isinstance(op, ast.GtE)):
                    num = random.randint(0,2)
                    if num == 0:
                        new_node.ops[i] = ast.Gt()
                    if num == 1:
                         new_node.ops[i] = ast.Lt()
                    if num == 2:
                         new_node.ops[i] = ast.LtE()
                if(isinstance(op, ast.Lt)):
                    num = random.randint(0,2)
                    if num == 0:
                        new_node.ops[i] = ast.LtE()
                    if num == 1:
                        new_node.ops[i] = ast.GtE()
                    if num == 2:
                        new_node.ops[i] = ast.Gt()
                if(isinstance(op, ast.LtE)):
                    num = random.randint(0,2)
                    if num == 0:
                        new_node.ops[i] = ast.Lt()
                    if num == 1:
                        new_node.ops[i] = ast.GtE()
                    if num == 2:
                        new_node.ops[i] = ast.Gt()
                if(isinstance(op, ast.Eq)):
                    new_node.ops[i] = ast.NotEq()
                if(isinstance(op, ast.NotEq)):
                    new_node.ops[i] = ast.Eq()
                if(isinstance(op, ast.Is)):
                    new_node.ops[i] = ast.IsNot()
                if(isinstance(op, ast.IsNot)):
                    new_node.ops[i] = ast.Is()
                print('THIS IS THE NEW OP', new_node.ops)
                print('I AM CREATING A NEW NODE HERE', self.binop_count)
                return new_node
        return node

if __name__ == '__main__':
    main()

#  if isinstance(node.op, ast.Eq): # CHANGE       
#                 new_node = ast.Compare(new_node.left, ast.NotEq(), new_node.right)
#             if isinstance(node.op, ast.NotEq):# CHANGE 
#                 new_node = ast.Compare(new_node.left, ast.Eq(), new_node.right)
#             if isinstance(node.op, ast.Lt):# CHANGE 
#                 num = random.randint(0,2)
#                 if num == 0:
#                     new_node = ast.Compare(new_node.left, ast.LtE(), new_node.right)
#                 if num == 1: 
#                     new_node = ast.Compare(new_node.left, ast.Gt(), new_node.right)
#                 if num == 2:
#                     new_node = ast.Compare(new_node.left, ast.GtE(), new_node.right)
#             if isinstance(node.op, ast.LtE):# CHANGE 
#                 num = random.randint(0,2)
#                 if num == 0:
#                     new_node = ast.Compare(new_node.left, ast.Lt(), new_node.right)
#                 if num == 1: 
#                     new_node = ast.Compare(new_node.left, ast.Gt(), new_node.right)
#                 if num == 2:
#                     new_node = ast.Compare(new_node.left, ast.GtE(), new_node.right) 
#             if isinstance(node.op, ast.Gt):# CHANGE 
#                 num = random.randint(0,2)
#                 if num == 0:
#                     new_node = ast.Compare(new_node.left, ast.LtE(), new_node.right)
#                 if num == 1: 
#                     new_node = ast.Compare(new_node.left, ast.GtE(), new_node.right)
#                 if num == 2:
#                     new_node = ast.Compare(new_node.left, ast.Lt(), new_node.right)
#             if isinstance(node.op, ast.GtE):# CHANGE 
#                 num = random.randint(0,2)
#                 if num == 0:
#                     new_node = ast.Compare(new_node.left, ast.LtE(), new_node.right)
#                 if num == 1: 
#                     new_node = ast.Compare(new_node.left, ast.Gt(), new_node.right)
#                 if num == 2:
#                     new_node = ast.Compare(new_node.left, ast.Lt(), new_node.right)


#  if isinstance(node.op, ast.Is):# CHANGE 
#                 new_node = ast.Compare(new_node.left, ast.IsNot(), new_node.right)
#             if isinstance(node.op, ast.IsNot):# CHANGE 
#                 new_node = ast.Compare(new_node.left, ast.IsNot(), new_node.right)