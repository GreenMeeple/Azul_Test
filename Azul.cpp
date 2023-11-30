#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <unordered_map>
#include <algorithm> 
#include <stdexcept>
#include <limits>

using namespace std;

// Define colors for tiles
enum Color { R = 0, Y = 1, G = 2, B = 3, W = 4,};

// Define a struct for a Factory Display
struct FactoryDisplay { vector<Color> tiles; };

// Define a struct for a Player Board
struct PlayerBoard {
    struct SquarePart {
        Color color;
        bool built;
    };

    struct StaircasePart {
        Color color;
        bool used;
        bool available;
    };
    
    int trash;  
    int point;  

    PlayerBoard() : trash(0), point(0) {}
    SquarePart squarePart[5][5];
    StaircasePart staircasePart[5][5];

};

// Define a list for points deducted for trashed tiles
int pointsToDeduct[8] = {0, 1, 2, 4, 6, 8, 11, 14};

// Define a bag that contains all the tiles
unordered_map<Color, int> bagTiles;

// Function to initialize a player board
void initializePlayerBoard(PlayerBoard& playerBoard) {
    // Initialize square part with colors and set built to false
    for (int i = 0; i < 5; ++i) {
        for (int j = 0; j < 5; ++j) {
            playerBoard.squarePart[i][j].color = static_cast<Color>((j + i) % 5);
            playerBoard.squarePart[i][j].built = false;
        }
    }

    // Initialize staircase part with colors and set built to false
    for (int i = 0; i < 5; ++i) {
        for (int j = 0; j < 5; ++j) {
            playerBoard.staircasePart[i][j].used = false;
            if(j > i){ playerBoard.staircasePart[i][j].available = false;}
            else { playerBoard.staircasePart[i][j].available = true;}
        }
    }
}

// Function to refill bagTiles
void refillBagTiles(unordered_map<Color, int>& bagTiles, vector<PlayerBoard>& playerBoards, int playerNumber){
    cout << "Tiles in the bag are used up, refill the bag. " << endl;

    for (int i = 0; i < 5; ++i) {
        bagTiles[static_cast<Color>(i)] = 20; // Each color starts with 20 tiles
    }

    for(int i = 0; i < playerNumber; i++){
        for(int row = 0; row < 5; row++){
            for(int column = 0; column < 5; column++){
                if(playerBoards[i].squarePart[row][column].built == true){
                    bagTiles[playerBoards[i].squarePart[row][column].color] --;
                }
            }
        }
    }
}

// Function to draw tiles for a round
void factoryDrawTiles(vector<FactoryDisplay>& factoryDisplays, unordered_map<Color, int>& bagTiles, vector<PlayerBoard>& playerBoards, int playerNumber) {
    int tileNum = 0;
    for (const auto& entry : bagTiles) {
        tileNum += entry.second;
    }

    // Randomly fill each factory display with tiles
    for (auto& display : factoryDisplays) {
        display.tiles.clear(); // Clear previous tiles
        for (int i = 0; i < 4; ++i) {

            // refill bagTiles
            if(tileNum == 0){ refillBagTiles(bagTiles, playerBoards, playerNumber);}

            Color randomColor = static_cast<Color>(rand() % 5);
            if (bagTiles[randomColor] > 0) {
                display.tiles.push_back(randomColor);
                bagTiles[randomColor]--;
                tileNum--;
            } else {
                // If no more tiles of this color are available, choose another color
                i--;
            }
        }
    }
}

// Function to display tiles in each factory display
void displayFactoryDisplays(const vector<FactoryDisplay>& factoryDisplays) {
    for (int i = 0; i < factoryDisplays.size(); ++i) {
        cout << "Factory " << (i + 1) << ": ";
        for (const auto& color : factoryDisplays[i].tiles) {
            switch (color) {
                case R:
                    cout << "R ";
                    break;
                case Y:
                    cout << "Y ";
                    break;
                case G:
                    cout << "G ";
                    break;
                case B:
                    cout << "B ";
                    break;
                case W:
                    cout << "W ";
                    break;
            }
        }
        cout << endl;
    }
    cout << "--------------------" << endl;
}

