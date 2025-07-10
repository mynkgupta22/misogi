import os
import json
from typing import Dict, List

def generate_sample_docs():
    # Technical documentation
    technical_docs = [
        {
            "content": """
            # API Integration Guide
            
            Our REST API uses JSON for all requests and responses. Here's how to get started:
            
            ## Authentication
            1. Get your API key from the dashboard
            2. Include it in the Authorization header:
               Authorization: Bearer YOUR_API_KEY
            
            ## Common Endpoints
            - GET /api/v1/users - List users
            - POST /api/v1/data - Submit data
            - PUT /api/v1/settings - Update settings
            
            ## Rate Limits
            - Free tier: 1000 requests/day
            - Pro tier: 10000 requests/day
            """,
            "metadata": {
                "title": "API Integration Guide",
                "type": "documentation",
                "tags": ["api", "integration", "authentication"]
            }
        },
        {
            "content": """
            # Error Handling Guide
            
            Common error codes and their solutions:
            
            ## 400 Bad Request
            - Check request payload format
            - Validate required fields
            
            ## 401 Unauthorized
            - Verify API key is valid
            - Check API key permissions
            
            ## 429 Too Many Requests
            - Rate limit exceeded
            - Upgrade plan or wait for reset
            """,
            "metadata": {
                "title": "Error Handling Guide",
                "type": "documentation",
                "tags": ["errors", "troubleshooting"]
            }
        }
    ]
    
    # Billing documentation
    billing_docs = [
        {
            "content": """
            # Pricing Plans
            
            Choose the plan that fits your needs:
            
            ## Basic Plan - $10/month
            - 1000 API calls/day
            - Email support
            - Basic analytics
            
            ## Pro Plan - $50/month
            - 10000 API calls/day
            - Priority support
            - Advanced analytics
            - Custom integrations
            
            ## Enterprise Plan
            - Unlimited API calls
            - 24/7 support
            - Dedicated account manager
            - Custom features
            """,
            "metadata": {
                "title": "Pricing Plans",
                "type": "pricing",
                "tags": ["pricing", "plans", "billing"]
            }
        },
        {
            "content": """
            # Billing FAQ
            
            Common billing questions:
            
            ## Payment Methods
            - Credit/Debit cards
            - PayPal
            - Bank transfer (Enterprise only)
            
            ## Billing Cycle
            - Monthly billing on signup date
            - Annual plans get 2 months free
            
            ## Refunds
            - 30-day money-back guarantee
            - Pro-rated refunds for annual plans
            """,
            "metadata": {
                "title": "Billing FAQ",
                "type": "faq",
                "tags": ["billing", "payments", "refunds"]
            }
        }
    ]
    
    # Feature documentation
    feature_docs = [
        {
            "content": """
            # Product Roadmap 2024
            
            Upcoming features and improvements:
            
            ## Q1 2024
            - Mobile app launch
            - Dark mode support
            - Enhanced analytics dashboard
            
            ## Q2 2024
            - Team collaboration features
            - Custom integrations marketplace
            - API v2 release
            
            ## Q3 2024
            - AI-powered insights
            - Advanced reporting
            - Workflow automation
            """,
            "metadata": {
                "title": "Product Roadmap",
                "type": "roadmap",
                "tags": ["features", "roadmap", "upcoming"]
            }
        },
        {
            "content": """
            # Feature Comparison
            
            How we compare to alternatives:
            
            ## API Features
            - REST and GraphQL support
            - WebSocket real-time updates
            - Batch processing
            
            ## Analytics
            - Real-time dashboards
            - Custom reports
            - Export capabilities
            
            ## Integration
            - 50+ pre-built connectors
            - Custom webhook support
            - SSO integration
            """,
            "metadata": {
                "title": "Feature Comparison",
                "type": "comparison",
                "tags": ["features", "comparison"]
            }
        }
    ]
    
    # Create directories if they don't exist
    for doc_type in ["technical_docs", "billing_docs", "feature_docs"]:
        os.makedirs(f"app/data/{doc_type}", exist_ok=True)
    
    # Save documents
    docs_map = {
        "technical": technical_docs,
        "billing": billing_docs,
        "feature": feature_docs
    }
    
    for intent, docs in docs_map.items():
        with open(f"app/data/{intent}_docs/documents.json", "w") as f:
            json.dump(docs, f, indent=2)
            
if __name__ == "__main__":
    generate_sample_docs() 