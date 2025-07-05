Tile = {}
Tile.__index = Tile

function Tile:new(image, x, y)
    local self = setmetatable({}, Tile)
    self.image = image
    self.x = x
    self.y = y
    self.width = image:getWidth() * 0.7
    self.height = image:getHeight() * 0.7
    self.speed = 100
    self.moving = false
    self.distance = 0
    self.isHovered = false
    self.isSelected = false
    return self
end

function Tile:moveTo(newX, newY)
    local distance = math.dist(self.x, self.y, newX, newY)

    if distance > 0 then
        self.startX = self.x
        self.startY = self.y
        self.targetX = newX
        self.targetY = newY
        self.distance = distance
        self.elapsed = 0
        self.duration = distance / self.speed
        self.moving = true
    end
end

function Tile:update(dt)
    if self.moving then
        self.elapsed = (self.elapsed + dt) * 1.05
        local t = math.min(self.elapsed / self.duration, 1)
        local ease = t * t * (3 - 2 * t) -- ease in/out

        self.x = self.startX + (self.targetX - self.startX) * ease
        self.y = self.startY + (self.targetY - self.startY) * ease

        if t >= 1 then
            self.x = self.targetX
            self.y = self.targetY
            self.moving = false
        end
    end
end

function Tile:draw(r, g, b, a)
    local padding = 2
    love.graphics.setLineWidth(3)
    if self.isSelected then
        love.graphics.setColor(1, 0, 0)
    elseif self.isHovered then
        love.graphics.setColor(0, 1, 1)
    else
        love.graphics.setColor(0, 0, 0, 0)
    end
    love.graphics.rectangle("line",
        self.x - padding,
        self.y - padding,
        self.width + padding * 2,
        self.height + padding * 2,
        6, 6 -- optional rounded corners
    )
    love.graphics.setLineWidth(1)
    love.graphics.setColor(r, g, b, a)
    love.graphics.draw(self.image, self.x, self.y, nil, 0.7)
    love.graphics.setColor(1, 1, 1)
end

function LoadTiles()
    local FirstPlayer = love.graphics.newImage('demo_assets/firstplayer.png')
    FirstPlayerX = Window.centerX - FirstPlayer:getWidth() / 2
    FirstPlayerY = Window.centerY - FirstPlayer:getHeight() / 2
    FirstPlayerTile = Tile:new(FirstPlayer, FirstPlayerX, FirstPlayerY)

    local tileTypes = { "blue", "yellow", "red", "black", "cyan" }
    for _, color in ipairs(tileTypes) do
        for i = 1, 20 do -- e.g. 20 tiles of each color
            local newTile = Tile:new(TileImages[color], BagLoc.x + 20, BagLoc.y + 20)
            table.insert(Bag, newTile)
        end
    end

    -- Shuffle bag
    for i = #Bag, 2, -1 do
        local j = love.math.random(i)
        Bag[i], Bag[j] = Bag[j], Bag[i]
    end
end
