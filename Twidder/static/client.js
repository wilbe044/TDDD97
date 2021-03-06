
var ws = null;

// function that defines which view to display and functions to call
displayView = function(){
	var token = getToken();
// the code required to display a view
    if (token === null ){
    //document.getElementById("main").innerHTML = document.getElementById("welcomeView").innerHTML;
    fillMainHandlebar(document.getElementById("welcomeView"));
} else{
	//document.getElementById("main").innerHTML = document.getElementById("profileView").innerHTML;
    fillMainHandlebar(document.getElementById("profileView"));
	getUserInfo();
	postWall();
    getNumberMessages();
    getNumberUsers()
}
};

window.onload = function(){
//code that is executed as the page is loaded.
//You shall put your own custom code here.
displayView();
};

//function that validates that the password chosen when signing up or changing password is valid
validateCheck = function(form){
	
	if (form.password.value != form.repeatedPassword.value){
		return false;
	}
	else if(form.password.value.length < 6 ){
		return false;
	}else {
		return true;
	}
 };

//function that controls the socket connections
var newSocket = function() {
    // Establish a connection with the socket API if no connections is initiated
    if (ws == null) {
        ws = new WebSocket("ws://" + document.domain + ":5000/socketapi");
    } else {
        console.log("You are already connected to the socket")
    }

    ws.onopen = function () {
        console.log("Connection with websocket open")
        ws.send(JSON.stringify({"message": "I just connected // Client"}));
    };

    ws.onclose = function() {
      console.log("The connections has CLOSED")
    };

    ws.onmessage = function (response) {
        console.log("Message received from server");
        var data = JSON.parse(response.data);
        console.log(response.data);

        //Handle sign out login with same account
        if (data.action == "signOutSocket") {
            localStorage.clear();
            displayView();
            //displayError(data.message);
            console.log(data.message);
            ws.close();
            ws = null;
        }

        //Handle actions executed when a message is posted
        if (data.action == "updateMessages") {
            document.getElementById("messages_posted").innerHTML = data.count;
            console.log(data.message);
            postOtherWall();
            postWall();
        }

        //Handle actions executed when the amount of logged in users is changed
        if (data.action == "updateUserCount") {
            console.log("client update user count");
            document.getElementById("usersOnlineNumber").innerHTML = data.online;
            console.log(data.message);
            updateChart(data.online, data.offline);
        }
    };
};

//function that defines which div to show when logged in
 function showDiv(number){
 	if(number==1){
 		document.getElementById("home").style.display = "block";
		document.getElementById("browse").style.display = "none";
		document.getElementById("account").style.display = "none";
		document.getElementById("otherUser").style.display = "none";
		postWall();
 	}else if(number==2){
 		document.getElementById("home").style.display = "none";
		document.getElementById("browse").style.display = "block";
		document.getElementById("account").style.display = "none";
		document.getElementById("otherUser").style.display = "none";
 	}else if(number==3){
 		document.getElementById("home").style.display = "none";
		document.getElementById("browse").style.display = "none";
		document.getElementById("account").style.display = "block";
		document.getElementById("otherUser").style.display = "none";
 	}else if(number==4){
 		document.getElementById("home").style.display = "none";
		document.getElementById("browse").style.display = "none";
		document.getElementById("account").style.display = "none";
		document.getElementById("otherUser").style.display = "block";
		postOtherWall();
 	}
 };


var AJAXPostFunction = function(url, requestHeader, requestHeaderValue,  param, callback) {
    var httpRequest;
    httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function() {
        if (httpRequest.readyState === 4 && httpRequest.status===200) {
            callback.call(JSON.parse(httpRequest.responseText));
        }
    };
    httpRequest.open("POST", url, true);
    httpRequest.setRequestHeader(requestHeader, requestHeaderValue);
    httpRequest.send(param);
};

/*
 * Method that handles Ajax requests
 * @params - Url - url for request as string
 * method - request method as string
 * header - request header as string (x-www-form-urlencoded)
 * param - parameters as string
 * Callbacks a javascript object (Parsed JSON from the server)
 */

var AJAXGetFunction = function(url, callback) {
    var httpRequest;
    httpRequest = new XMLHttpRequest();
    httpRequest.onreadystatechange = function() {
        if (httpRequest.readyState === 4 && httpRequest.status===200) {
            //Parse the returned JSON object before returning it
            callback.call(JSON.parse(httpRequest.responseText));
        }
    };
    httpRequest.open("GET", url, true);
    httpRequest.send();
};

