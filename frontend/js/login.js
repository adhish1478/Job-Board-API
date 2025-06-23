const host= "http://56.228.30.131:8000/api/" // Base URL for the API

document.getElementById('loginForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent the default form submission

    const email= document.getElementById('email').value.trim();
    const password= document.getElementById('password').value.trim();

    try {
        const response= await fetch(host + "token/", {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({email, password})
        });

        const data= await response.json();

        if(response.ok && data.access && data.refresh) {
            // Login successful, store the token and redirect to the dashboard
            localStorage.setItem('token', data.access);
            localStorage.setItem('refresh', data.refresh);
            window.location.href= "dashboard.html"; // Redirect to the dashboard page
        } else if (response.status === 401) {
            alert("Login failed: Invalid credentials.");
        } else {
            // Handle login error
            alert("Login Failed: " + (data.detail || "Unknown error, Please try again"));
        }
        } catch(err) {
            alert("Something went wrong, Please try after some time");
            console.error("Error during login:", err);
        }
    
});