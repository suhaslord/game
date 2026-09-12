# Arena Survival Game

A small top-down arcade prototype written in Python and Pygame. Control a player, aim with the mouse, and survive waves of chasing, shooting, and fast-moving enemies.

## Run locally

Install Python 3 and run these commands from the repository root:

```sh
python -m pip install pygame
python main.py
```

## Controls

- **W / A / S / D:** move.
- **Mouse:** aim; click to fire.
- **Close the window:** exit.

The health bar appears in the upper-left corner. The session ends when health reaches zero. The game uses an 800 × 600 window and caps the loop at 60 FPS.

## Project scope

An early learning project exploring game loops, movement, projectiles, collision detection, and enemy behavior. All game logic is in [main.py](main.py); graphics are drawn with Pygame primitives. There is no menu, save system, or packaged executable.
