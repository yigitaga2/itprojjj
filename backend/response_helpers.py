# Response helper functions for consistent API responses

from typing import Dict, Any, Optional, List
from datetime import datetime

def success_response(
    data: Any = None, 
    message: str = "Success", 
    status_code: int = 200
) -> Dict[str, Any]:
    """Create a standardized success response"""
    response = {
        "status": "success",
        "message": message,
        "timestamp": datetime.now().isoformat(),
        "status_code": status_code
    }
    
    if data is not None:
        response["data"] = data
    
    return response

def error_response(
    message: str = "An error occurred",
    error_code: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    status_code: int = 400
) -> Dict[str, Any]:
    """Create a standardized error response"""
    response = {
        "status": "error",
        "message": message,
        "timestamp": datetime.now().isoformat(),
        "status_code": status_code
    }
    
    if error_code:
        response["error_code"] = error_code
    
    if details:
        response["details"] = details
    
    return response

def paginated_response(
    items: List[Any],
    total: int,
    page: int = 1,
    per_page: int = 10,
    message: str = "Data retrieved successfully"
) -> Dict[str, Any]:
    """Create a paginated response"""
    return success_response(
        data={
            "items": items,
            "pagination": {
                "total": total,
                "page": page,
                "per_page": per_page,
                "total_pages": (total + per_page - 1) // per_page
            }
        },
        message=message
    )
