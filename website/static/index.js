function myFunction(name) {
    var y = document.getElementById(name).previousElementSibling.childNodes[1].childNodes[1].innerHTML;
    console.log(y)
    var xhr = new XMLHttpRequest();
    var url = "https://dogs-service-cs361.herokuapp.com/";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var json = JSON.parse(xhr.responseText);
            // console.log(json);
            
            var x = document.getElementById(name);
            x.innerHTML = json.snippet
            console.log(x.innerHTML)


            if (x.style.display === "none") {
                x.style.display = "block";
            } else {
                x.style.display = "none";
            }
        }
    };
    var data = JSON.stringify({"breed": y});
    // console.log(data, y)
    xhr.send(data);


}


// https://dogs-service-cs361.herokuapp.com/
// {
//     "breed": "Bearded Collie"
// } 

