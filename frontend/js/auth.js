const API_BASE = "http://56.228.30.131:8000/api";

async function fetchWithAuth(url, options = {}) {
    let token = localStorage.getItem("token");

    const headers = new Headers(options.headers || {});
    const isFormData = options.body instanceof FormData;

    if (!headers.has("Authorization")) {
        headers.set("Authorization", "Bearer " + token);
    }

    if (!isFormData && !headers.has("Content-Type")) {
        headers.set("Content-Type", "application/json");
    }

    options.headers = headers;

    let response = await fetch(url, options);

    if (response.status === 401) {
        const newToken = await refreshAccessToken();
        if (!newToken) return null;

        headers.set("Authorization", "Bearer " + newToken);
        options.headers = headers;

        response = await fetch(url, options);
    }

    return response;
}

async function refreshAccessToken() {
    const refresh = localStorage.getItem("refresh");
    if (!refresh) return null;

    const res = await fetch(`${API_BASE}/token/refresh/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ refresh }),
    });

    if (res.ok) {
        const data = await res.json();
        localStorage.setItem("token", data.access);
        return data.access;
    } else {
        console.warn("Refresh token expired or invalid");
        localStorage.clear();
        window.location.href = "login.html";
        return null;
    }
}