//function that signs up a new user and then signs in the new user
signUpUser = function(form){
	if (validateCheck(form)){
		var formData = {
			email: form.email.value,
			password: form.password.value,
			firstname: form.firstname.value, 
			familyname: form.lastname.value, 
			gender: form.gender.value, 
			city: form.city.value,
			country: form.country.value 
		}
        var data = encodeToFormUrl(formData);
        AJAXPostFunction("/sign_up", "Content-type", "application/x-www-form-urlencoded", data, function() {
            if (this.success) {
                signInUser(form);
            } else {
                document.getElementById("errorBox").style.display = "block";
                document.getElementById("errorMessage").innerHTML = this.message;
            }
            return false;
        });
	}else
        {
            document.getElementById("errorBox").style.display = "block";
            document.getElementById("errorMessage").innerHTML = "Password do not match or must contain at least 6 characters!";
        }
};

//function that signs in a current user
var signInUser = function(form){
	var userData = {
		email: form.email.value,
		password: form.password.value
	};
    var data = encodeToFormUrl(userData);
    AJAXPostFunction("/sign_in", "Content-type", "application/x-www-form-urlencoded", data, function(){
        if (this.success) {
            localStorage.setItem("myToken", this.data);
            displayView();
            newSocket();
        } else {
            document.getElementById("errorBox").style.display = "block";
		    document.getElementById("errorMessage").innerHTML = this.message;
        }
    });
};

//function that signs out a user
signOutUser = function(){
    AJAXGetFunction("/sign_out/"+localStorage.getItem("myToken")+"", function() {
        if(this.success){
            localStorage.clear();
            displayView();
            console.log(this.message);
            ws = null;
        }
        else{
            console.log(this.message);
        }
    });
};

//function that stores tha token in local storage
function setToken(token){
	localStorage.setItem("myToken", token);
}

//function that gets the token from local storage
function getToken(){
	return localStorage.getItem("myToken");
}

//function that changes a users password
function changePassword(form){
	var token = getToken();
	var formData = {
		token: token,
        old_password: form.oldPassword.value,
		new_password: form.password.value
	};
	if(validateCheck(form)) {
        var data = encodeToFormUrl(formData);
        AJAXPostFunction("/change_password", "Content-type", "application/x-www-form-urlencoded", data, function () {
            if (this.success) {
                document.getElementById("accountErrorBox").style.display = "block";
                document.getElementById("accountErrorMessage").innerHTML = this.message;
            } else {
                document.getElementById("accountErrorBox").style.display = "block";
                document.getElementById("accountErrorMessage").innerHTML = "Password error!";
            }
        });
    }else{
        document.getElementById("errorBox").style.display = "block";
        document.getElementById("errorMessage").innerHTML = "Password do not match or must contain at least 6 characters!";
    }
	form.oldPassword.value = "";
	form.password.value = "";
	form.repeatedPassword.value = "";
};

//function that gets the user data and semds it to the html file
function getUserInfo(){
    AJAXGetFunction("/get_user_data_by_token/"+localStorage.getItem("myToken")+"", function() {
        if (this.success) {
            localStorage.setItem("myEmail", this.data.email);
            document.getElementById("email").innerHTML = this.data.email;
            document.getElementById("firstname").innerHTML = this.data.firstname;
            document.getElementById("familyname").innerHTML = this.data.familyname;
            document.getElementById("gender").innerHTML = this.data.gender;
            document.getElementById("city").innerHTML = this.data.city;
            document.getElementById("country").innerHTML = this.data.country;
        }
        else{
            console.log(this.message)
        }
    });
};

//function that collects the messages from the db of a logged in user and calls postWall
function postMessage(form){
	var token = getToken();
    var toEmail = localStorage.getItem("myEmail");
	var message = {
        token: token,
		message: form.message.value,
        to_email: toEmail
	};
    form.message.value = "";
    var data = encodeToFormUrl(message);
    AJAXPostFunction("/post_message", "Content-type", "application/x-www-form-urlencoded", data, function () {
        if(this.success) {
            postWall();
        }
        else{
            console.log(this.message);
        }
    });
};

