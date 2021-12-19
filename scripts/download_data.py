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
import arxiv
import networkx as nx
import os

# Time libraries
from dateutil.relativedelta import relativedelta
from datetime import datetime, timezone

# Globals
max_results = 400
date_limit = datetime.now(timezone.utc) - relativedelta(years=6)
searched_papers = set()
searched_authors = set()
debug = True
save_name = "arxiv.net"

# Root graph
G = nx.Graph()

# Check if the file already exists
if os.path.isfile(save_name):
	G = nx.read_pajek(save_name)
	searched_authors = set(G.nodes)
	searched_papers = set(map(lambda x : x[2], G.edges))

# Reset wierd dates
reset_date = lambda x : datetime(*map(int, str(x).split()[0].split('-')))

# Query ArXiv articles from a specific author
def query_by_author(author_name):
	return arxiv.Search(query="au:" + author_name, max_results=max_results)

# Filter results of a query with authors
# Check that this entry was not already checked and that the authors and conform
def filter_query(results, author):
	return filter(lambda x : (x.updated >= date_limit) and (x.get_short_id() not in searched_papers) and any(author == x_a.name for x_a in x.authors), results)

# Process a result
def process_result(result, distance_from_root):
	# Add authors as nodes
	G.add_nodes_from(map(lambda x : x.name, result.authors))
	# Add edges
	for author1 in result.authors:
		for author2 in result.authors:
			if author1.name != author2.name:
				if G.has_edge(author1.name, author2.name):
					G[author1.name][author2.name]['weight'] += 1
				else:
					G.add_edge(author1.name, author2.name, weight=1)
	# Mark the publication as seen
	searched_papers.add(result.get_short_id())
	# Browse each authors
	for author in result.authors:
		browse_arxiv(query_by_author(author.name), author.name, distance_from_root=distance_from_root+1)

# Recursively browse ArXiv
def browse_arxiv(s, author_name, distance_from_root=0, threshold_distance=5):
	# Don't query an author which was already searched
	# Don't query an author if we are too far from the original author
	if author_name not in searched_authors and distance_from_root <= threshold_distance:
		# Get the filtered query
		query_filtered = filter_query(s.results(), author_name)
		# Add it to the list of authors
		searched_authors.add(author_name)
		# Process every result
		for result in query_filtered:
			# Process it
			process_result(result, distance_from_root)
		# Debug print
		if debug:
			print("# of papers -> ", len(searched_papers))
			print("# of authors -> ", len(searched_authors))
		# Save
		nx.write_pajek(G, save_name)
		if debug:
			print("Saved !")

# Reference author
root_author = "Eric Moulines"

# Run the algorithm
browse_arxiv(query_by_author(root_author), root_author)
