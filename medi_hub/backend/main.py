import uvicorn
from core.apis.api import app

if __name__ == "__main__":
    uvicorn.run(
        "core.apis.api:app",
        host="0.0.0.0",
        port=5100,
        reload=True,  # Auto-reload on file changes (development only)
        server_header=False,  # Don't expose uvicorn version in response headers
    )
