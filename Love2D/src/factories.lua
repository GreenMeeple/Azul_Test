function LoadFactory()
    local Factory = love.graphics.newImage('demo_assets/factory.png')
    Factories = {}
    Factories.image = Factory
    -- Center part
    table.insert(Factories, { tiles = {} })

    -- In draw circle: store positions
    for i = 2, FactoryNum do
        local angle = 2 * math.pi * (i - 2) / (FactoryNum - 1)
        local fx = Window.centerX + 150 * math.cos(angle)
        local fy = Window.centerY + 150 * math.sin(angle)
        table.insert(Factories, {
            x = fx,
            y = fy,
            angle = angle,
            tiles = {} -- Will be filled later
        })
    end
    -- Center board (namely 10th factory)
end

function DrawFactory() -- Draw factories in a circle
    love.graphics.draw(BagLoc.image, BagLoc.x, BagLoc.y)

    for i = 2, FactoryNum do
        love.graphics.draw(Factories.image, Factories[i].x, Factories[i].y, Factories[i].angle, 0.55)
    end

    -- Draw Tiles
    for _, factory in ipairs(Factories) do
        for _, tile in ipairs(factory.tiles) do tile:draw(1, 1, 1, 1) end
    end
end

function CheckTilesHovered(mx, my)
    for _, factory in ipairs(Factories) do
        local colorHovered = nil

        for _, tile in ipairs(factory.tiles) do
            if mx >= tile.x and mx <= tile.x + tile.width and
                my >= tile.y and my <= tile.y + tile.height then
                colorHovered = tile.image -- assuming image acts as tile type
                break
            end
        end

        if colorHovered then
            for _, tile in ipairs(factory.tiles) do
                if tile.image == colorHovered then
                    tile.isHovered = true
                end
            end
        end
    end
end
