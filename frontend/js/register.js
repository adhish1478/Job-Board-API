const host= "http://56.228.30.131:8000/api/" // Base URL for the API

document.getElementById("registerForm").addEventListener("submit", async function(event) {
    event.preventDefault(); // Prevent the default form submission

    const email= document.getElementById("email").value.trim();
    const password= document.getElementById("password").value.trim();
    const role= document.getElementById("role").value;

    try {
        const response= await fetch(host + "register/", {
            method: "POST",
            mode: "cors",
            headers: {
                "content-type" : "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            body: JSON.stringify({email, password, role})
        });

        const data= await response.json();

        if (response.ok) {
            // Registration successful, redirect to login page
            window.location.href = "login.html";
        } else {
            // Handle registration error
            alert("Registration Failed: " + (data.error || "Unknown error, Please try after some time"));
        }

    } catch(err) {
            alert("Something went wrong, Please try after some time");
            console.error("Error during registration:", err);
        }});