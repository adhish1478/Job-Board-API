const host= "http://56.228.30.131:8000/api" // Base URL for the API

async function fetchJobs() {
    try {
        const token= localStorage.getItem('token');
        const response= await fetch(host + "/jobs/", {
            method: 'GET',
            headers: {
                "Content-Type": "application/json",
                //"Authorization": "Bearer " + token
            }
        });

        if(!response) throw new Error("Failed to fetch Jobs!");

        const jobs= await response.json()
        renderJobs(jobs);

    } catch(err) {
        console.error("Error loading jobs: ", err);
        alert("Could not load jobs, Please try again later.")
    }
}

function renderJobs(jobs) {
    const jobList= document.getElementById('jobList');
    jobList.innerHTML= "";

    const jobArray= jobs.results || jobs; // Handles both paginated and raw list

    if (!jobArray.length) {
        jobList.innerHTML= "<p>No jobs to display!</p>";
        return;
    }

    jobArray.forEach(job => {
        const div= document.createElement('div');
        div.className= 'job-block'
        div.innerHTML= `
            <h5>${job.title}</h5>
            <p>${job.description}</p>
            <p><strong>Location:</strong> ${job.location}</p>
            <p><strong>Skills:</strong> ${job.skills ? job.skills_required.split(",").join(", ") : "Not specified"}</p>
            <p><strong>Experience:</strong> ${job.min_experience} years</p>
            <button class="btn btn-success float-right" onclick="applyToJob(${job.id})">Apply</button>
        `;
        jobList.appendChild(div)
    });
}

async function applyToJob(jobId) {
    const token= localStorage.getItem('token');
    try {
        const res= await fetch(host + `/apply/${jobId}/`, {
            
            method: 'POST',
            headers: {
                "Authorization": "Bearer " + token
            }
        });

        if(res.ok) {
            alert("application submitted");
        } else {
            const data= await res.json();
            alert(data.detail || "already submitted or error occured.");
        }

    } catch (err) {
        alert("error applying to job!", err)
    }
}

fetchJobs();