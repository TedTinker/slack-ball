# slack-ball
Slack-bot for the baseball-game!

The baseball-game (https://www.hackster.io/hyun-woo-park/baseball-game-daecdd) is a particular
instance of the more general game Bull-and-Cows (https://en.wikipedia.org/wiki/Bulls_and_Cows).

One player chooses a sequence of three digits from 0 to 9, and the other player guesses that sequence.
The first player tells the second player how many "strikes" they got (how many correct digits in
the correct places) and how many "balls" they got (correct digits in the incorrect places).
Then the second player guesses again. This proceeds for however-many-attemps, or until the second player nails it.
In this app, the second player has unlimited attempts. 

The app has four slash-commands:
   /playball
   /guess
   /reply
   /endgame
  
"/playball bat" will begin a game with the player at-bat, guessing a sequence of digits chosen by the bot. Then, 
"/guess xyz" will prompt the bot to tell the player how many strikes and balls the player scored with the sequence-attempt xyz.

![At bat](https://github.com/TedTinker/slack-ball/blob/master/pic_bat.png)

"/playball xyz" will begin a game with the player pitching the sequence xyz at the bot, who will automatically guess. Then,
"/reply sbb", for instance, tells the bot that it scored one (s)trike and two (b)alls.  

The game automatically ends when someone wins, but "/endgame" will end the game manually so a new one can be started.

For now, the bot's strategy is very simple. It guesses three of the same digit in a random order, as in
444, 222, 777, 000, and so on. When it counts three strikes total, it knows the three digits of the player's sequence,
so it guesses different orderings of those digits until it stumbles upon the correct one. 

The app is hosted on local port 5000, which was given a public key with ngrok.
