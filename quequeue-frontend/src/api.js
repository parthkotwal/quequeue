import axios from "axios";

const apiClient = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    withCredentials: true,
});

export const browserBaseURL = import.meta.env.VITE_API_URL;

export default apiClient;
