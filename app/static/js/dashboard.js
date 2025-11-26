async function loadStats() {
    const res = await fetch("/api/stats/overview");
    const data = await res.json();

    document.getElementById("stats-container").innerHTML = `
        <p><strong>Total Jobs:</strong> ${data.total_jobs}</p>
        <p><strong>Total Companies:</strong> ${data.total_companies}</p>
        // <p><strong>Top Skill:</strong> ${data.top_skill}</p>
        <p><strong>Average Salary:</strong> ${data.avg_salary || "N/A"}</p>
    `;
}

async function loadJobs() {
    const res = await fetch("/api/jobs");
    const jobs = await res.json();

    document.getElementById("jobs-container").innerHTML = jobs.map(job => `
        <div class="job-card">
            <h3>${job.title}</h3>
            <p><strong>Company:</strong> ${job.company}</p>
            <p><strong>Location:</strong> ${job.location}</p>
            <p><strong>Salary:</strong> ${job.salary || "Not Provided"}</p>
            <a href="${job.apply_link}" target="_blank">Apply</a>
        </div>
    `).join("");
}

loadStats();
loadJobs();
