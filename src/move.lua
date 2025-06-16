-- Helper: Highlight selected tiles in a factory
function ClickToSelectTile(mx, my)
    -- Clear all previous selection
    SelectedTiles = { color = nil, fIndex = 0 }
    for _, factory in ipairs(Factories) do
        for _, tile in ipairs(factory.tiles) do
            tile.isSelected = false
        end
    end

    for fIndex, factory in ipairs(Factories) do
        for _, tile in ipairs(factory.tiles) do
            if mx >= tile.x and mx <= tile.x + tile.width and
                my >= tile.y and my <= tile.y + tile.height then
                SelectedTiles.color = tile.image
                SelectedTiles.fIndex = fIndex

                for _, t in ipairs(factory.tiles) do
                    if t.image == tile.image then
                        t.isSelected = true
                    end
                end
                return
            end
        end
    end
end

function PressToNavigateTiles(direction)
    if SelectedTiles.fIndex <= 0 then return end

    local factory = Factories[SelectedTiles.fIndex]
    if not factory or #factory.tiles == 0 then return end

    -- Get all unique colors in this factory
    local uniqueColors = {}
    local colorOrder = {}

    for _, tile in ipairs(factory.tiles) do
        if not uniqueColors[tile.image] then
            uniqueColors[tile.image] = true
            table.insert(colorOrder, tile.image)
        end
    end

    -- Find current index
    local currentIndex = 1
    for i, color in ipairs(colorOrder) do
        if color == SelectedTiles.color then
            currentIndex = i
            break
        end
    end

    -- Move to next/previous color
    local newIndex
    if direction == "right" then
        newIndex = (currentIndex % #colorOrder) + 1
    elseif direction == "left" then
        newIndex = (currentIndex - 2) % #colorOrder + 1
    end

    -- Update selected color
    SelectedTiles.color = colorOrder[newIndex]

    -- Update selection visuals
    for _, tile in ipairs(factory.tiles) do
        tile.isSelected = (tile.image == SelectedTiles.color)
    end
end


-- Helper: Highlight selected tiles in a factory
function PressToNavigateFactories(direction)
    for _, factory in ipairs(Factories) do
        for _, tile in ipairs(factory.tiles) do
            tile.isSelected = false
        end
    end
    SelectedTiles.color = nil

    local attempts = 0
    repeat
        if direction == "up" then
            SelectedTiles.fIndex = (SelectedTiles.fIndex) % FactoryNum + 1
        elseif direction == "down" then
            SelectedTiles.fIndex = (SelectedTiles.fIndex - 2) % FactoryNum + 1
        end

        local factory = Factories[SelectedTiles.fIndex]

        if factory and factory.tiles and #factory.tiles > 0 then
            SelectedTiles.color = factory.tiles[1].image
            for _, t in ipairs(factory.tiles) do
                t.isSelected = (t.image == SelectedTiles.color)
            end
            break
        end

        attempts = attempts + 1
    until attempts >= FactoryNum
end

-- Helper: Get clicked row from player board
function ClickedRow(mx, my)
    if not SelectedTiles or not SelectedTiles.color then
        return -1
    end

    -- selecting floor line directly
    local floor = Players[Turn].floor[Players[Turn].floorCount + 1]
    if floor and mx >= floor.x and mx <= floor.x + Boards.floorOffset and
        my >= floor.y and my <= floor.y + Boards.floorOffset then
        return 0
    end

    for j = 1, 5 do
        local row = Players[Turn].line[j]
        local rowFull = true
        local colorMatch = true
        local rowColor = nil

        for k = 1, j do
            local tile = row[k].tile
            if tile == nil then
                rowFull = false
            else
                rowColor = rowColor or tile.image
                if tile.image ~= SelectedTiles.color then
                    colorMatch = false
                end
            end
        end

        local skipRow = rowFull or (rowColor and not colorMatch)

        -- Check if selected color already exists on the wall row
        if not skipRow then
            for k = 1, 5 do
                local wallTile = Players[Turn].wall[j][k].tile
                if wallTile and wallTile.image == SelectedTiles.color then
                    skipRow = true
                    break
                end
            end
        end

        -- Check if mouse is over the row
        if not skipRow then
            for k = 1, j do
                local slot = row[k]
                if mx >= slot.x and mx <= slot.x + Boards.tileOffset and
                    my >= slot.y and my <= slot.y + Boards.tileOffset then
                    return j
                end
            end
        end
    end
    return -1
end

function IsRowValid(rowIndex)
    local row = Players[Turn].line[rowIndex]
    local rowFull = true
    local colorMatch = true
    local rowColor = nil

    for k = 1, rowIndex do
        local tile = row[k].tile
        if tile == nil then
            rowFull = false
        else
            rowColor = rowColor or tile.image
            if tile.image ~= SelectedTiles.color then
                colorMatch = false
            end
        end
    end

    if rowFull or (rowColor and not colorMatch) then
        return false
    end

    -- Check for duplicate in wall
    for k = 1, 5 do
        local wallTile = Players[Turn].wall[rowIndex][k].tile
        if wallTile and wallTile.image == SelectedTiles.color then
            return false
        end
    end

    return true
end

-- Helper: Place tiles into row or floor
function HandleTilePlacement(row)
    local fIdx = SelectedTiles.fIndex
    local factory = Factories[fIdx]
    if (fIdx == 1) and
        FirstPlayerTile.x == FirstPlayerX and
        FirstPlayerTile.y == FirstPlayerY then
        Players[Turn].floorCount = Players[Turn].floorCount + 1
        local floor = Players[Turn].floor[Players[Turn].floorCount]
        FirstPlayerTile:moveTo(floor.x, floor.y)
    end

    for i = #factory.tiles, 1, -1 do
        local tile = factory.tiles[i]

        if tile.image == SelectedTiles.color then
            local placed = false

            -- Try line row
            for k = 1, row do
                if not Players[Turn].line[row][k].tile then
                    TileToBoard(tile, Players[Turn].line[row][k])
                    table.remove(factory.tiles, i)
                    placed = true
                    break
                end
            end

            -- Otherwise, floor
            if not placed then
                Players[Turn].floorCount = Players[Turn].floorCount + 1
                TileToBoard(tile, Players[Turn].floor[Players[Turn].floorCount])
                table.remove(factory.tiles, i)
            end
            -- Move non-matching tiles to center
        elseif SelectedTiles.fIndex ~= 1 then
            local x, y = RandomCenterPos()
            local newTile = Tile:new(tile.image, tile.x, tile.y)
            newTile:moveTo(x, y)
            table.insert(Factories[1].tiles, newTile)
            table.remove(factory.tiles, i)
        end
    end
end

function RandomCenterPos()
    local maxAttempts = 50
    for _ = 1, maxAttempts do
        local angle = math.random() * 2 * math.pi
        local radius = math.random(80, 145)
        local x = Window.centerX + math.cos(angle) * radius
        local y = Window.centerY + math.sin(angle) * radius

        local tooClose = false
        for _, pos in ipairs(Factories[1].tiles) do
            if math.dist(x, y, pos.x, pos.y) < 35 then
                tooClose = true
                break
            end
        end

        if not tooClose then
            return x, y
        end
    end
end

-- Helper: Place tile visually
function TileToBoard(tile, slot)
    local newTile = Tile:new(tile.image, tile.x, tile.y)
    newTile:moveTo(slot.x, slot.y)
    slot.tile = newTile
end

-- Helper: Move tiles from bag to factories
function DistributeTilesToFactories()
    for j = 2, FactoryNum do
        Factories[j].tiles = {}
        for i = 1, 4 do
            local newTile = table.remove(Bag)
            if not newTile then
                return -- or break/continue depending on your logic
            end
            -- Small local offset in tile-space
            local baseAngle = (i - 1) * math.rad(90)            -- 0, π/2, π, 3π/2
            local jitter = (math.random() - 0.5) * math.rad(30) -- ±15°
            local localAngle = baseAngle + jitter

            local finalX = 30 * math.cos(localAngle) +
                Window.centerX + 230 * math.cos(Factories[j].angle + 0.3) - 15
            local finalY = 30 * math.sin(localAngle) +
                Window.centerY + 230 * math.sin(Factories[j].angle + 0.3) - 15

            newTile:moveTo(finalX, finalY)
            table.insert(Factories[j].tiles, newTile)
        end
    end
    GameState.roundNum = GameState.roundNum + 1
end