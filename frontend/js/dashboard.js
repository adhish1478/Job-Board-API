const host = "http://56.228.30.131:8000/api" // Base URL for the API

async function fetchJobs() {
    try {
        const token = localStorage.getItem('token');
        const response = await fetchWithAuth(host + "/jobs/", {
            method: 'GET'
                //headers: {
                //"Content-Type": "application/json",
                //"Authorization": "Bearer " + token
                //}
        });

        if (!response) throw new Error("Failed to fetch Jobs!");

        const jobs = await response.json();
        const appliedJobs = await fetchAppliedJobs(token) //for rendering both jobs as well as applied jobs
        renderJobs(jobs, appliedJobs)


    } catch (err) {
        console.error("Error loading jobs: ", err);
        alert("Could not load jobs, Please try again later.")
    }
}

function renderJobs(jobs, appliedJobIds) {
    const jobList = document.getElementById('jobList');
    jobList.innerHTML = "";

    const jobArray = jobs.results || jobs; // Handles both paginated and raw list

    if (!jobArray.length) {
        jobList.innerHTML = "<p>No jobs to display!</p>";
        return;
    }

    jobArray.forEach(job => {
        const isApplied = appliedJobIds.includes(job.id);
        const applyButton = isApplied ?
            `<button class="btn btn-secondary" disabled>Already Applied</button>` :
            `<button class= "btn btn-success float-right" onclick="applyToJob(${job.id})">Apply</button>` // 4 lines of code for already applied grey style


        const div = document.createElement('div');
        div.className = isApplied ? 'job-block applied' : 'job-block';
        div.innerHTML = `
            <h5>${job.title}</h5>
            <p>${job.description}</p>
            <p><strong>Location:</strong> ${job.location}</p>
            <p><strong>Skills:</strong> ${job.skills_required ? job.skills_required.split(",").join(", ") : "Not specified"}</p>
            <p><strong>Experience:</strong> ${job.min_experience} years</p>
            ${applyButton}
        `;
        jobList.appendChild(div)
    });
}

async function applyToJob(jobId) {
    const token = localStorage.getItem('token');
    selectedJobId = jobId;

    try {
        const res = await fetchWithAuth(host + '/profile/');

        const profile = await res.json();
        const hasResume = profile.resume !== null && profile.resume !== "";

        const modalBody = document.getElementById('modalBodyContent');
        const resumeInput = document.getElementById('resumeInput');
        resumeInput.hidden = true;

        if (hasResume) {
            modalBody.innerHTML = `
            <p>You already have a resume uploaded. What would you like to do?</p>
            <button type="button" class="btn btn-outline-primary me-2" onclick="useExistingResume()">Use Existing Resume</button>
            <button type="button" class="btn btn-outline-secondary" onclick="uploadNewResume()">Upload New Resume</button>
            `;
        } else {
            modalBody.innerHTML = `<p>You haven’t uploaded a resume yet. Please upload one to apply.</p>`;
            resumeInput.hidden = false;
        }

        new bootstrap.Modal(document.getElementById('resumeModal')).show()

    } catch (err) {
        alert("Couldn't load profile, please login again");
        console.log('resume check failed!')
    }
}

function uploadNewResume() {
    document.getElementById('resumeInput').hidden = false;
}

function useExistingResume() {
    document.getElementById('resumeInput').hidden = true;
}

// Handle modal form submit
document.getElementById('resumeForm').addEventListener("submit", async function(e) {
    e.preventDefault();

    const token = localStorage.getItem('token')
    const formData = new FormData();
    const fileInput = document.getElementById('resumeInput');

    if (!fileInput.hidden && fileInput.files.length > 0) {
        formData.append("resume", fileInput.files[0]);
    }

    try {
        const response = await fetchWithAuth(`${host}/apply/${selectedJobId}/`, {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            alert("Application submitted succesfully!")
            bootstrap.Modal.getInstance(document.getElementById('resumeModal')).hide();
        } else {
            const data = await response.json();
            alert("Error: " + (data.detail || "Couldn't apply."))
        }
    } catch (err) {
        alert("Error applying to job!");
        console.error(err);
    }
});

// For checking applied jobs and greying out buttons
let appliedJobIds = []

async function fetchAppliedJobs(token) {
    try {
        const res = await fetchWithAuth(host + '/my-applications/');
        if (!res) throw new Error("Unauthorized or refresh failed");

        const data = await res.json();
        if (!Array.isArray(data)) throw new Error("Invalid data structure");

        return data.map(app => app.job)
    } catch (err) {
        console.error("Failed to fetch applied jobs", err);
        return [];
    }
}

fetchJobs();