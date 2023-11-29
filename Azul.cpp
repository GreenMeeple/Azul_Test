#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <unordered_map>
#include <algorithm> 

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
    int Point;  

    PlayerBoard() : trash(0), Point(0) {}
    SquarePart squarePart[5][5];
    StaircasePart staircasePart[5][5];

};

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

// Function to draw tiles for a round
void factoryDrawTiles(vector<FactoryDisplay>& factoryDisplays, unordered_map<Color, int>& bagTiles) {
    // Randomly fill each factory display with tiles
    for (auto& display : factoryDisplays) {
        display.tiles.clear(); // Clear previous tiles
        for (int i = 0; i < 4; ++i) {
            Color randomColor = static_cast<Color>(rand() % 5);
            if (bagTiles[randomColor] > 0) {
                display.tiles.push_back(randomColor);
                bagTiles[randomColor]--;
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
                cout << "X ";
            } else {
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
    factoryDrawTiles(factoryDisplays, bagTiles);

    // Initialize unused tiles count
    for (int i = 0; i < 5; ++i) {
        unusedTiles[static_cast<Color>(i)] = 0; // Each color starts with 20 tiles
    }

    displaybagTiles(bagTiles);
    displayAll(playerNumber, factoryDisplays, unusedTiles, playerBoards);

    return playerBoards;
}
// Function to draw tiles for a player's turn

void playRound(int playerNumber, vector<FactoryDisplay>& factoryDisplays, unordered_map<Color, int>& unusedTiles, vector<PlayerBoard>& playerBoards, int firstPlayer){
    // Simulate a player's turn
    int nextPlayer = 0;
    int unusedNum = 0;

    while(factoryDisplays.size() > 0 || unusedNum > 0){

        cout << "Player " << nextPlayer%playerNumber+firstPlayer+1 << "\'s turn:"<< endl;

        // Ask the player to choose a factory and Validate the input
        int factoryNumber;
        if(unusedNum > 0) {
            cout << "Enter the number of the factory you want to choose or type 0 for taking tiles from Unused Pile: ";
            cin >> factoryNumber;

            while (factoryNumber-1 < 0 || factoryNumber-1 > factoryDisplays.size()) {
                if(factoryNumber == 0){break;}

                cout << "Invalid row number";
                cin >> factoryNumber;

                if (cin.fail()) {
                    cin.clear();
                }
            }
        }
        else {
            cout << "Enter the number of the factory you want to choose: ";
            cin >> factoryNumber;

            while (factoryNumber-1 < 0 || factoryNumber-1 > factoryDisplays.size()) {
                cout << "Invalid row number";
                cin >> factoryNumber;
                
                if (cin.fail()) {
                    cin.clear();
                }
            }
        }
            
        // Ask the player to choose a color
        Color chosenColor;
        cout << "Enter the letter of the color you want to choose (R/Y/G/B/W): ";
        
        // Validate the input
        bool validColor = false;
        while (!validColor) {
            char colorChar;
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
            if(factoryNumber != 0){
                if (find(factoryDisplays[factoryNumber - 1].tiles.begin(), factoryDisplays[factoryNumber - 1].tiles.end(), chosenColor) != factoryDisplays[factoryNumber - 1].tiles.end()) {
                    validColor = true;
                } else {cout << "Invalid Color. Please choose a color in the corresponding factory.";}
            }
            else {
                if(unusedTiles[chosenColor] > 0){validColor = true;}
                else {cout << "Invalid Color. Please choose a color in the corresponding factory.";}
            }

            // Clear any input errors and discard invalid input
            if (cin.fail()) {
                cin.clear();
                validColor = false;
            }
                    
        }

        // Take all tiles of the chosen color from the selected factory
        int tileCount = 0;
        if(factoryNumber != 0){
            for (auto& display : factoryDisplays[factoryNumber - 1].tiles) {
                if (display == chosenColor) {
                    tileCount++;
                }
            }

            // Add the rest to unused tile
            for (auto& display : factoryDisplays[factoryNumber - 1].tiles) {
                if (display != chosenColor) {
                    unusedTiles[display]++;
                    unusedNum++;
                }
            }
            factoryDisplays.erase(factoryDisplays.begin() + factoryNumber-1);
        }

        // Take all tiles of the chosen color from Unused Tiles
        else {
            tileCount = unusedTiles[chosenColor];
            unusedTiles[chosenColor] = 0;
            unusedNum -= tileCount;
        }

        // Ask the player to choose a row for the staircase
        int rowNumber;
        cout << "Enter the number of the row you want to place the tiles (1-5): ";

        // Validate the input
        bool checkStaircase = true;
        while(checkStaircase){
            cin >> rowNumber;
            
            if(rowNumber < 1 || rowNumber > 5){
                cout << "Invalid row number. Please choose a number between 1 and 5: ";
            }
            else if(playerBoards[(nextPlayer+firstPlayer)%playerNumber].staircasePart[rowNumber-1][0].used == true && playerBoards[(nextPlayer+firstPlayer)%playerNumber].staircasePart[rowNumber-1][0].color != chosenColor){
                cout << "This Row has used for different color, please choose other row: ";
            }
            else if(playerBoards[(nextPlayer+firstPlayer)%playerNumber].staircasePart[rowNumber-1][rowNumber-1].used == true){
                cout << "This row is full, please choose other row: ";
            }
            else{checkStaircase = false;}

            if (cin.fail()) {
                cin.clear();
            }
        }

        //Calculate the spaces available to put the tiles
        int spacesAvailable = rowNumber;
        int startToAdd = 0;
        for(int i = 0; i < rowNumber; i++){
            if(playerBoards[(nextPlayer+firstPlayer)%playerNumber].staircasePart[rowNumber-1][i].used == true){
                spacesAvailable--;
                startToAdd++;
            }
        }
        if(tileCount < spacesAvailable){spacesAvailable = tileCount;}

        // Update the player board and remaining tiles
        for(int i = 0; i < spacesAvailable; i++){
            playerBoards[(nextPlayer+firstPlayer)%playerNumber].staircasePart[rowNumber-1][startToAdd+i].color = chosenColor;
            playerBoards[(nextPlayer+firstPlayer)%playerNumber].staircasePart[rowNumber-1][startToAdd+i].used = true;
            tileCount--;
        }

        // If the chosen row has fewer spaces than the tiles, move extra tiles to trash
        if(tileCount > 0){
            playerBoards[(nextPlayer+firstPlayer)%playerNumber].trash += tileCount;
            cout << "Number of Extra tiles moved to trash: " << tileCount << endl;
        }
        cout << "Updated Player Boards:" << endl;
        displayAll(playerNumber, factoryDisplays, unusedTiles, playerBoards);

        nextPlayer++;
    }

    CountPoint();
    bool a = CheckEnd(playerNumber, playerBoards);
    cout << a << endl;
}
void CountPoint(){};
bool CheckEnd(int playerNumber, vector<PlayerBoard>& playerBoards){
    bool gameEnd = true;

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
          // No row found where all are built
    }
    return gameEnd;
}

int main() {
    // Seed the random number generator
    srand(static_cast<unsigned>(time(0)));

    // Get the number of players
    int firstPlayer = 0;
    int playerNumber;
    cout << "Enter the number of the players (2-4): ";
    cin >> playerNumber;

    // Validate the input
    while (playerNumber < 2 || playerNumber > 4) {
        cout << "Invalid row number. Please choose a number between 2 and 4: ";
        cin >> playerNumber;
        
        if (cin.fail()) {
            cin.clear(); // Clear the error flag
        }
    }

    // Create 9 Factory Displays, remaining tiles, unused tiles
    vector<FactoryDisplay> factoryDisplays(playerNumber*2+1);
    unordered_map<Color, int> bagTiles;
    unordered_map<Color, int> unusedTiles;

    //Game Board Setup
    vector<PlayerBoard> playerBoards = gameSetUp(playerNumber, factoryDisplays, bagTiles, unusedTiles);

    //Play a Round
    playRound(playerNumber, factoryDisplays, unusedTiles, playerBoards, firstPlayer);

    return 0;
}
