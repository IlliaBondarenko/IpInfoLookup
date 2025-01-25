import threading
import os
from fastapi import FastAPI, HTTPException
import uvicorn
from ipinfo_lookup import get_ipinfo_api,get_macinfo_api

# Define FastAPI app
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}

@app.post("/ip/{ip}")
def get_ipinfo(ip: str):
    ip_info = get_ipinfo_api(ip)
    if "error" in ip_info:
        raise HTTPException(status_code=400, detail=ip_info["error"])
    return ip_info

@app.post("/oui/{mac_address}")
def get_ouiinfo(mac_address: str):  
    oui_info = get_macinfo_api(mac_address)
    if "error" in oui_info:
        raise HTTPException(status_code=400, detail=mac_address["error"])
    return oui_info

# Function to run FastAPI
def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Function to run Streamlit
def run_streamlit():
    os.system("streamlit run ipinfo_lookup.py --server.port 8501")

# Main logic of the script
def main():
    # Create threads for FastAPI and Streamlit
    fastapi_thread = threading.Thread(target=run_fastapi)
    streamlit_thread = threading.Thread(target=run_streamlit)
    
    # Start both threads
    fastapi_thread.start()
    streamlit_thread.start()

    # Wait for both threads to finish
    fastapi_thread.join()
    streamlit_thread.join()

# Entry point
if __name__ == "__main__":
    main()
