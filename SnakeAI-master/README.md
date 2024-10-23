# Snake Game AI

![alt text](https://media.giphy.com/media/3oKIPDUvDdTO5yOBHi/giphy.gif "Snake AI In Action")

The AI that plays the game uses the A Star Search Algorithm to find the least cost path. The AI uses the Euclidian distance from the head of the snake to the food as a heurstic (an admissible heuristic, as this never overestimates the cost of reaching the goal) to get better results than Dijkstra's least cost path Algorithm.

Snake Game GUI built using TkInter python module. 



## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development.


Clone the repo from the command line

```
git clone https://github.com/chankyuoh/SnakeGame.git
```

go into the newly created directory called 'SnakeGame'

```
cd SnakeGame
```

Run the game

```
python SnakeGame.py
```
