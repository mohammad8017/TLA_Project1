from DFA import DFA
import graphviz
from PySimpleAutomata import automata_IO


class NFA():
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
		for rule in self.Rules:
			tmp = [rule[0], rule[2], rule[1]]
			holdRules.append(tmp)

		alphabetSet = set()
		for i in self.alphabet:
			alphabetSet.add(i)

		statesSet = set()
		for i in self.allStates:
			statesSet.add(i)

		initialStateSet = set()
		for i in self.initialState:
			initialStateSet.add(i)

		finalStateSet = set()
		for i in self.finalStates:
			finalStateSet.add(i)

		transitionsDict = {}
		for i in holdRules:
			transitionsDict.setdefault((i[0],i[1]), set()).add(i[2])			


		# NFA_example = {
		# 	"alphabet": self.alphabet, 
		# 	# [
				
		# 	# 	# "a",
		# 	# 	# "b",
		# 	# 	# "c"
		# 	# ],
		# 	"states": self.allStates,
		# 	# [
				
		# 	# 	# "a0",
		# 	# 	# "t0",
		# 	# 	# "t1",
		# 	# 	# "t2",
		# 	# 	# "t3",
		# 	# 	# "t4"
		# 	# ],
		# 	"initial_states": [self.initialState],
		# 	# [
				
		# 	# 	# "t0",
		# 	# 	# "a0"
		# 	# ],
		# 	"accepting_states": self.finalStates,
		# 	# [
		# 	# 	# "t0",
		# 	# 	# "t4",
		# 	# 	# "a0"
		# 	# ],
		# 	"transitions": 	holdRules,
		# 	# [
		# 	# 	# ["t0","b","t1"],
		# 	# 	# ["t0","a","t2"],
		# 	# 	# ["t1","c","t3"],
		# 	# 	# ["t1","c","t2"],
		# 	# 	# ["t1","b","t4"],
		# 	# 	# ["t2","b","t1"],
		# 	# 	# ["t2","a","t2"],
		# 	# 	# ["t2","a","t4"],
		# 	# 	# ["t3","c","t0"],
		# 	# 	# ["t3","b","t0"],
		# 	# 	# ["t3","b","t3"],
		# 	# 	# ["t3","a","t4"],
		# 	# 	# ["t3","a","t1"],
		# 	# 	# ["t4","a","t4"],
		# 	# 	# ["t4","b","t0"],
		# 	# 	# ["t4","c","t0"],
		# 	# 	# ["a0","a","t1"]
		# 	# ]
		# }

		nfa = {
        'alphabet': alphabetSet,
        'states': statesSet,
        'initial_states': initialStateSet,
        'accepting_states': finalStateSet,
        'transitions': transitionsDict
    	}
		
		automata_IO.nfa_to_dot(nfa, "NFA_Diagram")
		#automata_IO.nfa_to_dot(NFA_example, "NFA Diagram")
		print()

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

		

		return DFA(allStatesDFA, alphabetDFA, initialStateDFA, finalStatesDFA, RulesDFA)            

