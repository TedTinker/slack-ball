from flask import Flask, jsonify, request
import os
from random import randrange, shuffle

app = Flask(__name__)

#####

current = ""
xyz = []
untried = list(range(10))
strikes = []
last_guesses = []

#####

@app.route("/playball", methods=["POST"])
def playball():
    
    global current
    global xyz
    global untried
    global strikes
    global last_guesses
        
    if(current == "P"):
        return("You're already playing a game. The bot has a sequence of three digits. Guess with */guess xyz*.")
    if(current == "B"):
        return("You're already playing a game. The bot guessed *{0}* against your sequence, *{1}*.".format(last_guesses[-1], xyz))
    
    if(request.form["text"] == "bat"):
        current = "P"
        xyz = [randrange(10),randrange(10),randrange(10)]
        return("The bot has a sequence of three digits {0}. Guess with */guess xyz*.".format(xyz))
    if(len(request.form["text"]) > 0):    
        try:
            xyz = [int(char) for char in list(request.form["text"])]
            xyz = xyz[:3] + [0 for i in range(3 - len(xyz))]
            untried = list(range(10))
            shuffle(untried)
            strikes = []
            current = "B"
            return(bot_guess())
        except:
            pass
    
    return("""Type */playball xyz* to pitch the digits xyz at the bot.
           \nOr, type */playball bat* to let the bot pitch to you.""")
    
#####
    
@app.route("/guess", methods=["POST"])
def guess():
    
    global current
    global xyz
    if(current != "P"):
        return("The bot isn't pitching for you right now.")
        
    guess = [int(char) for char in list(request.form["text"])]
    guess = guess[:3] + [0 for i in range(3 - len(guess))]
    
    strike_count = 0
    ball_count = 0
    for i in range(0, 3):
        for j in range(0, 3):
            if xyz[i] == guess[j]:
                if i == j:
                    strike_count += 1
                else:
                    ball_count += 1
            
    if(strike_count == 3):
        end_the_game()
        return("Three strikes! You win! It was *{0}*! Thanks for playing!".format(xyz))
            
    return("""*{0}* strike(s), right number, right place.
           \n*{1}* ball(s), right number, wrong place.""".format(strike_count, ball_count))
    
#####
    
@app.route("/reply", methods=["POST"])
def reply():
    
    global current
    global xyz
    global untried
    global strikes
    global last_guesses
    if(current != "B"):
        return("The bot isn't batting against you right now.")
        
    text = request.form["text"].lower()
    strike_count = text.count("s")
    ball_count = text.count("b")
    
    if(strike_count == 3):
        end_the_game()
        return("Three stikes! The bot wins! Thanks for playing!")
        
    if(strike_count > 0 and len(set(last_guesses[-1])) == 1):
        strikes += [last_guesses[-1][0] for i in range(strike_count)]
    
    return(bot_guess())
    
#####
    
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
    
#####
    
def bot_guess():
    
    global xyz
    global untried
    global strikes
    global last_guesses
    
    if(len(strikes) == 3):
        guess = strikes.copy()
        while(guess in last_guesses):
            shuffle(guess)
    else:
        random_untried = untried.pop()
        guess = [random_untried] * 3
        
    last_guesses.append(guess)    
        
    return("""The bot is guessing *{0}* against your sequence *{1}*. 
           \nReply with */reply*, then an *s* for every strike and a *b* for every ball.""".format(guess, xyz, untried, strikes, last_guesses))
    
#####
    
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)