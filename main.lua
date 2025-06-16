require 'src.assets'
require 'src.factories'
require 'src.players'
require 'src.score'
require 'src.state'
require 'src.textbox'
require 'src.tiles'
require 'src.move'

function StartCoroutine(fn)
    CoroutineRunner.current = coroutine.create(fn)
    CoroutineRunner.waitTime = 0
end

function ColorFromBytes(r, g, b, a)
    return { (r or 0)/255, (g or 0)/255, (b or 0)/255, (a or 255)/255 }
end

function math.dist(x1, y1, x2, y2)
    return ((x2 - x1) ^ 2 + (y2 - y1) ^ 2) ^ 0.5
end

function Wait(seconds)
    coroutine.yield(seconds)
end

function UpdateCoroutine(dt)
    if CoroutineRunner.waitTime > 0 then
        CoroutineRunner.waitTime = CoroutineRunner.waitTime - dt
    else
        local ok, wait = coroutine.resume(CoroutineRunner.current)
        if not ok or coroutine.status(CoroutineRunner.current) == "dead" then
            CoroutineRunner.current = nil
        elseif type(wait) == "number" then
            CoroutineRunner.waitTime = wait
        end
    end
end

CoroutineRunner = {
    current = nil,
    waitTime = 0
}

GameState = {
    gameStart = false,
    gameEnd = false,
    roundEnd = false,
    roundNum = 0,
    winners = {}
}

function love.load()
    -- Fonts
    Fonts = {
        large = love.graphics.newFont("assets/Algerian Regular.ttf", 24),
        small = love.graphics.newFont("assets/Algerian Regular.ttf", 15),
    }
    -- Sound Effects
    TileSound = love.audio.newSource("assets/ceramic.mp3", "stream")
    TileSound:setVolume(0.2)
    CoinSound = love.audio.newSource("assets/coin.mp3", "stream")
    RoundSound = love.audio.newSource("assets/jackpot.mp3", "stream")
    -- Tiles Image
    TileImages = {
        black = love.graphics.newImage("assets/black.png"),
        blue = love.graphics.newImage("assets/blue.png"),
        red = love.graphics.newImage("assets/red.png"),
        yellow = love.graphics.newImage("assets/yellow.png"),
        cyan = love.graphics.newImage("assets/cyan.png"),
        FirstPlayer = love.graphics.newImage('assets/firstplayer.png')
    }
    Background = love.graphics.newImage('assets/background.png')
    -- Window Size
    Window = {
        x = 1440,
        y = 810,
        centerX = 720,
        centerY = 405
    }
    -- Confirm Buttons
    ConfirmPopup = { active = false, row = nil }
    SelectedTiles = { color = nil, fIndex = 0 }
    HelpBtn = {
        x = Window.x - 450 - 130,
        y = 55,
        width = 130,
        height = 40,
        hover = false,
        press = false
    }
    BackBtn = {
        x = 450,
        y = 55,
        width = 130,
        height = 40,
        hover = false,
    }
    -- Min. Player = 2
    PlayerNum = 2
    PlayerOptions = {
        { label = "2 Players", value = 2, x = 620, y = 300, w = 200, h = 50 },
        { label = "3 Players", value = 3, x = 620, y = 370, w = 200, h = 50 },
        { label = "4 Players", value = 4, x = 620, y = 440, w = 200, h = 50 },
    }
end

function LoadGame()
    LoadAssets()
    LoadTiles()
    LoadPlayer()
    LoadFactory()
end

function love.update(dt)
    -- create waiting time between animations
    if CoroutineRunner.current then
        UpdateCoroutine(dt)
    end

    local mx, my = love.mouse.getPosition()
    -- Check HelpBtn
    HelpBtn.hover = mx >= HelpBtn.x and
        mx <= HelpBtn.x + HelpBtn.width and
        my >= HelpBtn.y and
        my <= HelpBtn.y + HelpBtn.height or HelpBtn.press

    if GameState.gameStart then
        FirstPlayerTile:update(dt)

        -- Check Return button
        BackBtn.hover = mx >= BackBtn.x and
            mx <= BackBtn.x + BackBtn.width and
            my >= BackBtn.y and
            my <= BackBtn.y + BackBtn.height

        -- Updates Tiles on Factories
        for _, factory in ipairs(Factories) do
            for _, tile in ipairs(factory.tiles) do
                tile:update(dt)
                tile.isHovered = false
            end
        end

        -- Check Tile Hovered on Factories
        CheckTilesHovered(mx, my)

        -- Updates Tiles in the box
        for _, tile in ipairs(Box) do
            tile:update(dt)
            tile.isHovered = false
        end

        -- Tiles on Player's Boards
        UpdatePlayer(dt, mx, my)

        -- Check if all tiles are taken
        if GameState.roundNum > 0 and IsRoundEnd() and CoroutineRunner.current == nil then
            GameState.roundEnd = true
            StartCoroutine(ScoringRoutine)
        end
    end
