# Pig Gamble

Pig Gamble is a simple multiplayer dice game built in Python. The concept is based on taking risks: players can keep rolling to earn more points, but rolling a 1 causes them to lose their turn score and the turn ends.

## How the game works
- The game supports 2 to 4 players.
- On each turn, a player can choose to roll the dice repeatedly.
- Every roll from 2 to 6 adds that value to the player's current turn score.
- If a player rolls a 1, they lose their current turn score and their turn ends.
- A player can stop at any time and keep the points they earned during that turn.
- The first player to reach or exceed 100 points wins the game.

## Game concept
This is a classic risk-versus-reward game. The more a player rolls, the more points they can gain, but the greater the chance of losing everything earned on that turn.

## How to run
Run the game with:

```bash
python projecttest.py
```
