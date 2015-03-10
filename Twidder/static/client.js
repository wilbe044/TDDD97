
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
		alert("Password do not match!");
		return false;
	}
	else if(form.password.value.length < 6 ){
		alert("Password must contain 6 or more characters!");
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
		var success = serverstub.signUp(formData);
		alert(success.message);
		if(success.success){
			var object = serverstub.signIn(formData.email, formData.password);
			localStorage.setItem("myToken", object.data);
			displayView();
		}
		
		return false;
	}
};

signInUser = function(form){
	var userData = {
		email: form.email.value,
		password: form.password.value
	}
	var object = serverstub.signIn(userData.email, userData.password);
	if (object.success){
		localStorage.setItem("myToken", object.data);
		displayView();
	} else{
		alert(object.message);
	}	

};

signOutUser = function(){
	var token = getToken();
	var object = serverstub.signOut(token);
	localStorage.removeItem("myToken");
	displayView();
};

function setToken(token){
	localStorage.setItem("myToken", token);
};

function getToken(){
	return localStorage.getItem("myToken");
};

function changePassword(form){
	var token = getToken();
	var formData = {
		oldPassword: form.oldPassword.value,
		newPassword: form.password.value
	}
	if(validateCheck(form)){
		var object = serverstub.changePassword(token, formData.oldPassword, formData.newPassword);
		alert(object.message);
	}
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

};

function postMessage(form){
	var token = getToken();
	var message = {
		message: form.message.value
	}
	var toEmail = localStorage.getItem("myEmail");
	var object = serverstub.postMessage(token, message, toEmail);
	postWall();
};

function postOtherMessage(form){
	var token = getToken();
	var message = {
		message: form.message.value
	}
	var toEmail = localStorage.getItem("toEmail");
	var object = serverstub.postMessage(token, message, toEmail);
	postOtherWall();
};

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
	}
	localStorage.setItem("toEmail", toEmail.toEmail);
	var otherUserInfo = serverstub.getUserDataByEmail(token, toEmail.toEmail);
	document.getElementById("otherEmail").innerHTML = otherUserInfo.data.email;
	document.getElementById("otherFirstname").innerHTML = otherUserInfo.data.firstname;
	document.getElementById("otherFamilyname").innerHTML = otherUserInfo.data.familyname;
	document.getElementById("otherGender").innerHTML = otherUserInfo.data.gender;
	document.getElementById("otherCity").innerHTML = otherUserInfo.data.city;
	document.getElementById("otherCountry").innerHTML = otherUserInfo.data.country;
}

