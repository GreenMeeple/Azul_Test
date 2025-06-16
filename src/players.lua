function LoadPlayer()
    local wallLayout = {
        { "blue",   "yellow", "red",    "black",  "cyan" },
        { "cyan",   "blue",   "yellow", "red",    "black" },
        { "black",  "cyan",   "blue",   "yellow", "red" },
        { "red",    "black",  "cyan",   "blue",   "yellow" },
        { "yellow", "red",    "black",  "cyan",   "blue" },
    }

    Players = {}
    -- Create player board objects
    for i = 1, PlayerNum do
        Players[i] = {}
        Players[i].x = BoardDim[i].x
        Players[i].y = BoardDim[i].y
        Players[i].name = "Player " .. i
        Players[i].score = 0
        Players[i].floor = {}
        Players[i].floorCount = 0
        Players[i].wall = {}
        Players[i].line = {}
        -- floor row
        for j = 1, 37 do
            local row = math.floor((j - 1) / 7)
            local col = (j - 1) % 7

            Players[i].floor[j] = {
                x = Players[i].x + Boards.floorX + col * Boards.floorOffset,
                y = Players[i].y + Boards.floorY + row * Boards.floorOffset,
                tile = nil
            }
        end

        for j = 1, 5 do
            Players[i].wall[j] = {}
            Players[i].line[j] = {}
            -- Scoring Wall
            for k = 1, 5 do
                Players[i].wall[j][k] = {
                    x = Players[i].x + Boards.wallX + (k - 1) * Boards.tileOffset,
                    y = Players[i].y + Boards.wallY + (j - 1) * Boards.tileOffset,
                    tile = nil,
                    color = TileImages[wallLayout[j][k]]
                }
            end
            -- Pattern lines
            for l = 1, j do
                Players[i].line[j][l] = {
                    x = Players[i].x + Boards.lineOneX - (l - 1) * Boards.tileOffset,
                    y = Players[i].y + Boards.lineOneY + (j - 1) * Boards.tileOffset,
                    tile = nil
                }
            end
        end
    end
end

function DrawPlayer()
    -- Draw each player board
    for _, player in ipairs(Players) do
        love.graphics.draw(Boards.image, player.x, player.y, nil, 0.5)

        -- Optional: draw player name/score
        love.graphics.setFont(Fonts.large)
        love.graphics.setColor(love.math.colorFromBytes(0, 121, 155))
        love.graphics.print(player.name, player.x + 260, player.y - 25, nil)
        love.graphics.printf(player.score, player.x + 20, player.y + 27, 66, "center")
        love.graphics.setFont(Fonts.small)
        love.graphics.print("Score", player.x + 3, player.y + 60, nil)
        love.graphics.setFont(Fonts.large)
        love.graphics.setColor(1, 1, 1)
    end

    for i = 1, PlayerNum do
        for j = 1, 37 do
            local tile = Players[i].floor[j].tile
            if tile then tile:draw(1, 1, 1, 1) end
        end

        for j = 1, 5 do
            -- Scoring Wall
            for k = 1, 5 do
                local tile = Players[i].wall[j][k].tile
                if tile then tile:draw(0, 0, 0, 0.5) end
            end
            -- Pattern lines
            for l = 1, j do
                local tile = Players[i].line[j][l].tile
                if tile then tile:draw(1, 1, 1, 1) end
            end
        end
    end
end

function DrawRows()
    love.graphics.setLineWidth(3)
    love.graphics.setColor(1, 0, 0) -- red outline

    -- Draw floor highlight
    local floorRow = math.floor(Players[Turn].floorCount / 7)
    local floorCol = Players[Turn].floorCount - math.floor(Players[Turn].floorCount / 7) * 7

    love.graphics.rectangle("line",
        Players[Turn].x + Boards.floorX + floorCol * Boards.floorOffset,
        Players[Turn].y + Boards.floorY + floorRow * Boards.floorOffset,
        33, 33)

    -- Draw pattern line highlights
    for j = 1, 5 do
        local row = Players[Turn].line[j]
        local rowColor = nil
        local hasConflict = false

        -- Check if the row contains any tile of a different color
        for k = 1, j do
            local tile = row[k].tile
            if tile then
                rowColor = rowColor or tile.image
                if tile.image ~= SelectedTiles.color then
                    hasConflict = true
                    break
                end
            end
        end

        for k = 1, 5 do
            local wallTile = Players[Turn].wall[j][k].tile
            if wallTile and wallTile.image == SelectedTiles.color then
                hasConflict = true
                break
            end
        end

        if not hasConflict then
            for k = 1, j do
                if not row[k].tile then
                    love.graphics.rectangle("line",
                        row[k].x,
                        row[k].y,
                        Boards.tileSize,
                        Boards.tileSize)
                end
            end
        end
    end

    love.graphics.setColor(1, 1, 1)
    love.graphics.setLineWidth(1)
end

function UpdatePlayer(dt, mx, my)
    for i = 1, PlayerNum do
        -- Penalty Floor
        for j = 1, 37 do
            local tile = Players[i].floor[j].tile
            if tile then
                tile:update(dt)
                tile.isHovered = false
            end
        end

        for j = 1, 5 do
            -- Scoring Wall
            for k = 1, 5 do
                local tile = Players[i].wall[j][k].tile
                if tile then
                    tile:update(dt)
                    tile.isHovered = false
                end
            end
            -- Pattern lines
            for l = 1, j do
                local tile = Players[i].line[j][l].tile
                if tile then
                    tile:update(dt)
                    tile.isHovered = false
                end
            end
        end
    end
end
