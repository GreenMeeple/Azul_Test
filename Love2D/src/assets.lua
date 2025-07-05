function LoadAssets()
    local Board = love.graphics.newImage('demo_assets/playerboard.png')

    -- Store board dimensions
    local boardW = Board:getWidth() / 2
    local boardH = Board:getHeight() / 2

    Turn = 1

    -- All dimensions for the players' board
    Boards = {
        image       = Board,
        width       = boardW,
        height      = boardH,
        floorX      = 4,
        floorY      = 204,
        floorOffset = 38,
        wallX       = 192,
        wallY       = 7,
        lineOneX    = 143,
        lineOneY    = 8,
        tileSize    = 30,
        tileOffset  = 34.5,
    }

    -- Board locations for each player
    BoardDim = {
        { x = 30,                           y = 35 },
        { x = Window.x - Boards.width - 30, y = 35 },
        { x = Window.x - Boards.width - 30, y = Window.y - Boards.height - 50 },
        { x = 30,                           y = Window.y - Boards.height - 50 },
    }

    Box = {}
    local BoxImage = love.graphics.newImage('demo_assets/Azul.png')
    -- Box for used tiles, stored until the bag is emptied
    BoxLoc = {
        image  = BoxImage,
        width  = BoxImage:getWidth(),
        height = BoxImage:getHeight(),
        x      = 1100,
        y      = Window.y / 2 - 70,
    }

    Bag = {}
    local BagImage = love.graphics.newImage('demo_assets/bag.png')
    -- Bag
    BagLoc = {
        image  = BagImage,
        width  = BagImage:getWidth(),
        height = BagImage:getHeight(),
        x      = 250,
        y      = Window.y / 2 - 80,
    }
end

function DrawStartMenu()
    love.graphics.setColor(love.math.colorFromBytes(0, 121, 155))
    love.graphics.rectangle("fill", Window.centerX - 220, Window.centerY - 200, 440, 320, 10)
    love.graphics.setFont(Fonts.large)
    love.graphics.setColor(1, 1, 1)
    love.graphics.printf("Select Number of Players", 0, 235, Window.x, "center")

    for _, option in ipairs(PlayerOptions) do
        love.graphics.rectangle("line", option.x, option.y, option.w, option.h)
        love.graphics.printf(option.label, option.x, option.y + 10, option.w, "center")
    end
    ConfirmPopup = { active = false, row = nil }
    SelectedTiles = { color = nil, fIndex = 0 }
    DrawHelpBtn()
    love.graphics.setColor(1, 1, 1)
end

function DrawBtns()
    DrawBackBtn()
    DrawHelpBtn()
end
