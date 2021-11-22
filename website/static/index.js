function dogDescription(name) {
  var y = document.getElementById(name).previousElementSibling.childNodes[1].childNodes[1].innerHTML;
  var xhr = new XMLHttpRequest();
  var url = "https://dogs-service-cs361.herokuapp.com/";
  xhr.open("POST", url, true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      var json = JSON.parse(xhr.responseText);
      var x = document.getElementById(name);
      x.innerHTML = json.snippet + "<br></br><p>Link to Wiki page <a target='_blank' href="+json.url+">here</a></p>";
    
      if (x.style.display === "none") {
        x.style.display = "block";
      } else {
        x.style.display = "none";
      }
    }
  };
  var data = JSON.stringify({ breed: y });
  xhr.send(data);
}

function toggleMenu() {
  document.getElementById("sidebar").classList.toggle("active");
}

function filterDogs() {
  var cardPrimary = document.getElementById('cardPrimary').children;
  var cardSecondary = document.getElementById('cardSecondary').children;
  var cardAge = document.getElementById('cardAge').children;
  var cardSize = document.getElementById('cardSize').children;
  var cardGender = document.getElementById('cardGender').children;

  const checkedPrimary = addToCheckedList(cardPrimary)
  const checkedSecondary = addToCheckedList(cardSecondary)
  const checkedAge = addToCheckedList(cardAge)
  const checkedSize = addToCheckedList(cardSize)
  const checkedGender = addToCheckedList(cardGender)

  var dogSection = document.getElementsByClassName("dogSection")[0].children;

  // Reset before each filter
  for (var i in dogSection){
    var sectParams = dogSection[i].children;
    if(sectParams) {
      var block = dogSection[i];
      block.style.display = 'block';
    }
  }

  for (var eachDog in dogSection) {
    var sectParams = dogSection[eachDog].children;
    if(sectParams) {
      const allCheckedParams = {};

      var dogPrimBreed = sectParams[3].children[0].children[1].innerHTML.trim();
      allCheckedParams['primary'] = dogPrimBreed;
      var dogSecBreed = sectParams[3].children[1].children[1].innerHTML.trim();
      allCheckedParams['secondary'] = dogSecBreed;
      var dogAge = sectParams[3].children[2].children[1].innerHTML.trim();
      allCheckedParams['age'] = dogAge;
      var dogSize = sectParams[3].children[3].children[1].innerHTML.trim();
      allCheckedParams['size'] = dogSize;
      var dogGender = sectParams[3].children[4].children[1].innerHTML.trim();
      allCheckedParams['gender'] = dogGender;

      var block = dogSection[eachDog];

      for(var i in allCheckedParams) {
        if (i == 'primary') {
          if (checkedPrimary.length > 0) {
            if(checkedPrimary.includes(allCheckedParams[i]) == true && block.style.display != 'none'){
              block.style.display = 'block';
            } else {
              block.style.display = 'none';
            }
          }
        }
        if (checkedSecondary.length > 0){
          if (i == 'secondary') {
            if(checkedSecondary.includes(allCheckedParams[i]) == true && block.style.display != 'none'){
              block.style.display = 'block';
            } else {
              block.style.display = 'none';
            }
          }
        }
        if (checkedAge.length > 0){
          if (i == 'age') {
            if(checkedAge.includes(allCheckedParams[i]) == true && block.style.display != 'none'){
              block.style.display = 'block';
            } else {
              block.style.display = 'none';
            }
          }
        }
        if (checkedSize.length > 0){
          if (i == 'size') {
            if(checkedSize.includes(allCheckedParams[i]) == true && block.style.display != 'none'){
              block.style.display = 'block';
            } else {
              block.style.display = 'none';
            }
          }
        }
        if (checkedGender.length > 0){
          if (i == 'gender') {
            if(checkedGender.includes(allCheckedParams[i]) == true && block.style.display != 'none'){
              block.style.display = 'block';
            } else {
              block.style.display = 'none';
            }
          }
        }
      }
    }
  }
}


function addToCheckedList(param) {
  const checkedArray = []
  for (var each in param) {
    if(param[each].children){
      if(param[each].children[0].checked == true){
        checkedArray.push(param[each].children[0].value)
      }
    }
  }
  return checkedArray
}


function filterRescues() {
  const checkedZip = [];

  var cardZip = document.getElementById('cardZip').children;
  
  for (var each in cardZip) {
    if(cardZip[each].children){
      if(cardZip[each].children[0].checked == true){
        checkedZip.push(cardZip[each].children[0].value)
      }
    }
  }

  var rescueSection = document.getElementsByClassName("rescueSection")[0].children;
  

  // Reset before each filter
  for (var i in rescueSection){
    var sectParams = rescueSection[i].children;
    if(sectParams) {
      var block = rescueSection[i];
      block.style.display = 'block';
    }
  }

  for (var eachRescue in rescueSection) {
    var sectParams = rescueSection[eachRescue].children;
    if(sectParams) {
      const allCheckedParams = {};

      var rescueZip = sectParams[2].children[14].innerHTML.trim();
      allCheckedParams['zip'] = rescueZip;

      var block = rescueSection[eachRescue];

      for(var i in allCheckedParams) {
        if (i == 'zip') {
          if (checkedZip.length > 0) {
            if(checkedZip.includes(allCheckedParams[i]) == true && block.style.display != 'none'){
              block.style.display = 'block';
            } else {
              block.style.display = 'none';
            }
          }
        }
      }
    }
  }
}