// Function to display remaining tiles for each color
void displaybagTiles(const unordered_map<Color, int>& bagTiles) {
    cout << "Tiles in the Bag: ";
    for (const auto& entry : bagTiles) {
        switch (entry.first) {
            case R:
                cout << "RED: " << entry.second << " ";
                break;
            case Y:
                cout << "YELLOW: " << entry.second << " ";
                break;
            case G:
                cout << "GREEN: " << entry.second << " ";
                break;
            case B:
                cout << "BLUE: " << entry.second << " ";
                break;
            case W:
                cout << "WHITE: " << entry.second << " ";
                break;
        }
    }
    cout << endl;
    cout << "--------------------" << endl;
}

// Function to display remaining tiles for each color
void displayUnusedTiles(const unordered_map<Color, int>& unusedTiles) {
    cout << "Unused Tiles: ";
    for (const auto& entry : unusedTiles) {
        switch (entry.first) {
            case R:
                cout << "RED: " << entry.second << " ";
                break;
            case Y:
                cout << "YELLOW: " << entry.second << " ";
                break;
            case G:
                cout << "GREEN: " << entry.second << " ";
                break;
            case B:
                cout << "BLUE: " << entry.second << " ";
                break;
            case W:
                cout << "WHITE: " << entry.second << " ";
                break;
        }
    }
    cout << endl;
    cout << "--------------------" << endl;
}

// Function to display a player board
void displayPlayerBoard(const PlayerBoard& playerBoard) {
    for (int i = 0; i < 5; ++i) {
        
        // Display square part
        for (int j = 0; j < 5; ++j) {
            if (playerBoard.squarePart[i][j].built) {
                cout << "O ";
            } 
            else {
                switch (playerBoard.squarePart[i][j].color) {
                    case R:
                        cout << "R ";
                        break;
                    case Y:
                        cout << "Y ";
                        break;
                    case G:
                        cout << "G ";
                        break;
                    case B:
                        cout << "B ";
                        break;
                    case W:
                        cout << "W ";
                        break;
                }
            }
        }
        cout << "--- ";
        // Display staircase part
        for (int k = 0; k < 5; ++k) {
            if (!playerBoard.staircasePart[i][k].available) {
                cout << "X ";
            } 
            else if (!playerBoard.staircasePart[i][k].used) {
                cout << "O ";
            }
            else {
                switch (playerBoard.staircasePart[i][k].color) {
                    case R:
                        cout << "R ";
                        break;
                    case Y:
                        cout << "Y ";
                        break;
                    case G:
                        cout << "G ";
                        break;
                    case B:
                        cout << "B ";
                        break;
                    case W:
                        cout << "W ";
                        break;
                }
            }
        }
        cout << endl;
    }
    cout << "Trashed Tiles: "<< playerBoard.trash << endl;
    cout << "--------------------" << endl;
}

// Function to display a player board
void displayPlayerScore(int playerNumber, vector<PlayerBoard>& playerBoards) {
    for(int i = 0; i < playerNumber; i++){
        cout << "Player " << i+1 << ": "<< playerBoards[i].point << endl;
    }
}

// A warpper function for easying calling
void displayAll(int playerNumber, vector<FactoryDisplay>& factoryDisplays, unordered_map<Color, int>& unusedTiles, vector<PlayerBoard>& playerBoards){
    for (int i = 0; i < playerNumber; ++i) {
        cout << "Player " << (i + 1) << ":" << endl;
        displayPlayerBoard(playerBoards[i]);
        cout << endl;
    }
    displayFactoryDisplays(factoryDisplays);
    displayUnusedTiles(unusedTiles);
}

// Initialize The whole game
vector<PlayerBoard> gameSetUp(int playerNumber, vector<FactoryDisplay>& factoryDisplays, unordered_map<Color, int>& bagTiles, unordered_map<Color, int>& unusedTiles){
    // Initialize player boards
    vector<PlayerBoard> playerBoards(playerNumber);
    for (int i = 0; i < playerNumber; ++i) {
        initializePlayerBoard(playerBoards[i]);
    }

    // Initialize tiles in the bag
    for (int i = 0; i < 5; ++i) {
        bagTiles[static_cast<Color>(i)] = 20; // Each color starts with 20 tiles
    }

    // Draw tiles for the first round
    factoryDrawTiles(factoryDisplays, bagTiles, playerBoards, playerNumber);

    // Initialize unused tiles count
    for (int i = 0; i < 5; ++i) {
        unusedTiles[static_cast<Color>(i)] = 0; // Each color starts with 20 tiles
    }

    displaybagTiles(bagTiles);
    displayAll(playerNumber, factoryDisplays, unusedTiles, playerBoards);

    return playerBoards;
}

