<h2> Following are the changes that took place in the GraphInterface Library</h2><br>
1. We removed the Node helper class that we initially proposed in Project 01. We had initially implemented this class considering that a node or vertex would be
represented using its separate class but after reading the description of Project 02, we realized that the nodes or vertices would be represented using their name
which meant that the class would be a string class and hence we altogether dropped the Node class. <br>
2. We initially made a slight error in designing the interface in Project 01 by adding a constructor to the Graph Interface class not realizing that this class is never going to be
instantiated. We corrected this issue and removed the interface constructor. <br>
3. We changed the names of the methods in the Graph Interface to follow the snake case convention and changed the name of joinTwoGraphs method to join, to make it generalized. <br/>

