function DrawPopUpBg(r, g, b, a)
    love.graphics.setColor(r, g, b, a)
    love.graphics.rectangle("fill", Window.centerX - 200, Window.centerY - 100, 400, 200, 10)
    love.graphics.setColor(1, 1, 1)
end

--  PopUp window for confirming actions
function DrawConfirmPopUp()
    DrawPopUpBg(0, 0, 0, 0.8)
    if ConfirmPopup.row > 0 then
        love.graphics.printf("Place tiles in row " .. ConfirmPopup.row .. "?",
            Window.centerX - 180,
            Window.centerY - 55,
            360, "center")
    else
        love.graphics.printf("Place tiles in Floor line?\n(It gives you minus score)",
            Window.centerX - 180,
            Window.centerY - 65,
            360, "center")
    end

    YesX, YesY, YesW, YesH = Window.centerX - 100, Window.centerY + 20, 80, 40
    NoX, NoY, NoW, NoH = Window.centerX + 20, Window.centerY + 20, 80, 40
    -- Draw buttons
    love.graphics.setColor(0.2, 0.8, 0.2)
    love.graphics.rectangle("fill", YesX, YesY, YesW, YesH, 6)
    love.graphics.setColor(1, 1, 1)
    love.graphics.printf("Yes", YesX, YesY + 7, YesW, "center")

    love.graphics.setColor(0.8, 0.2, 0.2)
    love.graphics.rectangle("fill", NoX, NoY, NoW, NoH, 6)
    love.graphics.setColor(1, 1, 1)
    love.graphics.printf("No", NoX, NoY + 7, NoW, "center")
end

--  PopUp window for confirming round ended
function DrawPopUp()
    if GameState.gameEnd then
        DrawPopUpBg(0, 0, 0, 0.8)
        love.graphics.printf(
            "Someone Finished a horizontal line.\nCalculating end game bonus",
            Window.centerX - 180, Window.centerY - 55, 360, "center")
    elseif #GameState.winners > 0 then
        DrawPopUpBg(0, 0, 0, 0.8)
        love.graphics.printf(
            EndGameChart,
            Window.centerX - 180, Window.centerY - 55, 360, "center")
    elseif GameState.roundEnd then
        DrawPopUpBg(0, 0, 0, 0.8)
        love.graphics.printf(
            "Calculating Scores...",
            Window.centerX - 180, Window.centerY - 35, 360, "center")
    end
end

function DrawHelpBtn()
    -- Help Button (circle with "?")
    love.graphics.setColor(HelpBtn.hover and { 0.7, 0.2, 0.2 } or { love.math.colorFromBytes(0, 121, 155) })
    love.graphics.rectangle("fill", HelpBtn.x, HelpBtn.y, HelpBtn.width, HelpBtn.height, 6)
    love.graphics.setColor(1, 1, 1)
    love.graphics.printf("Help (h)", HelpBtn.x, HelpBtn.y + 6, HelpBtn.width, "center")
    if HelpBtn.hover then
        love.graphics.setColor(0, 0, 0, 0.8)
        love.graphics.rectangle("fill", HelpBtn.x - 170, HelpBtn.y + 55, 555, 510, 8)
        love.graphics.setColor(1, 1, 1)
        love.graphics.printf(
            [[
                         Hotkeys in Menu
-----------------------------------------------------------------
2-4:                     Select no. of players
h:                        "H"elp panel

                         Hotkeys in Game
-----------------------------------------------------------------
up/down:          select factories
left/right:     select tiles
1-5:                     Select line to place tiles
6:                         Select floor to place tiles
h:                        "H"elp panel
b:                        "B"ack to main menu
y:                         Confirm Actions
n:                         Cancel Actions
]],
            HelpBtn.x - 150,
            HelpBtn.y + 75, 570)
    end
    -- Tooltip on hover
end

function DrawBackBtn()
    love.graphics.setColor(BackBtn.hover and { 0.7, 0.2, 0.2 } or { love.math.colorFromBytes(0, 121, 155) })
    love.graphics.rectangle("fill", BackBtn.x, BackBtn.y, BackBtn.width, BackBtn.height, 6)
    love.graphics.setColor(1, 1, 1)
    love.graphics.printf("Back (b)", BackBtn.x, BackBtn.y + 6, BackBtn.width, "center")
end
