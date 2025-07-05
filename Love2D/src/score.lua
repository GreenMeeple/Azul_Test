-- Move tiles from line to wall
function WallTiling(i, j)
    local lineTiles = Players[i].line[j]

    -- Only move when the whole line is occupied, return the column to move (1-5)
    for k = 1, j do
        local checkTile = lineTiles[k].tile
        if checkTile == nil then
            return 0
        end
    end

    local image = lineTiles[1].tile.image
    local wall = Players[i].wall[j]
    -- All tiles move to the box except the first one
    for k = 2, j do
        local newTile = lineTiles[k]
        newTile.tile:moveTo(BoxLoc.x + 15, BoxLoc.y + 15)
        table.insert(Box, newTile.tile)
        newTile.tile = nil
    end
    -- Find the place to move
    for k = 1, 5 do
        local wallColor = wall[k].color
        if image == wallColor then
            TileSound:play()
            local newTile = lineTiles[1]
            TileToBoard(newTile.tile, wall[k])
            newTile.tile = nil
            return k
        end
    end
    return 0
end

-- Score the newly moved tiles on the wall
function WallScore(i, row, col)
    CoinSound:play()
    local newTile = Players[i].wall
    local horizontal = 1
    local vertical = 1

    -- Check left
    for c = col - 1, 1, -1 do
        if newTile[row][c].tile then
            horizontal = horizontal + 1
        else
            break
        end
    end
    -- Check right
    for c = col + 1, 5 do
        if newTile[row][c].tile then
            horizontal = horizontal + 1
        else
            break
        end
    end

    -- Check up
    for r = row - 1, 1, -1 do
        if newTile[r][col].tile then
            vertical = vertical + 1
        else
            break
        end
    end
    -- Check down
    for r = row + 1, 5 do
        if newTile[r][col].tile then
            vertical = vertical + 1
        else
            break
        end
    end

    if horizontal == 1 then horizontal = 0 end
    if vertical == 1 then vertical = 0 end

    local points = horizontal + vertical
    if points == 0 then points = 1 end

    Players[i].score = Players[i].score + points
end

-- Deduct the points from the tiles on the floor
function FloorScore(i)
    local player = Players[i]
    if player.floorCount == 0 then
        return
    end

    TileSound:play()
    local penaltyScore = 0
    local penaltyTable = { 1, 2, 4, 6, 8 }
    local floor = player.floor

    -- After five tiles, each minus 3 points
    if player.floorCount > 5 then
        penaltyScore = (player.floorCount - 5) * 3 - 8
    else
        penaltyScore = penaltyTable[player.floorCount]
    end

    -- Player score cannot be negative
    if penaltyScore > player.score then
        player.score = 0
    else
        player.score = player.score - penaltyScore
    end

    -- Reset floor
    for j = 1, player.floorCount do
        -- Put it back to the box
        if floor[j].tile then
            floor[j].tile:moveTo(BoxLoc.x + 15, BoxLoc.y + 15)
            table.insert(Box, floor[j].tile)
            floor[j].tile = nil
        else
            -- if there's no tile, meaning that is the firstplayer tile
            FirstPlayerTile:moveTo(FirstPlayerX, FirstPlayerY)
            Turn = i
        end
    end
    player.floorCount = 0
end

function EndGameBonus(playerIndex)
    local player = Players[playerIndex]
    local wall = player.wall
    local bonus = 0

    -- 1. Full rows (+2 each)
    for i = 1, 5 do
        local full = true
        for j = 1, 5 do
            if not wall[i][j].tile then
                full = false
                break
            end
        end
        if full then
            bonus = bonus + 2
        end
    end

    -- 2. Full columns (+7 each)
    for j = 1, 5 do
        local full = true
        for i = 1, 5 do
            if not wall[i][j].tile then
                full = false
                break
            end
        end
        if full then
            bonus = bonus + 7
        end
    end

    -- 3. All 5 of one color (+10 per color)
    local colorCount = {}
    for i = 1, 5 do
        for j = 1, 5 do
            local tile = wall[i][j].tile
            if tile then
                local color = tile.image -- or tile.color, depending on your code
                colorCount[color] = (colorCount[color] or 0) + 1
            end
        end
    end
    for _, count in pairs(colorCount) do
        if count == 5 then
            bonus = bonus + 10
        end
    end

    player.score = player.score + bonus
    print("Player " .. playerIndex .. " gets end-game bonus: " .. bonus)
end

function ScoringRoutine()
    --  1. Check if the line is full
    for i = 1, PlayerNum do
        Wait(1.5)
        for j = 1, 5 do
            print("Resolving Player " .. i .. "'s Tiles")
            local k = WallTiling(i, j)
            if k > 0 then
                -- 2. If the line is full, move to wall and score immediately
                -- otherwise the scoring will be wrong
                print("Player " .. i .. " Resolving Row " .. j)
                WallScore(i, j, k)
                Wait(1.5)
            end
        end
        -- when all tiles moved to the wall, deduct the tiles on the floor
        print("Resolving Player " .. i .. "'s Floor")
        FloorScore(i)
    end
    -- Delay before checking game end
    GameState.roundEnd = false
    Wait(1)

    if IsGameEnd() then
        GameState.gameEnd = true
        for i = 1, PlayerNum do -- For each player
            Wait(1.5)
            EndGameBonus(i)
        end
        Wait(1)
        GameState.gameEnd = false
        RoundSound:play()
        print("Game End")
        GetWinner()
    else
        -- If bag doesnt have enough tiles, move all tiles from box to bag
        if #Bag < 36 then
            for i = 1, #Box do
                Box[i]:moveTo(BagLoc.x + 20, BagLoc.y + 20)
            end
            Wait(1.5)
            while #Box > 0 do
                local tile = table.remove(Box)
                table.insert(Bag, tile)
            end
        end
        RoundSound:play()
        DistributeTilesToFactories()
        print("Tile moved, new round starts")
    end
end
