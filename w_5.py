#from __future__ import print_function, division
from w_4 import *
from collections import Counter
import copy
import random
import sys
import numpy as np

def ChromosomeToCycle(l):
	nodes = []
	for i in range(0, len(l)):
		start = l[i]
		if start > 0:
			nodes.append(2*start - 1)
			nodes.append(2*start)
		else:
			nodes.append(-2*start)
			nodes.append(-2*start - 1)
	return nodes

def CycleToChromosome(nodes):
	l = []
	i = 0
	while i < len(nodes):
		if nodes[i] < nodes[i+1]:
			l.append(nodes[i+1]//2)
		else:
			l.append(-nodes[i+1]//2)
		i += 2
	return l

def ColoredEdges(P):
	edges = []
	for chromosome in P:
		nodes = ChromosomeToCycle(chromosome)
		i = 1
		while i < len(nodes) - 2:
			edges.append((nodes[i], nodes[i+1]))
			i += 2
		edges.append((nodes[len(nodes) - 1], nodes[0]))

	return edges

def GraphToGenome(genome_graph):
	P = []
	i = 0
	visited = []
	adj = np.zeros(len(genome_graph)*2, dtype = np.int)
	for t in genome_graph:
		adj[t[0]-1] = t[1]-1
		adj[t[1]-1] = t[0]-1
	for t in genome_graph:
		start = t[0]
		if start in visited:
			continue
		visited.append(start)
		if start%2 == 0:
			find = start - 1
		else:
			find = start + 1
		chromosome = []
		while True:
			if start%2 == 0:
				chromosome.append(start//2)
			else:
				chromosome.append(-(start+1)//2)
			next = adj[start-1]+1
			visited.append(next)
			if next == find:
				P.append(chromosome)
				break
			if next%2 == 0:
				start = next - 1
			else:
				start = next + 1
			visited.append(start)
	genome = []
	for chromosome in P:
		x = chromosome.pop()
		genome.append([x] + chromosome)

	return genome

	#doesn't work for 2 break induced genomes ==>

	'''
	while i < len(genome_graph):
		chromosome = []
		tup = genome_graph[i]
		current = tup[0]
		if tup[0]%2 == 0:
			find = tup[0] - 1
		else:
			find = tup[0] + 1
		chromosome.append(current)
		chromosome.append(tup[1])
		i += 1
		while i < len(genome_graph):
			tup = genome_graph[i]
			chromosome.append(tup[0])
			chromosome.append(tup[1])
			i += 1
			if tup[1] == find:
				P.append(chromosome)
				break
		#print(P, '!!!')
	genome = []
	for cycle in P:
		x = cycle.pop()
		cycle = [x] + cycle
		genome.append(Format(CycleToChromosome(cycle)))
	return ''.join(genome)
	'''

def NumberOfCycles(blue, red):
	#forked form ngaude/sandbox
	cycles = []
	size = len(blue)+len(red) 
	adj = np.zeros(shape = (size,2), dtype = np.int)
	#print(adj)
	visited = np.zeros(shape = size, dtype = np.bool)
	#print(visited)
	for e in blue:
		adj[e[0]-1,0] = e[1]-1
		adj[e[1]-1,0] = e[0]-1
	for e in red:
		adj[e[0]-1,1] = e[1]-1
		adj[e[1]-1,1] = e[0]-1
	#print(adj)
	#sys.exit()
	for node in range(size):
		if not visited[node]:
			visited[node] = True
			head = node
			cycle = [head+1]
			# arbitrary we start with a blue edge
			color = 0
			while (True):
				node = adj[node,color]
				if (node == head):
					cycles.append(cycle)
					break
				cycle.append(node+1)
				visited[node] = True
				color = (color+1) % 2
	return cycles


def TwoBreakDistance(P, Q):
	edges_P = ColoredEdges(P)
	edges_Q = ColoredEdges(Q)
	blocks = len(edges_P)
	cycles = NumberOfCycles(edges_P, edges_Q)
	return blocks - len(cycles)
	#return None

def TwoBreakOnGenomeGraph(genome_graph, i_1, i_2, i_3, i_4):
	l = [(i_1, i_2), (i_2, i_1), (i_3, i_4), (i_4, i_3)]
	g = [tup for tup in genome_graph if tup not in l]
	g.append((i_1, i_3))
	g.append((i_2, i_4))
	'''
	if (i_1, i_2) in genome_graph:
		index_1 = genome_graph.index((i_1, i_2))
		g.insert(index_1, (i_4, i_2))
	else:
		index_1 = genome_graph.index((i_2, i_1))
		g.insert(index_1, (i_2, i_4))
	if (i_3, i_4) in genome_graph:
		index_2 = genome_graph.index((i_3, i_4))
		g.insert(index_2, (i_3, i_1))
	else:
		index_2 = genome_graph.index((i_4, i_3))
		g.insert(index_2, (i_1, i_3))
	'''
	return g

def TwoBreakOnGenome(P, i_1, i_2, i_3, i_4):
	genome_graph = ColoredEdges(P)
	#print(genome_graph)
	genome_graph = TwoBreakOnGenomeGraph(genome_graph, i_1, i_2, i_3, i_4)
	#print(genome_graph)
	P = GraphToGenome(genome_graph)
	return P
def TwoBreakSorting(edges_P, edges_Q):
	red_edges = ColoredEdges([edges_Q])
	sequence = []
	sequence.append(edges_P)
	P = [edges_P]
	Q = [edges_Q]
	while TwoBreakDistance(P, Q) > 0:
		cycles = NumberOfCycles(ColoredEdges(P), red_edges)
		for cycle in cycles:
			if len(cycle) >= 4:
				P = TwoBreakOnGenome(P, cycle[0], cycle[1], cycle[3], cycle[2])
				sequence.append(P)
	genome = []
	for chromosome in sequence:
		if len(chromosome) >= 4 and type(chromosome[0]) == int:
			temp = []
			for num in chromosome:
				if num > 0:
					temp.append('+' + str(num))
				else:
					temp.append(str(num))
			
			line = ' '.join(temp)
			line = '(' + line + ')'
			genome.append(line)
		else:
			newline = ''
			for c in chromosome:
				temp = []
				for num in c:
					if num > 0:
						temp.append('+' + str(num))
					else:
						temp.append(str(num))
				line = ' '.join(temp)
				line = '(' + line + ')'
				newline += line
			genome.append(newline)
	for chromosome in genome:
		print(chromosome)
	return None

def ReverseComplement(string):
	my_str = []
	d = {'A': 'T', 'G': 'C', 'T': 'A', 'C': 'G'}
	for i in range(0, len(string)):
		my_str.append(d[string[i]])

	my_str = my_str[::-1]
	my_str = "".join(my_str)
	return my_str

def SharedKmers(k, dna_a, dna_b):
	d_a = {}
	xy = []
	for i in range(0, len(dna_a) - k + 1):
		kmer = dna_a[i: i+k]
		d_a[kmer] = []
	for i in range(0, len(dna_a) - k + 1):
		kmer = dna_a[i: i+k]
		d_a[kmer].append(i)
	for i in range(0, len(dna_b) - k + 1):
		kmer = dna_b[i: i+k]
		reverse_kmer = ReverseComplement(kmer)
		if kmer in d_a:
			for pos in d_a[kmer]:
				xy.append((pos, i))
		elif reverse_kmer in d_a:
			for pos in d_a[reverse_kmer]:
				xy.append((pos, i))
	for tup in xy:
		print(tup)
	return len(xy)

'''
x = '+1 +2 +3 +4)(+5 +6)(+7 -9 -8'.split(')(')
P = []
for chromosome in x:
	temp = chromosome.split(' ')
	l = []
	for num in temp:
		if num[0] == '-':
			num = -1*int(num[1:])
		else:
			num = int(num[1:])
		l.append(num)
	P.append(l)
print(ColoredEdges(P))

'''
'''
k = 3
dna_a = 'TCAGTTGGCCTACAT'
dna_b = 'CCTACATGAGGTCTG'
print(SharedKmers(k, dna_a, dna_b))
'''

#x = '-1 +2 -3 -4 -5 -6 -7 +8 +9 +10 +11 +12 +13 +14 +15 -16 -17 -18 +19 -20 +21 +22 -23 -24 +25 -26 -27 +28 -29 -30 +31 +32 +33 -34 -35 +36 +37 +38 +39 -40 +41 +42 -43 +44 +45 +46 -47 +48 +49 +50 -51 +52 +53 +54 -55 -56 -57 +58 -59 -60 -61 +62 -63 +64 +65 -66 -67'
'''
x = '+1 -2 -3 +4 -5 -6 +7 +8 -9 +10 +11 +12 -13 +14 -15 -16 +17 -18 +19 +20 -21 +22 +23 -24 +25 +26 -27 +28 +29 -30 -31 +32 +33 -34 +35 -36 -37 -38 -39 +40 -41 +42 +43 +44 +45 -46 -47 +48 -49 +50 +51 -52 +53 +54 +55 +56 -57 -58 -59 -60 +61 +62 -63 +64'
x = x.split(' ')
l = []
for num in x:
	if num[0] == '-':
		num = -1*int(num[1:])
		l.append(num)
	else:
		num = int(num[1:])
		l.append(num)

P = [l]
i_1, i_2, i_3, i_4 = 121, 119, 109, 108
print(TwoBreakOnGenome(P, i_1, i_2, i_3, i_4))
'''


'''
x = '2 1 3 4 6 5 8 7 9 10 12 11 13 14 15 16 18 17 19 20 22 21 23 24 25 26 28 27 29 30 31 32 34 33 36 35 38 37 39 40 42 41 44 43 46 45 47 48 49 50 52 51 53 54 56 55 57 58 60 59 61 62 64 63 66 65 68 67 69 70 72 71 73 74 75 76 77 78 80 79 81 82 84 83 86 85 88 87 89 90 92 91 93 94 96 95 97 98 99 100 101 102 104 103 105 106 108 107 110 109 112 111 114 113 115 116 118 117 119 120 122 121'
x = x.split(' ')
nodes = [int(i) for i in x]
print(Format(CycleToChromosome(nodes)))
''' 
'''
x = '-1 -2 +3 +4 +5 +6 +7 +8 -9 -10 +11 -12 +13 +14 -15 +16 +17 -18 +19 +20 +21 -22 +23 +24 +25 -26 -27 -28 +29 +30)(-31 -32 -33 -34 -35 +36 +37 +38 -39 -40 -41 -42 +43 +44 +45 +46 -47 +48 -49 -50 +51 +52 +53 +54 -55 -56 -57 +58 +59 +60 -61)(+62 -63 +64 -65 +66 +67 -68 +69 +70 +71 +72 -73 -74 +75 +76 +77 -78 +79 +80 -81 -82 +83 +84 -85 +86)(-87 -88 +89 +90 -91 -92 -93 +94 -95 +96 +97 +98 +99 +100 +101 +102 +103 +104 +105 +106 -107 -108 -109 -110 +111)(-112 -113 -114 +115 -116 +117 -118 -119 -120 -121 -122 -123 +124 +125 +126 +127 -128 -129 -130 -131 -132 +133 -134 +135)(+136 -137 +138 +139 +140 +141 +142 -143 -144 +145 -146 -147 +148 +149 +150 +151 -152 -153 -154 +155 -156 -157 +158 +159 +160 +161 +162 +163 -164)(-165 -166 -167 +168 -169 -170 +171 -172 -173 +174 -175 -176 -177 +178 +179 -180 -181 +182 +183 -184 +185 +186 +187 -188 +189 -190)(-191 -192 -193 +194 -195 -196 -197 +198 -199 +200 +201 +202 +203 +204 -205 +206 +207 +208 +209 +210 +211 -212 -213 -214'
x = x.split(')(')
for i in range(0, len(x)):
	l = []
	item = x[i].split(' ')
	for num in item:
		if num[0] == '-':
			num = -1*int(num[1:])
			l.append(num)
		else:
			num = int(num[1:])
			l.append(num)
	x[i] = l
print(ColoredEdges(x))
'''

'''
P = '+11 -1 -2 -12 -9 +6 +14 +10 +8 +13 +7 -5 +4 +3'.split(' ')
Q = '-13 +8 +10 +6 +2 +14 -9 -1 +5 -3 +12 +7 -4 -11'.split(' ')
edges_P = []
for num in P:
	if num[0] == '-':
		num = -1*int(num[1:])		
	else:
		num = int(num[1:])
	edges_P.append(num)
edges_Q = []
for num in Q:
	if num[0] == '-':
		num = -1*int(num[1:])		
	else:
		num = int(num[1:])
	edges_Q.append(num)
print(TwoBreakSorting(edges_P, edges_Q))
'''
