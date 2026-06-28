import axios from "axios";

const apiClient = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    withCredentials: true,
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFToken',
});

export const browserBaseURL = import.meta.env.VITE_API_URL;

let csrfToken = null;
let csrfRequest = null;
const unsafeMethods = new Set(['post', 'put', 'patch', 'delete']);

async function ensureCsrfToken() {
    if (csrfToken) return csrfToken;
    if (!csrfRequest) {
        csrfRequest = apiClient.get('/csrf/', { skipCsrf: true })
            .then((response) => {
                csrfToken = response.data.csrfToken;
                return csrfToken;
            })
            .finally(() => {
                csrfRequest = null;
            });
    }
    return csrfRequest;
}

apiClient.interceptors.request.use(async (config) => {
    const method = (config.method || 'get').toLowerCase();
    if (!config.skipCsrf && unsafeMethods.has(method)) {
        const token = await ensureCsrfToken();
        config.headers = config.headers || {};
        config.headers['X-CSRFToken'] = token;
    }
    return config;
});

export default apiClient;
