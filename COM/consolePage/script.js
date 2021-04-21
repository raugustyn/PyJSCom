var data = false
function onLoad() {
    document.getElementById("root").innerHTML = ""
    if (data) {
        stopLoop = false
        for (var i = 0; i < data.length; i++) {
            drawData(document.getElementById("root"), data[i], false)
        }
    }
    else {
        document.getElementById("dataJS").innerHTML = ""
        var script = document.createElement("script")
        script.src="/console/data.js"
        stopLoop = true
        script.onload = ()=>{stopLoop = false;onLoad()}
        document.getElementById("dataJS").appendChild(script)
    }
    //commandsLoop()
    doLoop(true, 250)
}

function reloadPage() {
    //document.location.reload()
    data = false
    onLoad()
}

var commandTemplates = {
    "document.location.reload()": reloadPage
}

var stopLoop = true

function doLoop(canDoLoop, delay) {
    commandsLoop()
    canDoLoop = !stopLoop
    if (canDoLoop) {
        setTimeout(() => {
            doLoop(canDoLoop, delay)
        }, delay)
    }
}

function commandsLoop() {
    document.getElementById("commands").innerHTML = ""
    var script = document.createElement("script")
    script.src="/console/commands.js"
    document.getElementById("commands").appendChild(script)
}

function readTextFile(url, useMy1) {
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", url, true);
    rawFile.onreadystatechange = function () {
        if (rawFile.readyState === 4) {
            var allText = rawFile.responseText;
            if (useMy1) {
                parseCommands(allText)
            }
        }
    }
    rawFile.send();
}

function drawData(target, thingData, appendToAppending) {
    //console.log(thingData)
    var whatAppend, div, button, bar, barDiv, header, text, table, row, rowIndex, cell, cellIndex, input
    switch (thingData["type"]) {
        case "header":
            header = document.createElement(thingData["tag"])
            header.innerHTML = thingData["text"]
            whatAppend = header
            break
        case "progressBar":
            bar = document.createElement("div")
            bar.className = "w3-light-grey"
            bar.style.width = thingData["width"] + "px"
            barDiv = document.createElement("div")
            barDiv.className = "w3-blue"
            barDiv.style.height = "24px"
            barDiv.style.width = thingData["progress"] + "%"
            bar.appendChild(barDiv)
            // '<div class="w3-light-grey"><div class="w3-blue" style="height:24px;width:' + thingData["progress + '%"></div></div>'
            whatAppend = bar
            break
        case "text":
            text = document.createTextNode(thingData["text"])
            whatAppend = text
            break
        case "table":
            table = document.createElement("table")
            table.style.border = "1px solid black"
            for (rowIndex = 0; rowIndex < thingData["HTML"].length; rowIndex++) {
                row = document.createElement("tr")
                for (cellIndex = 0; cellIndex < thingData["HTML"][0].length; cellIndex++) {
                    cell = document.createElement("td")
                    //var cellInner = drawData("", thingData["HTML[rowIndex][cellIndex], true)
                    /*if (thingData["HTML[rowIndex][cellIndex].type === "progressBar"){

                    }*/
                    cell.appendChild(drawData("", thingData["HTML"][rowIndex][cellIndex], true))
                    cell.style.border = "1px solid black"
                    row.appendChild(cell)
                }
                table.appendChild(row)
            }
            if (thingData["fullWidth"] === "true") {
                table.style.width = window.innerWidth - 15 + "px"
            }
            whatAppend = table
            break
        case "sendData":
            div = document.createElement("div")
            button = document.createElement("button")
            button.innerHTML = thingData.buttonText
            button.onclick = function () {
                send(thingData.data)
            }
            div.appendChild(button)

            whatAppend = div
            break
        case "sendDataWithInput":
            div = document.createElement("div")
            input = document.createElement("input")
            input.placeholder = thingData.placeholder
            input.size = thingData.size
            input.id = thingData.id
            button = document.createElement("button")
            button.innerHTML = thingData.buttonText
            button.onclick = function () {
                send(thingData.firstPart+document.getElementById(thingData.id).value)
            }
            div.appendChild(input)
            div.appendChild(button)

            whatAppend = div
            break
    }
    if (appendToAppending) {
        return whatAppend
    } else {
        target.appendChild(whatAppend)
    }
}

var canSend = true
function send(text) {
    if (canSend) {
        //console.log("Sending text: ", text)
        //document.location.href = "/console/send?text=" + text
        var ifr = document.createElement("iframe")
        ifr.src = "/console/send?text=" + text
        document.getElementById("iframe").innerHTML = ""
        document.getElementById("iframe").appendChild(ifr)
        stopLoop = true
        canSend = false
        setTimeout(()=>{canSend = true}, 200)
        reloadPage()
    }
}

function onReceive(text) {
    console.log("Received text: ", text)

}

var errors = []

function newError(code, message) {
    errors.push({code, message})
    throwError(errors[errors.length - 1])
}

function throwError(error) {
    document.getElementById("errors").innerHTML += `<span class="error"><h1>Error</h1>ErrorCode: ${error.code}, ErrorMessage: ${error.message}</span><br>`
}
