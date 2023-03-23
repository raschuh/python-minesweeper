# Python-Minesweeper

Yet another implementation of Minesweeper in Python.

This game was created as a portfolio project for Codecademy's Computer Science Career Path. 

## Install

### Dependencies
- blessed
- questionary

Run `pip install blessed questionary` to install the dependencies.

## How to Play

1. In your favourite Terminal, enter `python3 main.py` to start the game.
2. Enter a command as listed below to play the game.
- `o[row][col]` Open a hidden cell where [row] and [col] corresponds to the alphanumeric grid coordinates seen on the screen.
- `f[row][col]` Flag or unflag an unopened cell that you suspect hiding a mine.
- `s[level]` Change the difficulty level. [level] -> 0 for easy (8x8 with 10 mines), 1 for medium (16x16 with 40 mines), and 2 for hard (30x16 with 99 mines).
- `r` Reset the game to the initial startup state.
- `q` Quit the game.
3. Enjoy and good hunting!


