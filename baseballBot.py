from flask import Flask, request
import os
from random import randrange, shuffle

app = Flask(__name__)

##### Some global variables for running the game

current = ""                 # No game: "", bot at bat:"B", bot pitching: "P"
xyz = []                     # Actual sequence to be guessed
untried = list(range(10))    # Digits the bot hasn't yet tried
strikes = []                 # Digits which got the bot a strike
last_guesses = []            # The bot's prior guesses

##### Initializing a game

@app.route("/playball", methods=["POST"])
def playball():
    
    global current
    global xyz
    global untried
    global strikes
    global last_guesses
        
    # If there's already a game going on, remind the player
    if(current == "P"):
        return("You're already playing a game. The bot has a sequence of three digits. Guess with */guess xyz*.")
    if(current == "B"):
        return("You're already playing a game. The bot guessed *{0}* against your sequence, *{1}*.".format(last_guesses[-1], xyz))
    
    # Start the game with the player at bat against a random sequence
    if(request.form["text"] == "bat"):
        current = "P"
        xyz = [randrange(10),randrange(10),randrange(10)]
        return("The bot has a sequence of three digits. Guess with */guess xyz*.".format(xyz))
        
    # Start the game with the bot at bat against the sequence given by the player
    if(len(request.form["text"]) > 0):    
        try:
            xyz = [int(char) for char in list(request.form["text"])]
            xyz = xyz[:3] + [0 for i in range(3 - len(xyz))]
            untried = list(range(10))
            shuffle(untried)
            strikes = []
            last_guesses = []
            current = "B"
            return(bot_guess())
        except:
            pass
    
    # If no return-statement breaks the function, give the player instructions
    return("""Type */playball xyz* to pitch the digits xyz at the bot.
           \nOr, type */playball bat* to let the bot pitch to you.""")
    
##### Player guesses the sequence and the bot responds
    
@app.route("/guess", methods=["POST"])
def guess():
    
    global current
    global xyz
    
    # Is the player allowed to guess?
    if(current != "P"):
        return("The bot isn't pitching for you right now.")
        
    # Break down the guess    
    guess = [int(char) for char in list(request.form["text"])]
    guess = guess[:3] + [0 for i in range(3 - len(guess))]
    
    # Count strikes and balls
    strike_count = 0
    ball_count = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if xyz[i] == guess[j]:
                if i == j:
                    strike_count += 1
                else:
                    ball_count += 1
            
    # If the player wins, break!        
    if(strike_count == 3):
        end_the_game()
        return("Three strikes! You win! It was *{0}*! Thanks for playing!".format(guess))
            
    # Otherwise, report strikes and balls    
    return("""*{0}* strike(s), right number, right place.
           \n*{1}* ball(s), right number, wrong place.""".format(strike_count, ball_count))
    
##### Player reponds to the bot's guess
    
@app.route("/reply", methods=["POST"])
def reply():
    
    global current
    global strikes
    global last_guesses
    
    # Is the player in position to respond?
    if(current != "B"):
        return("The bot isn't batting against you right now.")
        
    # Count reported strikes and balls    
    text = request.form["text"].lower()
    strike_count = text.count("s")
    # ball_count = text.count("b") # The bot doesn't care for balls
    
    # If the bot wins, break!
    if(strike_count == 3):
        end_the_game()
        return("Three stikes! The bot wins! Thanks for playing!")
        
    # The bot's first phase of attack is identifying the digits which strike    
    if(strike_count > 0 and len(set(last_guesses[-1])) == 1):
        strikes += [last_guesses[-1][0] for i in range(strike_count)]
    
    # Return the bot's next guess
    return(bot_guess())
    
##### End the current game
    
@app.route("/endgame", methods=["POST"])
def endgame():
    end_the_game()
    return("No game ongoing.")
    
def end_the_game():
    
    global current
    global xyz
    global untried
    global strikes
    global last_guesses
    
    current = ""
    xyz = []
    untried = list(range(10))
    strikes = []
    last_guesses = []
    
##### How the bot chooses its next guess
    
def bot_guess():
    
    global untried
    global strikes
    global last_guesses
    
    # If the bot has identified the three digits...
    if(len(strikes) == 3):
        guess = strikes.copy()
        # ...sort them in a new random order
        while(guess in last_guesses):
            shuffle(guess)
    # Otherwise, try three of the same digit to see if they get strikes
    else:
        random_untried = untried.pop()
        guess = [random_untried] * 3
        
    # Keep track of tried guesses    
    last_guesses.append(guess)    
        
    return("""The bot is guessing *{0}* against your sequence *{1}*. 
           \nReply with */reply*, then an *s* for every strike and a *b* for every ball.""".format(guess, xyz, untried, strikes, last_guesses))
    
##### Host the app locally
    
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)