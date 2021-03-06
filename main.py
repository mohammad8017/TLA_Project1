from NFA import NFAClass
from DFA import DFAClass
from graphviz import Graph
from PySimpleAutomata import automata_IO
import networkx as nx
import matplotlib.pyplot as plt

if __name__ == "__main__":
    print("NFA input :")
    print("-------------------")
    allStates = input("Enter states of Finite Automata: ").split(',')
    finalStates = input("Enter final states of Finite Automata: ").split(',')
    alphabet = input("Enter alphabet of Finite Automata: ").split(',')
    initialState = allStates[0]
    numOfRules = int(input("Enter number of rules: "))

    Rules = []
    print("Enter rules: ")
    for i in range(numOfRules):
        Rules.append(input().split(','))

     

    nfaDiagram = NFAClass(allStates, alphabet, initialState, finalStates, Rules)
    nfaDiagram.showSchematicNFA()
        
    
    checkStr = input("Enter string to check accepted by NFA or not(replace landa with space): ")
    print(nfaDiagram.isAcceptByNFA(checkStr))

    #nfaDiagram.findRegExp() 

    tempDfA = nfaDiagram.createEquivalentDFA()
    hold = DFAClass()
    hold = tempDfA
    print("Equivalent DFA:")
    hold.printInfo()
    print("========================================================")





    print("DFA input :")
    print("-------------------")
    allStates = input("Enter states of Finite Automata: ").split(',')
    finalStates = input("Enter final states of Finite Automata: ").split(',')
    alphabet = input("Enter alphabet of Finite Automata: ").split(',')
    initialState = allStates[0]
    numOfRules = int(input("Enter number of rules: "))

    Rules = []
    print("Enter rules: ")
    for i in range(numOfRules):
        Rules.append(input().split(','))

    dfaDiagram = DFAClass(allStates, alphabet, initialState, finalStates, Rules)
    dfaDiagram.showSchematicDFA()   

    dfaDiagram.makeSimpleDFA() 

    checkStr = input("Enter string to check accepted by DFA or not(replace landa with space): ")
    print(dfaDiagram.isAcceptByDFA(checkStr))
    

    




    


# q0,q2,a
# q0,q4,a
# q0,q1,b
# q0,q2,b
# q0,q4,b
# q1,q0,a
# q1,q3,a
# q1,q0,b
# q1,q3,b
# q2,q0,b
# q2,q3,b
# q3,q2,a
# q3,q4,a
# q3,q1,b
# q3,q2,b
# q3,q4,b




