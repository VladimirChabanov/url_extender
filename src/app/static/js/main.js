async function extend(){
    let sliceLink = {
        url: (document.getElementById('link')).value,
        alias: (document.getElementById('alias')).value,
        password: (document.getElementById('passw')).value
    }

    console.log(sliceLink)
    let response = await fetch('/extendUrl', { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(sliceLink)
    });

    let result = await response.json();

    document.getElementById('result').value = result.alias
    document.getElementById('qrCode').src = result.qrCode
}

async function checkPass(){
    let err = document.getElementById('error')
    err.classList.add("hidden")
    
    const urlSearchParams = new URLSearchParams(window.location.search);
    const params = Object.fromEntries(urlSearchParams.entries());

    let goToUrl = {
        alias: params.alias,
        password: (document.getElementById('passwd')).value
    }

    let response = await fetch('/pass', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(goToUrl)
    });

    console.log(response);

    let result = await response.text();
    if (!response.ok) {
        err.value = result
        err.classList.remove("hidden")
    } else{
        location = result
    }
}