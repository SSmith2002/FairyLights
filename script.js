function fill(){
    let colour = document.getElementById("colorpicker").value.substring(1)

    params = {"colour":colour}
    result = formatURL("fill",params)

    return "Done"
}

function gradient(){
    let colour1 = document.getElementById("gradient1").value.substring(1)
    let colour2 = document.getElementById("gradient2").value.substring(1)

    params = {"colour1":colour1,
                "colour2":colour2}
    result = formatURL("gradient",params)
}

async function formatURL(methodName,params = {}){
    let url = "/" + methodName + "?";
    for(let key in params){
        url += key + "=" + params[key] + "&";
    }

    url = url.substring(0,url.length-1)

    return await fetch(url)
}