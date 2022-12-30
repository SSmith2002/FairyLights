function fill(){
    let colour = document.getElementById("colorpicker").value.substring(1)

    params = {"colour":colour}
    result = formatURL("fill",params)

    return "Done"
}

async function formatURL(methodName,params = {}){
    let url = "/" + methodName + "?";
    for(let key in params){
        url += key + "=" + params[key] + "&";
    }

    url = url.substring(0,url.length-1)

    return await fetch(url)
}