// Player Choose a factory to take tiles
int getFactoryNum(int unusedNum, vector<FactoryDisplay>& factoryDisplays){
    int factoryNum = 99;

    if(unusedNum > 0) {
        cout << "Enter the number of the factory you want to choose or type 0 for taking tiles from Unused Pile: ";
        while (true) {
            cin >> factoryNum;
            if(factoryNum >= 0 && factoryNum <= factoryDisplays.size()){break;}
            else {cout << "Invalid row number, please choose again: ";}
            if (cin.fail()) {cin.clear(); std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); }
        }
    }
    else {
        cout << "Enter the number of the factory you want to choose: ";
        while (true) {
            cin >> factoryNum;
            if(factoryNum >= 1 && factoryNum <= factoryDisplays.size()){break;}
            else {cout << "Invalid row number, please choose again: ";}
            if (cin.fail()) {cin.clear(); std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); }
        }
    }

    return factoryNum;
}

// Player choose a color to take
Color getColor(int unusedNum, int factoryNum, vector<FactoryDisplay>& factoryDisplays, unordered_map<Color, int>& unusedTiles){
    cout << "Enter the letter of the color you want to choose (R/Y/G/B/W): ";

    // Validate the input
    Color chosenColor;
    bool validColor = false;
    char colorChar;

    while (!validColor) {
        cin >> colorChar;
        // Convert the character to Color enum
        switch (colorChar) {
            case 'R':
                chosenColor = R;
                break;
            case 'Y':
                chosenColor = Y;
                break;
            case 'G':
                chosenColor = G;
                break;
            case 'B':
                chosenColor = B;
                break;
            case 'W':
                chosenColor = W;
                break;
        }

        // if player choose factory, check if that color exist in the factory
        if(factoryNum != 0){
            if (find(factoryDisplays[factoryNum - 1].tiles.begin(), factoryDisplays[factoryNum - 1].tiles.end(), chosenColor) != factoryDisplays[factoryNum - 1].tiles.end()) {
                validColor = true;
            } else {cout << "Invalid Color. Please choose a color in the corresponding factory.";}
        }

        // check if the color exist in Unused tile
        else {
            if(unusedTiles[chosenColor] > 0){validColor = true;}
            else {cout << "Invalid Color. Please choose a color in the corresponding factory.";}
        }

        // Clear any input errors and discard invalid input
        if (cin.fail()) { validColor = false; cin.clear(); std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); }      
    }

    return chosenColor;
}

// Get the number of tiles player takes
int getTiles(int unusedNum, int factoryNum, Color chosenColor, vector<FactoryDisplay>& factoryDisplays, unordered_map<Color, int>& unusedTiles){
    int tileCount = 0;
    
    // Take all tiles of the chosen color from the selected factory
    if(factoryNum != 0){
        for (auto& display : factoryDisplays[factoryNum - 1].tiles) {
            if (display == chosenColor) {
                tileCount++;
            }
        }

        // Add the rest to unused tile
        for (auto& display : factoryDisplays[factoryNum - 1].tiles) {
            if (display != chosenColor) {
                unusedTiles[display]++;
                unusedNum++;
            }
        }
        factoryDisplays.erase(factoryDisplays.begin() + factoryNum-1);
    }

    // Take all tiles of the chosen color from Unused Tiles
    else {
        tileCount = unusedTiles[chosenColor];
        unusedTiles[chosenColor] = 0;
        unusedNum -= tileCount;
    }
    return tileCount;
}

