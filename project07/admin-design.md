<h4> We had to make the following changes to the Administrator interface throughout this project</h4>
1. We removed the board, current_player, players, game_over, and stock_market attributes from the Acquiregame class and instead created an instance of banker and 
acquire classes. <br/>
2. The acquire instance maintains a state object that has the current board and player's information. The players attribute maintains a list of players where a player is
an instance of the Player class. The player class has information about the player's name, player tiles, player shares, and the cash he has.  <br/>
3. The shares maintained by the player are an instance of the Share class which has attributes about the hotel to which the share belongs and the number of such shares belonging to that player. <br/>
4. The banker instance maintains attributes about remaining tiles, remaining hotels, and remaining shares per hotel and stock market details.  <br/>
5. The banker class has methods to update tiles, update hotels, update shares, and give a new tile to the player.  <br/>
6. All these individual classes are a part of the Administrator interface indirectly.   <br/>
7. Additionally the Administrator has a method called place which checks for the effect of placing a player's tile on board and the corresponding output state, buy method 
which has functionality for buying shares, a done method that gives a new tile to the player and switches to the next player.   <br/>
8. The setup method remains as it as which sets the board up.  <br/>

