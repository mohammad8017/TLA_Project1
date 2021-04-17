from DFA import DFAClass
from graphviz import Graph, render
from automata.fa.nfa import NFA
from PySimpleAutomata import automata_IO
import networkx as nx
import matplotlib.pyplot as plt


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
		holdRules = []
		dicttest = {}
		for rule in self.Rules:
			tmp = (rule[0], rule[1])
			temp = (rule[0], rule[1])
			temp2 = rule[2]
			dicttest.update({temp:temp2})
			holdRules.append(tmp)

		G = nx.DiGraph()
		G.add_edges_from(holdRules)
		
		labels = nx.get_edge_attributes(G, 'weight')
		labels = dicttest
		pos = nx.spring_layout(G)
		nx.draw_networkx_nodes(G, pos, node_size=500)
		nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='black')
		nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
		nx.draw_networkx_labels(G, pos)
		plt.title("NFA Diagram")
		plt.show()	


		

		
	def findRegExp(self):
		# regex = ""
		# for state in self.allStates:
		# 	FromCurrentState = [tmp for tmp in self.Rules if tmp[0] == state]
		# 	toghe = [tmp for tmp in FromCurrentState if tmp[0] == tmp[1]]

		# 	if len(toghe) > 0:
		# 		regex +='('
		# 		for i in range(len(toghe)):
		# 			if i == len(toghe)-1:
		# 				regex += toghe[i][2]
		# 			else:
		# 				regex += toghe[i][2]
		# 				regex +='+'
		# 			FromCurrentState.remove(toghe[i])	
		# 		regex += ")*"

		equations = []
		for state in self.allStates:
			FromCurrentState = [tmp for tmp in self.Rules if tmp[0] == state]
			tmp = "{}=".format(state)
			for hold in FromCurrentState:
				tmp += "{}{}+".format(hold[2], hold[1])
			tmp = list(tmp)	
			if tmp[-1] == '+':
				tmp.pop(-1)
				tmp = str(tmp)
			if state in self.finalStates:
				tmp += "+$"     # replace landa with $

		print()   

	def isAcceptByNFA(self, inputString):
		accept = True      
		currentState = self.initialState

		# insert landa between all chars of string
		# inputString = " ".join(inputString)
		# inputString = list(inputString)
		# inputString.insert(0,' ')
		# inputString.append(' ')


		for i in range(len(inputString)):
			currentStateList = [item for item in self.Rules if (item[0] == currentState and item[2] == inputString[i]) or (item[0] == currentState and item[2] == ' ')] #all rules from current state
			check = False
			for item in currentStateList:
				if item[2] == inputString[i]:
					currentState = item[1]
					check = True
					break
			accept = check
			if not accept and inputString[i] != " ":
				return accept   

		if accept and (currentState in self.finalStates):
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

