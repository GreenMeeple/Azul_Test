# Azul_Test

This project is a digital adaptation of the board game [**Azul**](https://boardgamegeek.com/boardgame/230802/azul) by Michael Kiesling, created for educational and research purposes.

It includes:

- 🧠 **C++**: Core logic and game mechanics, with basic command line interface.
- 🐍 **Python**: Another option of basic logic, usable for AI training.
- 🎮 **Lua**: For UI interaction, including local and web version.
  - 🎮 **LÖVE2D**: A `.love` application that can be run by [Love2D executable](https://love2d.org/#download) (`love.exe`).
  - 🌐 **Web demo**: Built using [`love.js`](https://github.com/Davidobot/love.js), allowing you to play the game in a browser via WebAssembly.

## 🚀 Web Demo

You may try the game in [here](https://greenmeeple.github.io/Azul_Test/)

## 🏠 Local Run

### Web version

To run the web version locally:

1. Download the `WebDemo` folder and `index.html` or simply clone this repo

2. Put them into the same folder, for example:

    `Your_Folder`
    ├── WebDemo
    │   ├── theme
    │   ├── game.data
    │   ├── game.js
    │   ├── love.js
    │   ├── love.wasm
    │   └── love.worker.js
    └── index.html

3. Start a local server in the `Your_Folder` (where `index.html` locates). For example, you may use python:

    ```bash
    python -m http.server
    ```

4. Then open: `http://localhost:8000/`

### Run locally

1. Download [Love2D](https://love2d.org/#download).

2. Download the `Love2D` folder in this repo or simply clone this repo.

3. Double click `TilesBuilder.love` or drag it to the executable `love.exe`.

## 📘 Game Rules & Informations

- [Official Rulebook](https://www.ultraboardgames.com/azul/game-rules.php)

- [**2018 Spiel des Jahres Winner**](https://boardgamegeek.com/boardgamehonor/49380/2018-spiel-des-jahres-winner)

- Rank **2** in [Abstract games](https://boardgamegeek.com/abstracts/browse/boardgame?sort=rank&rankobjecttype=family&rankobjectid=4666&rank=2#2) (last update: 06/07/2025)
