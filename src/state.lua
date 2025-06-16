function IsRoundEnd()
    for _, factory in ipairs(Factories) do
        if #factory.tiles > 0 then
            return false
        end
    end
    return true
end

function IsGameEnd()
    for i = 1, PlayerNum do -- For each player
        for j = 1, 5 do     -- For each row
            if IsRowFull(i, j) then
                return true
            end
        end
    end
    return false
end

function IsRowFull(playerIndex, rowIndex)
    local wall = Players[playerIndex].wall[rowIndex]
    for col = 1, 5 do
        if wall[col].tile == nil then
            return false
        end
    end
    return true
end

function GetWinner()
    local maxScore = -math.huge
    EndGameChart = "Game Ends!\n"

    for i = 1, PlayerNum do
        local score = Players[i].score
        EndGameChart = EndGameChart .. "Player " .. i .. "--" .. score .. "\n"

        if score > maxScore then
            maxScore = score
            GameState.winners = { i }          -- new highest score, reset winners list
        elseif score == maxScore then
            table.insert(GameState.winners, i) -- tie
        end
    end

    EndGameChart = EndGameChart .. "Player "

    print("Max Score:", maxScore)
    for _, winner in ipairs(GameState.winners) do
        EndGameChart = EndGameChart .. winner
        print("Winner: Player " .. winner)
    end

    EndGameChart = EndGameChart .. " win!"
end
