# Graph of arXiv

This repository is a compilation of the tools I built to make the following picture

![Final result](data/arxiv_subgraph.graphml.svg)

You will find

* All the data I scrapped and processed in the folder `data`
* The scripts I used in `scripts`
  * `download_data.py` downloads the raw data from [arXiv](https://arxiv.org/)
  * `select_subgraph.py` does all the preprocessing (and identifies the universities with [Google Scholar](https://scholar.google.com/))
  * `convert_to_graphml.py` is just a small tool to make the outputs of `networkx` compatible with Cytoscape
* The graph is drawn by [Cytoscape](https://cytoscape.org/) with the help of the [EntOptLayout plugin](https://apps.cytoscape.org/apps/entoptlayout)

Here is the [LinkedIn post](https://www.linkedin.com/posts/lgrenioux_en-ce-mois-de-rentr%C3%A9e-%C3%A0-linstitut-polytechnique-activity-6850708113004351488-uS_y) I made about it

> In this month of re-entry at the Polytechnic Institute of Paris, we hear a lot about its impact in the AI research world. So to get an idea, I did some data visualization this weekend 🧠
>
> Here is how the graph below is constructed:
>
> - Each node represents a researcher who has worked at least at the second degree with Eric Moulines, coordinator of my master. The size is proportional to the number of publications. The color represents the academic affiliation of the researcher (Standford, IP Paris, ...): the Americans are in green, the French in blue and the English in red (it is an ultra-simplification).
>
> - Each link represents a collaboration between two scientists: the thicker and redder it is, the more publications the collaboration has resulted in.
>
> 🇫🇷 France has a large presence on this graph (not surprising since the root of the graph is French) and interacts with the whole world! The young nodes of the Paris PI are not the biggest but collaborate with scientists from all over the world: they represent 1% of the collaborations on this graph (which is the highest proportion).
>
> I'm just starting in this kind of visualization 😅 Feel free to give me feedback in the comments or contact me (louis.grenioux@polytechnique.edu) 😇 To search for someone on the graph, you can find the SVG in high quality here: https://lnkd.in/gEMzxibp
>
> Data origin: ArXiv publications from the last 15 years