// Get the Row number of the staircase to put
bool isValidRow(const PlayerBoard& playerBoard, int rowNum, Color chosenColor) {
    return rowNum >= 1 && rowNum <= 5 &&
           playerBoard.staircasePart[rowNum - 1][0].used == false &&
           playerBoard.staircasePart[rowNum - 1][rowNum - 1].used == false &&
           std::none_of(std::begin(playerBoard.squarePart[rowNum - 1]),
                        std::end(playerBoard.squarePart[rowNum - 1]),
                        [chosenColor](const PlayerBoard::SquarePart& square) {
                            return square.built && square.color == chosenColor;
                        });
}

// Put the tiles to the staircase
void takeTiles(int RowNum, int tileCount, int nextPlayer, int playerNumber, Color chosenColor, vector<PlayerBoard>& playerBoards){
    // Trash all selected tiles
    if(RowNum == 0){
        playerBoards[nextPlayer%playerNumber].trash += tileCount;
        cout << "Number of tiles moved to trash: " << tileCount << endl;
    }

    //Calculate the spaces available to put the tiles
    else {
        int spacesAvailable = RowNum;
        int startToAdd = 0;
        for(int i = 0; i < RowNum; i++){
            if(playerBoards[nextPlayer%playerNumber].staircasePart[RowNum-1][i].used == true){
                spacesAvailable--;
                startToAdd++;
            }
        }
        if(tileCount < spacesAvailable){spacesAvailable = tileCount;}

        // Update the player board and remaining tiles
        for(int i = 0; i < spacesAvailable; i++){
            playerBoards[nextPlayer%playerNumber].staircasePart[RowNum-1][startToAdd+i].color = chosenColor;
            playerBoards[nextPlayer%playerNumber].staircasePart[RowNum-1][startToAdd+i].used = true;
            tileCount--;
        }

        // If the chosen row has fewer spaces than the tiles, move extra tiles to trash
        if(tileCount > 0){
            playerBoards[nextPlayer%playerNumber].trash += tileCount;
            cout << "Number of Extra tiles moved to trash: " << tileCount << endl;
        }
    }
}

// Update the points of a round
void countPoints(int row, int col, PlayerBoard& playerBoard){
    int maxWidth = 1;
    int width = 1;

    // Check to the left of the current position
    for (int c = col - 1; c >= 0 && playerBoard.squarePart[row][c].built; --c) {++width;}

    // Check to the right of the current position
    for (int c = col + 1; c < 5 && playerBoard.squarePart[row][c].built; ++c) {++width;}

    maxWidth = std::max(maxWidth, width);

    // Function to find the longest vertical line
    int maxLength = 1;
    int length = 1;

    // Check above the current position
    for (int r = row - 1; r >= 0 && playerBoard.squarePart[r][col].built; --r) {++length;}

    // Check below the current position
    for (int r = row + 1; r < 5 && playerBoard.squarePart[r][col].built; ++r) {++length;}

    maxLength = std::max(maxLength, length);

    // Add the point
    playerBoard.point += maxLength + maxWidth;

    // Deduct points from trash then reset trash
    if (playerBoard.trash > 7) { playerBoard.trash = 7; }
    playerBoard.point -= pointsToDeduct[playerBoard.trash];
    playerBoard.trash = 0;

    // Player will not get negative number of points
    if (playerBoard.point < 0) { playerBoard.point = 0; }
}

// Move Tile from staircase to square then count points
void moveTile(int playerNumber, vector<PlayerBoard>& playerBoards){
    // check if the row is full
    for(int i = 0; i < playerNumber; i++){
        for(int row = 0; row < 5; row++){
            if(playerBoards[i].staircasePart[row][row].used == true){
                Color color = playerBoards[i].staircasePart[row][row].color;
                for(int column = 0; column < 5; column++){
                    playerBoards[i].staircasePart[row][column].used = false;                    
                    if(playerBoards[i].squarePart[row][column].color == color){
                        playerBoards[i].squarePart[row][column].built = true;
                        countPoints(row, column, playerBoards[i]);
                    }
                }
            }
        }
    }

    cout << "All players' Tiles has moved, the current scores are: " << endl;
    displayPlayerScore(playerNumber, playerBoards);
    cout << "---------------" << endl;
    cout << "Starting a new Round." << endl;
    cout << "---------------" << endl;

    for (int i = 0; i < playerNumber; ++i) {
        cout << "Player " << (i + 1) << ":" << endl;
        displayPlayerBoard(playerBoards[i]);
        cout << endl;
    }
};

