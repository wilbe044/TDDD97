
displayView = function(){
	var token = getToken();
// the code required to display a view
    if (token === null ){
    document.getElementById("main").innerHTML = document.getElementById("welcomeView").innerHTML;
} else{
	document.getElementById("main").innerHTML = document.getElementById("profileView").innerHTML;
	getUserInfo();
	postWall();
}
};

window.onload = function(){
//code that is executed as the page is loaded.
//You shall put your own custom code here.
displayView();
};

validateCheck = function(form){ 	
	// var password = document.getElementById("password");
	// var repeatedPassword = document.getElementById("repeatedPassword");
	
	if (form.password.value != form.repeatedPassword.value){
		return false;
	}
	else if(form.password.value.length < 6 ){
		return false;
	}else {
		return true;
	}

 };

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

signInUser = function(form){
	var userData = {
		email: form.email.value,
		password: form.password.value
	};
    var data = encodeToFormUrl(userData);
    AJAXPostFunction("/sign_in", "Content-type", "application/x-www-form-urlencoded", data, function(){
        if (this.success) {
            localStorage.setItem("myToken", this.data);
            displayView();
        } else {
            document.getElementById("errorBox").style.display = "block";
		    document.getElementById("errorMessage").innerHTML = object.message;
        }
    });
};

signOutUser = function(){
    console.log(localStorage);
    AJAXGetFunction("/sign_out/"+localStorage.getItem("myToken")+"", function() {
        if(this.success){
            localStorage.removeItem("myToken");
            displayView();
            console.log(this.message)
        }
        else{
            console.log(this.message)
        }
    });
};

function setToken(token){
	localStorage.setItem("myToken", token);
}
function getToken(){
	return localStorage.getItem("myToken");
}
function changePassword(form){
	var token = getToken();
	var formData = {
		token: token,
        old_password: form.oldPassword.value,
		new_password: form.password.value
	}
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
function getUserInfo(){
	var token = getToken();
	var userInfo = serverstub.getUserDataByToken(token);
	localStorage.setItem("myEmail", userInfo.data.email);
	document.getElementById("email").innerHTML = userInfo.data.email;
	document.getElementById("firstname").innerHTML = userInfo.data.firstname;
	document.getElementById("familyname").innerHTML = userInfo.data.familyname;
	document.getElementById("gender").innerHTML = userInfo.data.gender;
	document.getElementById("city").innerHTML = userInfo.data.city;
	document.getElementById("country").innerHTML = userInfo.data.country;

}
function postMessage(form){
	var token = getToken();
	var message = {
		message: form.message.value
	};
	var toEmail = localStorage.getItem("myEmail");
	var object = serverstub.postMessage(token, message, toEmail);
	postWall();
}
function postOtherMessage(form){
	var token = getToken();
	var message = {
		message: form.message.value
	};
	var toEmail = localStorage.getItem("toEmail");
	var object = serverstub.postMessage(token, message, toEmail);
	postOtherWall();
}
function postWall(){
	var token = getToken();
	var userMessages = serverstub.getUserMessagesByToken(token);
	var text = "";
	for(i = 0; i < userMessages.data.length; i++){
		if(i == 10){break}
	text += userMessages.data[i].writer + ": " + userMessages.data[i].content.message + "<br>";
}
document.getElementById("wallContent").innerHTML = text;

}

function postOtherWall(){
	var token = getToken();
	var toEmail = localStorage.getItem("toEmail");
	var userMessages = serverstub.getUserMessagesByEmail(token, toEmail);
	var text = "";
	for(i = 0; i < userMessages.data.length; i++){
		if(i == 10){break}
	text += userMessages.data[i].writer + ": " + userMessages.data[i].content.message + "<br>";
}
document.getElementById("otherWallContent").innerHTML = text;

}

function goToUser(form){
	showDiv(4);
	var token = getToken();
	var toEmail = {
		toEmail: form.otherUserEmail.value
	};
	localStorage.setItem("toEmail", toEmail.toEmail);
	var otherUserInfo = serverstub.getUserDataByEmail(token, toEmail.toEmail);
	document.getElementById("otherEmail").innerHTML = otherUserInfo.data.email;
	document.getElementById("otherFirstname").innerHTML = otherUserInfo.data.firstname;
	document.getElementById("otherFamilyname").innerHTML = otherUserInfo.data.familyname;
	document.getElementById("otherGender").innerHTML = otherUserInfo.data.gender;
	document.getElementById("otherCity").innerHTML = otherUserInfo.data.city;
	document.getElementById("otherCountry").innerHTML = otherUserInfo.data.country;
}

var encodeToFormUrl = function(object) {
    var data, key;
    data = "";
    for (key in object)  {
        data += ""+key+"="+object[key]+"&";
    }
    data = data.substring(0, data.length - 1);
    return data;
};