//function that collects the messages of another users from the db and calls postOtherWall
function postOtherMessage(form){
	var token = getToken();
    var toEmail = localStorage.getItem("toEmail");
	var formData = {
        token: token,
		message: form.otherMessage.value,
        to_email: toEmail
	};
    form.otherMessage.value = "";
    var data = encodeToFormUrl(formData);
    AJAXPostFunction("/post_message", "Content-type", "application/x-www-form-urlencoded", data, function () {
        if(this.success) {
            postOtherWall();
        }
        else{
            console.log(this.message);
        }
    });
};

//function that sends the logged in users messages to the html file to be shown
function postWall(){
    AJAXGetFunction("/get_user_messages_by_token/"+localStorage.getItem("myToken")+"", function() {
        if (this.success) {
            var text = "";
            var counter = this.data.length;
            for (i = 0; i < this.data.length; i++) {
                if (i == 10) {
                    break
                }
                counter = counter - 1;
                text += this.data[counter].writer + ": " + this.data[counter].message + "<br>";
            }
            document.getElementById("wallContent").innerHTML = text;
        }
        else{
            console.log(this.message);
        }
    });
};

//function that sends another users messages to the html file to be shown
function postOtherWall(){
	var token = getToken();
	var toEmail = localStorage.getItem("toEmail");
    var formData = {
        token: token,
        email: toEmail
    };
    var data = encodeToFormUrl(formData);
    AJAXPostFunction("/get_user_messages_by_email", "Content-type", "application/x-www-form-urlencoded", data, function () {
        if(this.success) {
            var text = "";
            var counter = this.data.length;
            for (i = 0; i < this.data.length; i++) {
                if (i == 10) {
                    break
                }
                counter =counter-1;
                text += this.data[counter].writer + ": " + this.data[counter].message + "<br>";
            }
            document.getElementById("otherWallContent").innerHTML = text;
        }else{
            console.log(this.message)
        }
    });
};

//function that shows the information and wall of another users the logged in users searched for
function goToUser(form){
	var token = getToken();
	var formData = {
        token: token,
		to_email: form.otherUserEmail.value
	}
    console.log(formData.to_email);
	form.otherUserEmail.value = "";
	localStorage.setItem("toEmail", formData.to_email);
    var data = encodeToFormUrl(formData);
    AJAXPostFunction("/get_user_data_by_email", "Content-type", "application/x-www-form-urlencoded", data, function () {
        if (this.success) {
            document.getElementById("otherEmail").innerHTML = this.data.email;
            document.getElementById("otherFirstname").innerHTML = this.data.firstname;
            document.getElementById("otherFamilyname").innerHTML = this.data.familyname;
            document.getElementById("otherGender").innerHTML = this.data.gender;
            document.getElementById("otherCity").innerHTML = this.data.city;
            document.getElementById("otherCountry").innerHTML = this.data.country;
            showDiv(4);
            document.getElementById("browseErrorBox").style.display = "none";
        }
        else {
            document.getElementById("browseErrorBox").style.display = "block";
            document.getElementById("browseErrorMessage").innerHTML = this.message;
        }
    });
};


var encodeToFormUrl = function(object) {
    var data, key;
    data = "";
    for (key in object)  {
        data += ""+key+"="+object[key]+"&";
    }
    data = data.substring(0, data.length - 1);
    return data;
};

//Allows to drop something in a div.
function allowDrop(ev) {
    ev.preventDefault();
}

//Function that drags an element.
function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

//The function that drops an element.
function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    ev.target.appendChild(document.getElementById(data));
}

//function that gets the total number of messages posted on twidder
var getNumberMessages = function (){
    AJAXGetFunction("/get_number_messages", function(){
        if (this.success){
            document.getElementById("messages_posted").innerHTML = this.data;
            console.log(this.data)
        } else {
            console.log(this.message)
        }
    });
};

//function that gets the total number of logged in users on Twidder
var getNumberUsers = function () {
    AJAXGetFunction("/get_number_users", function(){
        if (this.success){
            online_users = this.data.online;
            total_users = this.data.total;
            offline_users = total_users - online_users;
            document.getElementById("usersOnlineNumber").innerHTML = online_users;
            renderChart(online_users, offline_users);
        } else {
            console.log(this.message)
        }
    });
};

// Hanldebar function that fill main view
function fillMainHandlebar(view){
    var mainContent = document.getElementById("main");

    var source = view.innerHTML;
    var template = Handlebars.compile(source);

    mainContent.innerHTML = template();
}