// Function to check when the game is finished
bool CheckEnd(int playerNumber, vector<PlayerBoard>& playerBoards){
    bool gameEnd = false;

    // if any player finish one row in the squarepart, the game ends
    for(int i = 0; i < playerNumber; i++){
        for (int row = 0; row < 5; ++row) {
            for (int col = 0; col < 5; ++col) {
                gameEnd = true;
                if (!playerBoards[i].squarePart[row][col].built) {
                    gameEnd = false;
                    break;  // No need to check further if one is not built
                }
            }
        }
    }
    return gameEnd;
}

// Function to draw tiles for a player's turn
void playRound(int playerNumber, vector<FactoryDisplay>& factoryDisplays, unordered_map<Color, int>& unusedTiles, vector<PlayerBoard>& playerBoards, int firstPlayer){
    // Simulate a player's turn
    int nextPlayer = firstPlayer;
    int unusedNum = 0;

    while(factoryDisplays.size() > 0 || unusedNum > 0){

        cout << "Player " << nextPlayer%playerNumber+1 << "\'s turn:"<< endl;

        // Ask the player to choose a factory and Validate the input
        int factoryNum = getFactoryNum(unusedNum, factoryDisplays);

        // Get the Row number of the staircase to put
        int rowNum;
        Color chosenColor;
        while (true) {
            std::cout << "Enter the number of the row you want to choose (1-5), or 0 to exit: ";
            std::cin >> rowNum;

            if (rowNum == 0) {
                break;
            }

            // Ask the player to choose a color
            chosenColor = getColor(unusedNum, factoryNum, factoryDisplays, unusedTiles);

            if (isValidRow(playerBoards[nextPlayer % playerNumber], rowNum, chosenColor)) {
                std::cout << "Valid input. Processing..." << std::endl;
                // Your processing logic here
                // Update the playerBoards or perform other actions based on the valid input
                ++nextPlayer;
            } else {
                std::cout << "Invalid input. Please choose again." << std::endl;
            }

            if (std::cin.fail()) {
                std::cin.clear();
                std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            }
        }   

        // Get the number of tiles of the color in the factory
        int tileCount = getTiles(unusedNum, factoryNum, chosenColor, factoryDisplays, unusedTiles);     

        takeTiles(rowNum, tileCount, nextPlayer, playerNumber, chosenColor, playerBoards);
        
        cout << "Updated Player Boards:" << endl;
        displayAll(playerNumber, factoryDisplays, unusedTiles, playerBoards);

        nextPlayer++;
    }

    cout << "No more tiles on the table, now move the tile from right to left and count the points" << endl;
    cout << "---------------" << endl;

    moveTile(playerNumber, playerBoards);
    bool finished = CheckEnd(playerNumber, playerBoards);
    if(finished){ cout << "The game is ended." << endl; }
    else { 
        factoryDrawTiles(factoryDisplays, bagTiles, playerBoards, playerNumber);
        playRound(playerNumber, factoryDisplays, unusedTiles, playerBoards, firstPlayer); 
    }
}

int main() {
    // Seed the random number generator
    srand(static_cast<unsigned>(time(0)));

    cout << "Welcome to Azul. For the rule of this boardgame, you may visit" << endl;
    cout << "https://www.ultraboardgames.com/azul/game-rules.php" << endl;

    // Get the number of players
    int firstPlayer = 0;
    int playerNumber;
    cout << "Enter the number of the players (2-4): ";
    cin >> playerNumber;

    // Validate the input
    while (playerNumber < 2 || playerNumber > 4) {
        cout << "Invalid row number. Please choose a number between 2 and 4: ";
        cin >> playerNumber;
        if (cin.fail()) {cin.clear();}
    }

    // Create Factory Displays and unused tiles
    vector<FactoryDisplay> factoryDisplays(playerNumber*2+1);
    unordered_map<Color, int> unusedTiles;

    //Game Board Setup
    vector<PlayerBoard> playerBoards = gameSetUp(playerNumber, factoryDisplays, bagTiles, unusedTiles);

    //Play a Round
    playRound(playerNumber, factoryDisplays, unusedTiles, playerBoards, firstPlayer);

    return 0;
}
