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
import argparse

argslist = argparse.ArgumentParser(description="Pajek to GraphML convertor")

argslist.add_argument('pajek_file', metavar='pajek_file', type=str, help='Path to file Pajek input file')
argslist.add_argument('graphml_file', metavar='graphml_file', type=str, help='Path to file GraphML output file')

args = argslist.parse_args()

# Read the Pajek
G = nx.Graph(nx.read_pajek(args.pajek_file))

# Save the graph as GraphML
nx.write_graphml_lxml(G, args.graphml_file)