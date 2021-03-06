from DFA import DFAClass
from graphviz import Graph, render, Digraph
from PySimpleAutomata import automata_IO
import networkx as nx
import matplotlib.pyplot as plt
import pyutil as Util


class NFAClass():
	def __init__(self, allStates = None, alphabet = None, initialState = None, finalStates = None, Rules = None):
		self.allStates = allStates
		self.alphabet = alphabet
		self.initialState = initialState
		self.finalStates = finalStates
		self.Rules = Rules


	def printInfo(self):
		print(self.allStates)
		print(self.alphabet)
		print(self.initialState)
		print(self.finalStates)
		print(self.Rules)  


	def showSchematicNFA(self):
		nfa = {}
		holdRules = {}
		for rule in self.Rules:
			if rule[2] != ' ':
				tmp = (rule[0], rule[2])
			else:
				tmp = (rule[0], "λ")	
			if tmp in holdRules.keys():
				holdRules[tmp].append(rule[1])	
			else:	
				temp2 = [rule[1]]
				holdRules.update({tmp:temp2})

		nfa['alphabet'] = set(self.alphabet)

		nfa['states'] = set(self.allStates)

		nfa['initial_states']= set([self.initialState])

		nfa['accepting_states'] = set(self.finalStates)

		nfa['transitions'] = holdRules

		automata_IO.nfa_to_dot(nfa, 'NFA_Diagram', '.\\NFA_Schema\\')


	def isAcceptByNFA(self, inputString):
		holdRules = {}
		for rule in self.Rules:
			tmp = (rule[0], rule[2])
			temp2 = rule[1]
			holdRules.update({tmp:temp2})

		holdAlphabet = set()
		for alphabet in self.alphabet:
			holdAlphabet.add(alphabet)

		holdStates = set()
		for state in self.allStates:
			holdStates.add(state)	

		holdInitial = set()
		for state in self.initialState:
			if type(self.initialState) == str:
				holdInitial.add(self.initialState)
				break
			else:
				holdInitial.add(state)

		holdFinal = set()
		for state in self.finalStates:
			holdFinal.add(state)		

		nfa = {
			"alphabet":holdAlphabet,

			"states": holdStates,

			"initial_states": holdInitial,

			"accepting_states": holdFinal,

			"transitions": holdRules
		}
			   
		current_level = set()
		current_level = current_level.union(nfa['initial_states'])
		next_level = set()
		for action in inputString:
			for state in current_level:
				if (state,action) in nfa['transitions']:
					tempCurrent = nfa['transitions'][state, action]
					next_level.add(tempCurrent)
					
			if len(next_level) < 1:
				return False
			current_level = next_level
			next_level = set()

		if current_level.intersection(nfa['accepting_states']):
			return True
		else:
			return False


	def createEquivalentDFA(self):     #ide az in site:      https://www.geeksforgeeks.org/conversion-from-nfa-to-dfa/ 
		alphabetDFA = self.alphabet
		initialStateDFA = self.initialState    
		allStatesDFA = [self.initialState]
		finalStatesDFA = []
		RulesDFA = []

		over = False
		i = 0
		while(not over):
			tempList2 = []
			for alphabet in self.alphabet:
				tempList = []
				for state in allStatesDFA[i]:
					if type(allStatesDFA[i]) != list: state = allStatesDFA[i]
					
					tmp = [item for item in self.Rules if item[0] == state and item[2] == alphabet]
					tempNewState = [item[1] for item in tmp]

					if len(tempNewState) == 1: 
						tempNewState = tempNewState[0]
						if not tempNewState in tempList:
							tempList.append(tempNewState)

					elif len(tempNewState) == 0:
						continue

					elif not tempNewState in tempList and tempNewState != tempList:
						for j in tempNewState:
							tempList.append(j)
						#tempList.append(tempNewState)
					if len(allStatesDFA) == 1:
						break 
					# if type(allStatesDFA[i]) != list:
					#     break    

				if len(tempList) == 1: tempList = tempList[0]

				RulesDFA.append([allStatesDFA[i], tempList, alphabet])
				
				if not tempList in allStatesDFA:
						tempList2.append(tempList)
						

			for j in tempList2:
				if not j in allStatesDFA:
					allStatesDFA.append(j)
			if len(tempList2) == 0 and i == len(allStatesDFA):
				over = True    
			if i < len(allStatesDFA)-1:
				i += 1
			else:
				break        

			 

		if [] in allStatesDFA:
			for alphabet in alphabetDFA:
				if not [[], [], alphabet] in RulesDFA:
					RulesDFA.append([[], [], alphabet])

		for finalState in self.finalStates:
			for state in allStatesDFA:
				if (finalState in state) and (state not in finalStatesDFA):
					finalStatesDFA.append(state)

		

		return DFAClass(allStatesDFA, alphabetDFA, initialStateDFA, finalStatesDFA, RulesDFA)            



	def _parenthesize(self,expr,starring=False):
		# """Return list of strings with or without parens for use in RegExp.
		# This is only for the purpose of simplifying the expressions returned,
		# by omitting parentheses or other expression features when unnecessary;
		# it would always be correct simply to return ['(',expr,')'].
		# """
		if len(expr) == 1 or (not starring and '+' not in expr):
			return [expr]
		elif starring and expr.endswith('+()'):
			return ['(',expr[:-3],')']  # +epsilon redundant when starring
		else:
			return ['(',expr,')']

	# def states(self):
	# 	visited = set()
	# 	unvisited = set(self.initialState)
	# 	while unvisited:
	# 		#state = arbitrary_item(unvisited)
	# 		state = next(iter(unvisited))
	# 		yield state
	# 		unvisited.remove(state)
	# 		visited.add(state)
	# 		for symbol in self.alphabet:
	# 			tmp = [[transition[0],transition[2]] for transition in self.Rules if transition[0]==state and transition[2]==symbol]
	# 			unvisited |= tmp - visited

	def transition(self,i,j,a):
		templist=[]
		templist.append('q'+str(i))
		templist.append('q'+str(j))
		templist.append(a)

		if(templist in self.Rules):
			return True
		else:
			return False
	
	def Star(self,s):
		return s+'*'


	def findRegExp(self):
		# Setup the system of equations A and B from Arden's Lemma.
  		# A represents a state transition table for the given DFA.
  		# B is a vector of accepting states in the DFA, marked as epsilons
		A=[[]]
		B=[]
		m=len(self.allStates)
		for i in self.allStates:
			if i in self.finalStates:
				B.append('ε')
			else:
				B.append('∅')
		
		for j in range(1,m):
			for q in range(1,m):
				for a in self.alphabet:
					if(self.transition(j,q,a)==True):
						A[i][j]=a
					else:
						A[i][j]='∅'
		
		for n in reversed(range(m,1)):
			B[n]=(self.Star(A[n][n])+B[n])
			for x in range(1,n):
				A[n][j]=(self.Star(A[n][n])+A[n][j])

			for z in range(1,n):
				B[i]+=(A[i][n]+B[n])
				for v in range(1,n):
					A[i][j]+=(A[i][n]+A[n][j])

		return B[1]







			

