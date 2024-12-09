import streamlit as st
import module
import streamlit.components.v1 as components
from module import js_test
from module import weather

code = """
<!DOCTYPE html>

<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta charset="utf-8" />
    <title>Flappy Bird</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi" crossorigin="anonymous">
</head>
<body>
<h1 class="text-center">Flappy Bird</h1>
<div style="position:absolute; left:50%;margin-left:-450px;">
<canvas id="canvas" height=700, width=900></canvas>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-OERcA2EqjJCMA+/3y+gxIOqMEjwtxJY7qPCqsdltbNJuaOe923+mo//f6V8Qbsw3" crossorigin="anonymous"></script>
<script>
var width = 900, height = 700;
var speed = 10;
var Pressed = false;
var jump = false;
var GameStart = false;
var environ=450;
var SpacePressed = false;
var Obstacles = new Array();

var Vy = 0;
var Py = 350;
var Px = 200;
var Ay = 0.35;
var Cu = 0;
var Cd = height;

var canvas = document.getElementById("canvas");
canvas.style.border='1px solid black'
var ctx = canvas.getContext("2d");

class ScoreManage {
    constructor()
    {
        this.score = 0;
    }
    scoreup()
    {
        this.score++;
    }
}

class Obstacle 
{
    constructor()
    {
        this.pass = parseInt(Math.random(1)*500 + 100);
        this.X = width;
        this.scored = false;
    }
    update()
    {
        this.X -= 2;
    }
}

var SM = new ScoreManage();

var interval = setInterval(function()
{
    game();
}, speed)

var interval2 = setInterval(function()
{
    CreateObs();
}, 2500);

function drawCloud(X, Y, S)
{
    X = X % width;
    X = width - X;
    ctx.fillStyle = "white";
    ctx.fillRect(X-10*S, Y-20*S, 40*S, 30*S);
    ctx.fillRect(X-20*S, Y, 50*S, 34*S);
    ctx.fillRect(X+14*S, Y+6*S, 44*S, 40*S);
}

function drawBird()
{
    ctx.translate(Px, Py);
    ctx.rotate((Math.PI/180)*Vy*2);

    ctx.fillStyle = "yellow";
    ctx.fillRect(-20, -15, 40, 35);
    ctx.fillStyle = "orange";
    ctx.fillRect(8, 2, 20, 9);
    ctx.fillStyle = "black";
    ctx.fillRect(5, -8, 5, 5);

    ctx.translate(-20, -2);
    ctx.rotate((Math.PI/180)*25);
    ctx.fillStyle = "yellow";
    ctx.fillRect(-12, -5, 20, 17);

    ctx.rotate((Math.PI/180)*-25);
    ctx.translate(20, 2);

    ctx.rotate(-(Math.PI/180)*Vy*2);
    ctx.translate(-Px, -Py);
}

function game()
{
    ctx.fillStyle = "skyblue";
    ctx.fillRect(0, 0, width, height);

    drawCloud(environ+275, 60, 1);
    drawCloud(environ-200, 200, 1.2);
    drawCloud(environ+420, 180, 1.1);
    drawCloud(environ+80, 90, 1.5);
    drawCloud(environ-400, 125, 1.4);
    drawCloud(environ-120, 70, 1.15);

    environ += 1;

    if (GameStart)
    {
        Vy += Ay;
        Py += Vy;

        drawBird();

        if (Py >= height || Py <= 0 || !(Cu <= Py && Py <= Cd))
        {
            clearInterval(interval);
            clearInterval(interval2);
            var promptstr = "" + SM.score + '점';
            alert(promptstr)

            speed = 10;
            Pressed = false;
            jump = false;
            GameStart = false;
            environ=450;
            SpacePressed = false;
            Obstacles = new Array();

            Vy = 0;
            Py = 350;
            Px = 200;
            Ay = 0.35;
            Cu = 0;
            Cd = height;

            SM = new ScoreManage();

            interval = setInterval(function()
            {
                game();
            }, speed)

            interval2 = setInterval(function()
            {
                CreateObs();
            }, 2000);
        }

        var clear = true;

        for (var i = 0; i < Obstacles.length; i++)
        {
            ob = Obstacles[i];
            x = ob.X;
            pass = ob.pass;

            if (Px-100 <=x && x<= Px)
            {
                Cu = pass - 80 + 18;
                Cd = pass + 80 - 10;
                clear = false;
            }
            else if (x <Px-100 && !ob.scored)
            {
                SM.scoreup()
                ob.scored=true;
            }

            ctx.fillStyle = "green";
            ctx.fillRect(x, 0, 100, pass - 80);
            ctx.fillRect(x, pass + 80, 100, height - pass - 80);
            ob.update();
        }

        if (clear)
        {
            Cu = 0;
            Cd = height;
        }

        if (Obstacles.length > 4)
        {
            Obstacles.shift(-1);
        }

        ctx.font = "50px Arial";
        ctx.fillStyle="black";
        ctx.fillText(SM.score, 450, 80);
    }

    if (jump)
    {
        Vy = -7;
        jump = false;
    }
}

function CreateObs()
{
    if (GameStart)
    {
        var ob = new Obstacle();
        Obstacles.push(ob);
    }
}

window.addEventListener("keydown", function(e){
    if(!Pressed)
    {
        jump = true;
        Pressed = true;
    }
    if(!GameStart)
    {
        GameStart=true;
    }
});

window.addEventListener("mousedown", function(e){
    if(!Pressed)
    {
        jump = true;
        Pressed = true;
    }
    if(!GameStart)
    {
        GameStart=true;
    }
});

window.addEventListener("keyup", function(e){
    Pressed = false;
});

window.addEventListener("mouseup", function(e){
    Pressed = false;
});
</script>
</body>
</html>
"""

#사이드 바 위젯
with st.sidebar:
    st.write("채팅")
    js_test.draw_chat()
    weather.draw_weather()

    
st.title("플래피버드")
components.html(code,width=800,height=1000)