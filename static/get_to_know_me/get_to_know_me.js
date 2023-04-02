var users = []
var xhr = new XMLHttpRequest();
xhr.open("GET", "static/users.json");
xhr.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200 && this.responseText) {
    var users = JSON.parse(this.responseText);
    var users_list = document.getElementById("users");
    for (var i = 0; i < users.length; i += 1) {
      let li = document.createElement("li");
      li.innerText = users[i];
      users_list.appendChild(li);
    }
  }
};
xhr.send();