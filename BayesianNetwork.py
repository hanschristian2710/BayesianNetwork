#!/usr/bin/env python
""" generated source for module BayesianNetwork """
from Assignment4 import *
import random

# 
#  * A bayesian network
#  * @author Panqu
#  
class BayesianNetwork(object):
    """ generated source for class BayesianNetwork """
    # 
    #     * Mapping of random variables to nodes in the network
    #     
    varMap = None

    # 
    #     * Edges in this network
    #     
    edges = None

    # 
    #     * Nodes in the network with no parents
    #     
    rootNodes = None

    # 
    #     * Default constructor initializes empty network
    #     
    def __init__(self):
        """ generated source for method __init__ """
        self.varMap = {}
        self.edges = []
        self.rootNodes = []

    # 
    #     * Add a random variable to this network
    #     * @param variable Variable to add
    #     
    def addVariable(self, variable):
        """ generated source for method addVariable """
        node = Node(variable)
        self.varMap[variable]=node
        self.rootNodes.append(node)

    # 
    #     * Add a new edge between two random variables already in this network
    #     * @param cause Parent/source node
    #     * @param effect Child/destination node
    #     
    def addEdge(self, cause, effect):
        """ generated source for method addEdge """
        source = self.varMap.get(cause)
        dest = self.varMap.get(effect)
        self.edges.append(Edge(source, dest))
        source.addChild(dest)
        dest.addParent(source)
        if dest in self.rootNodes:
            self.rootNodes.remove(dest)

    # 
    #     * Sets the CPT variable in the bayesian network (probability of
    #     * this variable given its parents)
    #     * @param variable Variable whose CPT we are setting
    #     * @param probabilities List of probabilities P(V=true|P1,P2...), that must be ordered as follows.
    #       Write out the cpt by hand, with each column representing one of the parents (in alphabetical order).
    #       Then assign these parent variables true/false based on the following order: ...tt, ...tf, ...ft, ...ff.
    #       The assignments in the right most column, P(V=true|P1,P2,...), will be the values you should pass in as probabilities here.
    #     
    def setProbabilities(self, variable, probabilities):
        """ generated source for method setProbabilities """
        probList = []
        for probability in probabilities:
            probList.append(probability)
        self.varMap.get(variable).setProbabilities(probList)

    # 
    #     * Returns an estimate of P(queryVal=true|givenVars) using rejection sampling
    #     * @param queryVar Query variable in probability query
    #     * @param givenVars A list of assignments to variables that represent our given evidence variables
    #     * @param numSamples Number of rejection samples to perform
    #     
    def performRejectionSampling(self, queryVar, givenVars, numSamples):
        """ generated source for method performRejectionSampling """
        #  TODO
        def priorSampling(varMap):
            x = {}
            for var in sorted(varMap.keys()):
                r = random.random()
                if r <= varMap.get(var).getProbability(x, True):
                    x[var.getName()] = True
                else:
                    x[var.getName()] = False
            return x
        
        def normalize(n1, n2):
            sum = n1 + n2
            if sum == 0:
                return 0.0
            return (float(n1) / sum)
        
        n1 = 0
        n2 = 0
        for j in range(1, numSamples):
            x = priorSampling(self.varMap)
            consistent = True
            for v in givenVars:
                if x[v.getName()] != givenVars[v]:
                    consistent = False
                    break
            if consistent:
                if x[queryVar.getName()]:
                    n1 = n1 + 1
                else:
                    n2 = n2 + 1
        return normalize(n1, n2)

    # 
    #     * Returns an estimate of P(queryVal=true|givenVars) using weighted sampling
    #     * @param queryVar Query variable in probability query
    #     * @param givenVars A list of assignments to variables that represent our given evidence variables
    #     * @param numSamples Number of weighted samples to perform
    #     
    def performWeightedSampling(self, queryVar, givenVars, numSamples):
        """ generated source for method performWeightedSampling """
        #  TODO
        def weightedSample(varMap, givenVars):
            w = 1
            x = Sample()
            for var in givenVars:
                x.setAssignment(var.getName(), givenVars[var])
            for var in sorted(varMap.keys()):
                if x.getValue(var.getName()) is not None:
                    w = x.getWeight() * varMap.get(var).getProbability(x.assignments, x.assignments.get(var.getName()))
                    x.setWeight(w)
                else:
                    r = random.random()
                    if r <= varMap.get(var).getProbability(x.assignments, True):
                        x.assignments[var.getName()] = True
                    else:
                        x.assignments[var.getName()] = False
            return (x.assignments, x.weight)
        
        def normalize(n1, n2):
            sum = n1 + n2
            if sum == 0:
                return 0.0
            return (float(n1) / sum)
                    
        n1 = 0
        n2 = 0
        for j in range(1, numSamples):
            (x, w) = weightedSample(self.varMap, givenVars)
            if x[queryVar.getName()]:
                n1 = n1 + w
            else:
                n2 = n2 + w
        return normalize(n1, n2)

    # 
    #     * Returns an estimate of P(queryVal=true|givenVars) using Gibbs sampling
    #     * @param queryVar Query variable in probability query
    #     * @param givenVars A list of assignments to variables that represent our given evidence variables
    #     * @param numTrials Number of Gibbs trials to perform, where a single trial consists of assignments to ALL
    #       non-evidence variables (ie. not a single state change, but a state change of all non-evidence variables)
    #     
    def performGibbsSampling(self, queryVar, givenVars, numTrials):
        """ generated source for method performGibbsSampling """
        #  TODO
        def normalize(n1, n2):
            sum = n1 + n2
            if sum == 0:
                return 0.0
            return (float(n1) / sum)
        
        def getNonEvidenceVar(varMap, givenVars):
            nonEvidenceVar = []
            for var in varMap.keys():
                if var not in givenVars:
                    nonEvidenceVar = nonEvidenceVar + [var]
            return nonEvidenceVar
        
        def initX(varMap, nonEvidenceVar):
            x = {}
            for var in varMap.keys():
                if var in nonEvidenceVar:
                    r = random.random()
                    if r <= 0.5:
                        x[var.getName()] = True
                    else:
                        x[var.getName()] = False
                else:
                    x[var.getName()] = givenVars[var]
            return x
        
        def getMarkovVar(varMapNode):
            markov = []
            for p in varMapNode.getParents():
                markov.append(p)
            for c in varMapNode.getChildren():
                if c not in markov:
                    markov.append(c)
                    for p in c.getParents():
                        if(p != varMapNode) and (p not in markov):
                            markov.append(p)
            return markov
        
        def markovProbability(varMap, var, x, tOrF):
            temp = {}
            for parent in varMap[var].getParents():
                temp[parent.getVariable().getName()] = x[parent.getVariable().getName()]
            pParent = varMap[var].getProbability(temp, tOrF)
            pChild = 1.0
            for child in varMap[var].getChildren():
                temp = {}
                for childParent in child.getParents():
                    if (childParent.getVariable().equals(varMap[var].getVariable())):
                        temp[varMap[var].getVariable().getName()] = tOrF
                    else:
                        temp[childParent.getVariable().getName()] = x[childParent.getVariable().getName()]
                pChild = pChild * child.getProbability(temp, x[child.getVariable().getName()])
            return pParent * pChild
        
        n1 = 0
        n2 = 0
        z = getNonEvidenceVar(self.varMap, givenVars)
        x = initX(self.varMap, z)
        for j in range(1, numTrials):
            for var in z:
                p = normalize(markovProbability(self.varMap, var, x, True), markovProbability(self.varMap, var, x, False))
                r = random.random()
                if p >= r:
                    x[var.getName()] = True
                else:
                    x[var.getName()] = False
                if x[queryVar.getName()]:
                    n1 = n1 + 1
                else:
                    n2 = n2 + 1
        return normalize(n1, n2)

