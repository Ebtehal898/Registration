$(document).ready(function(){ 
    $('#check').on("click", function(){
        var first_name =  document.forms["register"]["first_name"];
        var last_name =  document.forms["register"]["last_name"];  
        var email =  document.forms["register"]["email"]; 
        var birthday =  document.forms["register"]["birthday"]; 
        var password =  document.forms["register"]["password"]; 
        var confirm_pass =  document.forms["register"]["confirm_pass"]; 
        if (first_name.value == "" || last_name.value == "" || email.value == ""|| birthday.value == "" || password.value == "" ||confirm_pass.value == ""){
            window.alert("Please Fill All the Fields.");
            return false;
        }
        else
            return true; 
        
    });
});