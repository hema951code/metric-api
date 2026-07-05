import time
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

# ============================================================
# EDIT THIS ONE LINE: put your logged-in email here
# ============================================================
YOUR_EMAIL = "22f1000951@ds.study.iitm.ac.in"

# The single origin that is allowed to receive CORS headers.
ALLOWED_ORIGIN = "https://dash-rxga1i.example.com"

app = FastAPI()


# ------------------------------------------------------------
# Middleware: adds X-Request-ID and X-Process-Time to every
# response, and enforces the strict per-origin CORS policy
# manually (no wildcard, only the assigned origin gets the
# Access-Control-Allow-Origin header).
# ------------------------------------------------------------
class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        request_id = str(uuid.uuid4())
        origin = request.headers.get("origin")

        # Handle CORS preflight (OPTIONS) requests directly.
        if request.method == "OPTIONS":
            headers = {
                "X-Request-ID": request_id,
                "X-Process-Time": f"{time.time() - start_time:.6f}",
            }
            if origin == ALLOWED_ORIGIN:
                headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
                headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
                headers["Access-Control-Allow-Headers"] = "*"
                headers["Vary"] = "Origin"
            return JSONResponse(content={}, headers=headers)

        # Normal request path.
        response = await call_next(request)
        process_time = time.time() - start_time

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.6f}"

        if origin == ALLOWED_ORIGIN:
            response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
            response.headers["Vary"] = "Origin"

        return response


app.add_middleware(CustomMiddleware)


@app.get("/stats")
def get_stats(values: str):
    """
    Parse a comma-separated list of integers from `values` and
    return descriptive statistics, computed fresh every call.
    """
    nums = [int(v.strip()) for v in values.split(",") if v.strip() != ""]

    count = len(nums)
    total = sum(nums)
    minimum = min(nums)
    maximum = max(nums)
    mean = total / count

    return {
        "email": "22f1000951@ds.study.iitm.ac.in",
        "count": count,
        "sum": total,
        "min": minimum,
        "max": maximum,
        "mean": mean,
    }


@app.get("/")
def root():
    return {"status": "ok"}
