<h2> Following are the changes that took place in the Graph Interface Library after building the client.</h2> <br/>
1. Initially, for the addEdgeToGraph method, we had passed 3 arguments namely source node, target node and the cost. But after going through the project 02 description
we realized that we need to handle multiple graph clients that would be interacting with each other and hence we need to define exactly which graph do we want to add an edge to.
Hence we passed another argument called as the graphName which maked it easy to find the particular graph client with name as graphName and the specified edge to it. <br/>
