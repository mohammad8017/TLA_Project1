from PySimpleAutomata import automata_IO



class DFAClass():
	def __init__(self, allStates = None, alphabet = None, initialState = None, finalStates = None, Rules = None):
		self.allStates = allStates
		self.alphabet = alphabet
		self.initialState = initialState
		self.finalStates = finalStates
		self.Rules = Rules

	def printInfo(self):
		print("all states: ",self.allStates)
		print("................................")
		print("alphabet: ", self.alphabet)
		print("................................")
		print("initial state: ", self.initialState)
		print("................................")
		print("final state: ", self.finalStates)
		print("................................")
		print("rules: ", len(self.Rules))
		for i in self.Rules:
			print(i)   
		print("................................")   


	def isAcceptByDFA(self, inputStr):
		currentState = self.initialState

		for char in inputStr:
			tmp = []
			for item in self.Rules: 
				if item[0] == currentState and item[2] == char: tmp = item
			currentState = tmp[1]

		if currentState in self.finalStates:
			return True
		else:
			return False              

	def showSchematicDFA(self):
		dfa = {}
		holdRules = {}
		for rule in self.Rules:
			tmp = (rule[0], rule[2])		
			temp2 = rule[1]
			holdRules.update({tmp:temp2})

		dfa['alphabet'] = set(self.alphabet)

		dfa['states'] = set(self.allStates)

		dfa['initial_state']= self.allStates[0]

		dfa['accepting_states'] = set(self.finalStates)

		dfa['transitions'] = holdRules

		automata_IO.dfa_to_dot(dfa,'DFA_Diagram' , '.\\DFA_Schema\\')