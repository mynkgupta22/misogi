from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from pathlib import Path

app = FastAPI(title="Product Recommendation API")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load product data
def load_products():
    data_file = Path(__file__).parent.parent.parent / "data" / "products.json"
    with open(data_file, "r") as f:
        return json.load(f)["products"]  # Return just the products array

# Global variable to store products
PRODUCTS = load_products()

@app.get("/")
async def root():
    return {"message": "Welcome to the Product Recommendation API"}

@app.get("/api/products")
async def get_products():
    return PRODUCTS

# Import and include routers
from app.routers import auth, products, recommendations

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["recommendations"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 