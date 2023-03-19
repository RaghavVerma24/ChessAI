<br/>
<p>
  <p float="left" >
    <a href="https://github.com/RaghavVerma24/ChessAI">
      <img src="https://static-00.iconduck.com/assets.00/chess-icon-512x512-1mnnsw7y.png" alt="Logo" width="80" height="80">
    </a>
    <h1>Chess AI</h1>
  </p>

  <p>
   This project is a chess game with AI implemented using Pygame. The game features different levels of AI difficulty, and allows for both single player and two player modes.
   
  </p>
</p>

<p float="left" align="center">
  <img src="https://github.com/RaghavVerma24/ChessAI/blob/main/assets/readme_imgs/game.png?raw=true" alt="Game Screenshot"  width="400" height="400" />
  <img src="https://github.com/RaghavVerma24/ChessAI/blob/main/assets/readme_imgs/menu.png?raw=true" alt="Menu Screenshot" width="400" height="400" /> 
</p>

## Installation

### Prerequisites
- Python 3.0 or newer
- Pygame

### Steps
1. Clone the repository to your local machine:
```
git clone https://github.com/RaghavVerma24/ChessAI
```

2. Install Pygame:
```
pip install pygame
```

3. Run the game:
```
python main.py
```

## Usage

### Game Modes
- **Single Player Mode**: Player vs AI, with different levels of difficulty.
- **Two Player Mode**: Player vs Player, where two players can play on the same computer.

### Controls
- **Mouse Click**: Select or move pieces.
- **r**: Reset the game.
- **q**: Quit to the main menu.

## AI

The AI algorithm used in this game is a minimax algorithm with alpha-beta pruning.

### Difficulty Levels

There are three levels of difficulty:
- **Easy**: AI looks 1 move ahead.
- **Medium**: AI looks 2 moves ahead.
- **Hard**: AI looks 3 moves ahead.

### Customization

You can customize the AI by changing the `max_depth` parameter in `ai.py`. A higher `max_depth` value will result in a stronger AI, but will also increase the processing time required for each move.
