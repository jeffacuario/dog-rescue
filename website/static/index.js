function dogDescription(name) {
  var y =
    document.getElementById(name).previousElementSibling.childNodes[1]
      .childNodes[1].innerHTML;
  // console.log(y)
  var xhr = new XMLHttpRequest();
  var url = "https://dogs-service-cs361.herokuapp.com/";
  xhr.open("POST", url, true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      var json = JSON.parse(xhr.responseText);
      console.log(json);

      var x = document.getElementById(name);
      x.innerHTML = json.snippet + "<br></br><p>Link to Wiki page <a target='_blank' href="+json.url+">here</a></p>";
    
      // console.log(x.innerHTML)

      if (x.style.display === "none") {
        x.style.display = "block";
      } else {
        x.style.display = "none";
      }
    }
  };
  var data = JSON.stringify({ breed: y });
  // console.log(data, y)
  xhr.send(data);
}

function togglemenu() {
  document.getElementById("sidebar").classList.toggle("active");
}

function filterDogs() {
  const checkedPrimary = [];
  var cardPrimary = document.getElementById('cardPrimary').children;
  // console.log(cardPrimary);

  
  for (var each in cardPrimary) {
    if(cardPrimary[each].children){
      if(cardPrimary[each].children[0].checked == true){
        checkedPrimary.push(cardPrimary[each].children[0].value)
      }
    }
  }

  // console.log(checkedPrimary);
  var dogSection = document.getElementsByClassName("dog_section")[0].children;
  for (var eachDog in dogSection) {

    if(dogSection[eachDog].children){
      var dogBreed = dogSection[eachDog].children[3].children[0].children[1].innerHTML.trim();
      var block = dogSection[eachDog];

      if (checkedPrimary.includes(dogBreed) == false){
        // console.log(dogSection[eachDog].children)
        // console.log(block);
        block.style.display = "none";
      }
      else if (checkedPrimary.includes(dogBreed) == true) {
        if((block.style.display == "none")==true){
          block.style.display = "block";
        }
      }
    }
  }


}