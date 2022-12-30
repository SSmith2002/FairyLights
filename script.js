function fill(){
    let type = document.querySelector('input[name="designStyle"]:checked').value;
    let colour = document.getElementById("colorpicker").value.substring(1)

    params = {"colour":colour}
    result = formatURL("fill" + type,params)

    return "Done"
}

function gradient(){
    let colour1 = document.getElementById("gradient1").value.substring(1)
    let colour2 = document.getElementById("gradient2").value.substring(1)

    params = {"colour1":colour1,
                "colour2":colour2}
    result = formatURL("gradient",params)
}

function updateBrightness(){
    let value = document.getElementById("brightnessSlider").value

    params = {"value":value}
    result = formatURL("updateBrightness",params)
}

function updateSpeed(){
    let value = document.getElementById("animateSlider").value

    params = {"value":value}
    result = formatURL("updateSpeed",params)
}

async function formatURL(methodName,params = {}){
    let url = "/" + methodName + "?";
    for(let key in params){
        url += key + "=" + params[key] + "&";
    }

    url = url.substring(0,url.length-1)

    return await fetch(url)
}

var brightSlider = document.getElementById("brightnessSlider");
var brightVal = document.getElementById("brightnessValue");

brightSlider.oninput = function(){
    let value = this.value;
    brightVal.innerHTML = value;
}

var animateSlider = document.getElementById("animateSlider");
var animateVal = document.getElementById("animateValue");

animateSlider.oninput = function(){
    let value = this.value;
    animateVal.innerHTML = value;
}