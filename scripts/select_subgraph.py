# MIT License

# Copyright (c) 2021 Louis Popi

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Libraries
import networkx as nx
from scholarly import scholarly, ProxyGenerator
import pickle
import os.path
import pprint
from collections import Counter

# Proxy generator
pg = ProxyGenerator()
pg.Tor_External(tor_sock_port=9050, tor_control_port=9051, tor_password="scholarly_password")
scholarly.use_proxy(pg)

# Global variables
name = "Eric Moulines"
save_path = "arxiv.net"
max_depth = 2

# Open graph
G = nx.Graph(nx.read_pajek(save_path))

# Get the list of all nodes
selected_nodes = set()
def select_nodes(node, depth=0):
	# Add node to set
	selected_nodes.add(node)
	if depth < max_depth:
		# Browse
		for n in G[node].keys():
			select_nodes(n, depth=depth+1)

# Fill graph
select_nodes(name)

# Print the ratio
print("Selected {} / {} = {}%".format(len(selected_nodes), G.number_of_nodes(), round(len(selected_nodes) / G.number_of_nodes() * 100)))

# Build a new graph
G_new = G.subgraph(selected_nodes)

# API to get the domain
def get_email_domain(name):
	# Do the actual search
	search_query = scholarly.search_author(name)
	# Sort the results by citations
	sorted_search_query = sorted(search_query, key=lambda x : x['citedby'] if 'citedby' in x else 0, reverse=True)
	# Return the email domain
	if len(sorted_search_query) > 0 and 'citedby' in sorted_search_query[0]:
		return sorted_search_query[0]['email_domain']
	else:
		return None

# Set all email extensions
domain_save = "domain_mapping.pickle"

if os.path.isfile(domain_save):
	domain_mapping = pickle.load(open(domain_save, "rb"))
else:	
	domain_mapping = {}

c = 0
number_of_nodes = G_new.number_of_nodes()
for name in G_new.nodes.keys():
	if name not in domain_mapping:	
		domain = get_email_domain(name)
		if domain is not None:
			domain_mapping[name] = domain
		else:
			domain_mapping[name] = "@other"
	# Save from time to time
	c += 1
	if c % 50 == 0: pickle.dump(domain_mapping, open(domain_save, "wb"))
	print("Progress -> {}%".format(round(c/number_of_nodes * 100,2)))

# Only keep the last part
def process_domain(domain):
	domain_split = domain[1:].split('.')
	if domain == "@other" or domain == '@unknown' or len(domain) == 0:
		return "@other"
	elif len(domain_split) >= 3 and (domain_split[-2] == "ac" or domain_split[-2] == "edu"):
		return "@" + domain_split[-1] + "-" + '.'.join(domain_split[-3:])
	elif len(domain_split) >= 2:
		return "@" + domain_split[-1] + "-" + '.'.join(domain_split[-2:])
	else:
		return "@" + domain_split[-1] + "-" + domain[1:]

for node, domain in domain_mapping.items():
	p_domain = process_domain(domain)
	if p_domain[1:] in ['edu-polytechnique.edu', 'org-polytechnique.org', 'fr-polytechnique.fr', 'eu-telecom-sudparis.eu', 'fr-telecom-paris.fr', 'fr-ensae.fr']:
		p_domain = '@fr-ip-paris.fr'
	domain_mapping[node] = p_domain

# Fill gaps
for node, deg in sorted(G_new.degree, key=lambda x: x[1], reverse=True):
	# Check if we lack the domain for it
	if not isinstance(domain_mapping[node], str) or len(domain_mapping[node]) == 0 or domain_mapping[node] == "@other":
		# Build a counter of its neighbors
		c = {}
		for name in G_new.neighbors(node):
			if domain_mapping[name] in c: c[domain_mapping[name]] += G_new[node][name]["weight"]
			else: c[domain_mapping[name]] = G_new[node][name]["weight"]
		# Get the max
		m = max(c, key=c.get)
		if m == "@other":
			del c["@other"]
			m = max(c, key=c.get)
		domain_mapping[node] = m

# Set nodes under one to other
c = Counter(domain_mapping.values())
for node, domain in domain_mapping.items():
	if c[domain] <= 2: domain_mapping[node] = "@" + domain.split(".")[-1] + "-other"

# Find remaining other
for node, domain in domain_mapping.items():
	if not isinstance(domain_mapping[node], str) or len(domain_mapping[node]) == 0 or domain_mapping[node] == "@other":
		print("domain_mapping[\"{}\"] = \"\"".format(node))

# Print statistics
pprint.pprint(Counter(domain_mapping.values()))

# Dump the mapping
pickle.dump(domain_mapping, open(domain_save, "wb"))

# Update the graph
nx.set_node_attributes(G_new, domain_mapping, 'domain')

# Export
name_split = save_path.split('.')
nx.write_pajek(G_new, ''.join(name_split[:-1] + ["_subgraph", ".", name_split[-1]]))
print("Exported !")