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
    selectedJobId= jobId;

    try {
        const res= await fetch(host + '/profile/' ,{
            headers:{
                'Authorization': 'Bearer ' + token
            }
        });

        const profile= await res.json();
        const hasResume= profile.resume !== null && profile.resume !== "";

        const modalBody= document.getElementById('modalBodyContent');
        const resumeInput= document.getElementById('resumeInput');
        resumeInput.hidden= true;

        if (hasResume) {
            modalBody.innerHTML=`
            <p>You already have a resume uploaded. What would you like to do?</p>
            <button type="button" class="btn btn-outline-primary me-2" onclick="useExistingResume()">Use Existing Resume</button>
            <button type="button" class="btn btn-outline-secondary" onclick="uploadNewResume()">Upload New Resume</button>
            `;
        } else {
            modalBody.innerHTML= `<p>You haven’t uploaded a resume yet. Please upload one to apply.</p>`;
            resumeInput.hidden= false;
        }

        new bootstrap.Modal(document.getElementById('resumeModal')).show()

    } catch(err) {
        alert("Couldn't load profile, please login again");
        console.log('resume check failed!')
    }
}

function uploadNewResume() {
    document.getElementById('resumeInput').hidden= false;
}

function useExistingResume() {
    document.getElementById('resumeInput').hidden= true;
}

// Handle modal form submit
document.getElementById('resumeForm').addEventListener("submit", async function (e) {
    e.preventDefault();
    
    const token= localStorage.getItem('token')
    const formData= new FormData();
    const fileInput= document.getElementById('resumeInput');

    if (!fileInput.hidden && fileInput.files.length > 0) {
        formData.append("resume", fileInput.files[0]);
    }

    try {
        const response= await fetch(`${host}/apply/${selectedJobId}/`, {
            method: 'POST',
            headers: {
                Authorization: "Bearer " + token
            },
            body: formData
        });

        if(response.ok) {
            alert("Application submitted succesfully!")
            bootstrap.Modal.getInstance(document.getElementById('resumeModal')).hide();
        } else {
            const data= await response.json();
            alert("Error: "+ (data.detail || "Couldn't apply."))
        }
    } catch (err) {
        alert("Error applying to job!");
        console.error(err);
    }
});

fetchJobs();

// resume popup and