# Le Jeu De La Vie (Conway's Game of Life)

The universe of the Game of Life is an infinite, two-dimensional orthogonal grid of square cells,
each of which is in one of two possible states, live (blank places) or dead (black squares), (or populated and unpopulated, respectively).
Every cell interacts with its eight neighbours, which are the cells that are horizontally, vertically, or diagonally adjacent.

At each step in time, the following transitions occur:
- Any live cell with fewer than two live neighbours dies, as if by underpopulation.
- Any live cell with two or three live neighbours lives on to the next generation.
- Any live cell with more than three live neighbours dies, as if by overpopulation.
- Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

[cf Wikipedia](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)

## Controls
You can :
- place and remove cells by clicking on the grid
- move the camera over the grid dragging your mouse
- zoom with the mouse wheel
- go to the center of the grid with `C`
- reset the simulation with `R`
- manually calculate a generation with `space`
- automatically calculate :
  - 2 generations per second with `2`
  - 5 generations per second with `3`
  - 10 generations per second with `4`
- stop the automatic calculation with `1`
