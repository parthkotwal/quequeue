import axios from "axios";

const isBrowser = typeof window !== "undefined";

const apiClient = axios.create({
    baseURL: isBrowser
        ? import.meta.env.VITE_API_URL_EXTERNAL // browser -> 127.0.0.1:5173:8000
        : import.meta.env.VITE_API_URL_INTERNAL, // container -> web:8000
    withCredentials: true,
});

export const browserBaseURL = import.meta.env.VITE_API_URL_EXTERNAL;

export default apiClient;