end

function love.keypressed(key)
    if key == "h" then
        HelpBtn.press = true
    else
        HelpBtn.press = false
    end

    if not GameState.gameStart then
        if key == "2" or key == "3" or key == "4" then
            local val = tonumber(key)
            if val and PlayerOptions[val - 1] then
                PlayerNum = PlayerOptions[val - 1].value
                FactoryNum = 2 * PlayerNum + 2
                LoadGame()
                GameState.gameStart = true
                RoundSound:play()
                DistributeTilesToFactories()
                return
            end
        end
        return
    end

    if ConfirmPopup.active then
        if key == "y" then
            HandleTilePlacement(ConfirmPopup.row)       -- Move tile from factory to line
            SelectedTiles = { color = nil, fIndex = 0 } -- Reset selected tile effects
            Turn = Turn % PlayerNum + 1                 -- Next turn
            ConfirmPopup.active = false                 -- Hide PopUp
            TileSound:play()
            return
        elseif key == "n" then
            ConfirmPopup.active = false -- Cancel: close popup
        else
            return
        end
        return
    end

    if key == "up" then
        PressToNavigateFactories("up")
        return
    elseif key == "down" then
        PressToNavigateFactories("down")
        return
    elseif key == "left" then
        PressToNavigateTiles("left")
        return
    elseif key == "right" then
        PressToNavigateTiles("right")
        return
    elseif key == "b" then
        GameState.gameStart = false
        return
    end

    local val = tonumber(key)
    if val and SelectedTiles.fIndex > 0 then
        if val >= 1 and val <= 5 then
            if IsRowValid(val) then
                ConfirmPopup.row = val
                ConfirmPopup.active = true
            else
                print("Invalid row selected")
            end
        elseif val == 6 then
            -- Treat 6 as selecting floor row
            ConfirmPopup.row = 0
            ConfirmPopup.active = true
        end
    end
end

function love.mousepressed(mx, my, mbutton)
    if mbutton ~= 1 then return end
    -- Load the game interface after player number is selected
    if not GameState.gameStart then
        for _, option in ipairs(PlayerOptions) do
            if mx >= option.x and mx <= option.x + option.w and
                my >= option.y and my <= option.y + option.h then
                PlayerNum = option.value
                FactoryNum = 2 * PlayerNum + 2
                LoadGame()
                GameState.gameStart = true
                print("Game Starts")
                RoundSound:play()
                DistributeTilesToFactories()
                return
            end
        end
        return -- Don't allow clicking behind popup
    end
    -- Back to select player numbers
    if BackBtn.hover then
        GameState.gameStart = false
        return
    end
    -- Confirm taking tiles
    if ConfirmPopup.active then
        if mx >= YesX and mx <= YesX + YesW and
            my >= YesY and my <= YesY + YesH then
            HandleTilePlacement(ConfirmPopup.row)       -- Move tile from factory to line
            SelectedTiles = { color = nil, fIndex = 0 } -- Reset selected tile effects
            Turn = Turn % PlayerNum + 1                 -- Next turn
            ConfirmPopup.active = false                 -- Hide PopUp
            TileSound:play()
            return
        elseif mx >= NoX and mx <= NoX + NoW and
            my >= NoY and my <= NoY + NoH then
            ConfirmPopup.active = false -- Cancel: close popup
            return
        else
            return -- Don't allow clicking behind popup
        end
    end

    -- Handle tile row selection
    if SelectedTiles.fIndex > 0 then
        local selectedRow = ClickedRow(mx, my)
        if selectedRow > -1 then
            ConfirmPopup.active = true     -- Show PopUp
            ConfirmPopup.row = selectedRow -- Saved selected row
            return
        end
    end
    -- Highlight selected tiles in a factory
    ClickToSelectTile(mx, my)
end

function love.draw()
    love.graphics.draw(Background, 0, 0)
    if GameState.gameStart == false then
        DrawStartMenu()
        return -- Don't draw the game yet
    else
        DrawFactory()
        DrawPlayer()
        for _, tile in ipairs(Box) do tile:draw(1, 1, 1, 1) end
        FirstPlayerTile:draw(1, 1, 1, 1)
        if GameState.roundNum > 0 then
            DrawPopUp()
        end

        if SelectedTiles.fIndex > 0 then DrawRows() end

        if ConfirmPopup.active then
            DrawConfirmPopUp()
        end
        DrawBtns()
        love.graphics.draw(BoxLoc.image, BoxLoc.x, BoxLoc.y, nil, 0.2)
    end
end
