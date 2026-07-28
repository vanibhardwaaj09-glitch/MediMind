/**
 * MediMind Frontend Configuration
 * --------------------------------
 * This file stores settings used by app.js.
 *
 * When deploying to Render, update PRODUCTION_API_URL
 * with your Render backend URL (e.g. https://medimind-api.onrender.com)
 */

const CONFIG = {
  // Backend URL used when the site is deployed (Render)
  PRODUCTION_API_URL: "https://medimind-api.onrender.com",

  // Backend URL used during local development
  LOCAL_API_URL: "http://localhost:8000",

  // Maximum characters allowed in the symptoms text box
  MAX_SYMPTOMS_LENGTH: 500,
};

/**
 * Returns the correct API base URL depending on where the frontend is running.
 * - localhost / 127.0.0.1 → local FastAPI server
 * - anything else (Render) → production Render URL
 */
function getApiBaseUrl() {
  const hostname = window.location.hostname;
  const isLocal =
    hostname === "localhost" || hostname === "127.0.0.1";

  return isLocal ? CONFIG.LOCAL_API_URL : CONFIG.PRODUCTION_API_URL;
}
