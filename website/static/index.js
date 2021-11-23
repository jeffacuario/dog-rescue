// API Call to Team mate microservice
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
      x.innerHTML =
        json.snippet +
        "<br></br><p>Link to Wiki page <a target='_blank' href=" +
        json.url +
        ">here</a></p>";

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

// Show/Hide Filter
function toggleMenu() {
  document.getElementById("sidebar").classList.toggle("active");
}

// Filter Dog Results based on selected parameters
function filterDogs() {
  var cardPrimary = document.getElementById("cardPrimary").children;
  var cardSecondary = document.getElementById("cardSecondary").children;
  var cardAge = document.getElementById("cardAge").children;
  var cardSize = document.getElementById("cardSize").children;
  var cardGender = document.getElementById("cardGender").children;

  const checkedPrimary = addToCheckedList(cardPrimary);
  const checkedSecondary = addToCheckedList(cardSecondary);
  const checkedAge = addToCheckedList(cardAge);
  const checkedSize = addToCheckedList(cardSize);
  const checkedGender = addToCheckedList(cardGender);

  var dogSection = document.getElementsByClassName("dogSection")[0].children;

  // Reset before each filter
  filterResetAll(dogSection)

  for (var eachDog in dogSection) {
    var sectParams = dogSection[eachDog].children;
    if (sectParams) {
      const allCheckedParams = {};

      var dogPrimBreed = sectParams[3].children[0].children[1].innerHTML.trim();
      var dogSecBreed = sectParams[3].children[1].children[1].innerHTML.trim();
      var dogAge = sectParams[3].children[2].children[1].innerHTML.trim();
      var dogSize = sectParams[3].children[3].children[1].innerHTML.trim();
      var dogGender = sectParams[3].children[4].children[1].innerHTML.trim();

      allCheckedParams["primary"] = dogPrimBreed;
      allCheckedParams["secondary"] = dogSecBreed;
      allCheckedParams["age"] = dogAge;
      allCheckedParams["size"] = dogSize;
      allCheckedParams["gender"] = dogGender;

      var block = dogSection[eachDog];

      for (var i in allCheckedParams) {
        hideOrDisplay(i, 'primary', checkedPrimary, allCheckedParams, block);
        hideOrDisplay(i, 'secondary', checkedSecondary, allCheckedParams, block);
        hideOrDisplay(i, 'age', checkedAge, allCheckedParams, block);
        hideOrDisplay(i, 'size', checkedSize, allCheckedParams, block);
        hideOrDisplay(i, 'gender', checkedGender, allCheckedParams, block);
      }
    }
  }
}


// Filter Rescue Results based on selected parameters
function filterRescues() {
  var cardZip = document.getElementById("cardZip").children;
  const checkedZip = addToCheckedList(cardZip);
  var rescueSection = document.getElementsByClassName("rescueSection")[0].children;

  // Reset before each filter
  filterResetAll(rescueSection)

  for (var eachRescue in rescueSection) {
    var sectParams = rescueSection[eachRescue].children;
    if (sectParams) {
      const allCheckedParams = {};
      var rescueZip = sectParams[2].children[14].innerHTML.trim();
      allCheckedParams["zip"] = rescueZip;
      var block = rescueSection[eachRescue];

      for (var i in allCheckedParams) {
        hideOrDisplay(i, 'zip', checkedZip, allCheckedParams, block);
      }
    }
  }
}

function hideOrDisplay(current, param, checkedParam, allCheckedParams, block){
  if (current == param) {
    if (checkedParam.length > 0) {
      if (checkedParam.includes(allCheckedParams[current]) == true && block.style.display != "none") {
        block.style.display = "block";
      } else {
        block.style.display = "none";
      }
    }
  }
}

function addToCheckedList(param) {
  const checkedArray = [];
  for (var each in param) {
    if (param[each].children) {
      if (param[each].children[0].checked == true) {
        checkedArray.push(param[each].children[0].value);
      }
    }
  }
  return checkedArray;
}

function filterResetAll(section){
  for (var i in section) {
    var sectParams = section[i].children;
    if (sectParams) {
      var block = section[i];
      block.style.display = "block";
    }
  }
}