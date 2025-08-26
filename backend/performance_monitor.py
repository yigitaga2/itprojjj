# Performance monitoring utilities for the School Feedback Platform

import time
import functools
import logging
from typing import Dict, Any, Callable
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """Monitor and log performance metrics"""
    
    def __init__(self):
        self.metrics = {}
        self.start_time = time.time()
    
    def time_function(self, func_name: str = None):
        """Decorator to time function execution"""
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                name = func_name or f"{func.__module__}.{func.__name__}"
                start_time = time.time()
                
                try:
                    result = func(*args, **kwargs)
                    execution_time = time.time() - start_time
                    
                    # Log performance
                    logger.info(f"Function {name} executed in {execution_time:.4f}s")
                    
                    # Store metrics
                    if name not in self.metrics:
                        self.metrics[name] = []
                    self.metrics[name].append({
                        'execution_time': execution_time,
                        'timestamp': datetime.now().isoformat(),
                        'success': True
                    })
                    
                    return result
                    
                except Exception as e:
                    execution_time = time.time() - start_time
                    logger.error(f"Function {name} failed after {execution_time:.4f}s: {str(e)}")
                    
                    # Store error metrics
                    if name not in self.metrics:
                        self.metrics[name] = []
                    self.metrics[name].append({
                        'execution_time': execution_time,
                        'timestamp': datetime.now().isoformat(),
                        'success': False,
                        'error': str(e)
                    })
                    
                    raise
            
            return wrapper
        return decorator
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get performance metrics summary"""
        summary = {}
        
        for func_name, executions in self.metrics.items():
            if not executions:
                continue
                
            times = [e['execution_time'] for e in executions if e['success']]
            errors = [e for e in executions if not e['success']]
            
            if times:
                summary[func_name] = {
                    'total_calls': len(executions),
                    'successful_calls': len(times),
                    'failed_calls': len(errors),
                    'avg_time': sum(times) / len(times),
                    'min_time': min(times),
                    'max_time': max(times),
                    'total_time': sum(times)
                }
            else:
                summary[func_name] = {
                    'total_calls': len(executions),
                    'successful_calls': 0,
                    'failed_calls': len(errors),
                    'avg_time': 0,
                    'min_time': 0,
                    'max_time': 0,
                    'total_time': 0
                }
        
        return summary
    
    def log_metrics_summary(self):
        """Log performance metrics summary"""
        summary = self.get_metrics()
        
        logger.info("=== Performance Metrics Summary ===")
        for func_name, metrics in summary.items():
            logger.info(f"{func_name}:")
            logger.info(f"  Total calls: {metrics['total_calls']}")
            logger.info(f"  Success rate: {metrics['successful_calls']}/{metrics['total_calls']}")
            logger.info(f"  Avg time: {metrics['avg_time']:.4f}s")
            logger.info(f"  Min time: {metrics['min_time']:.4f}s")
            logger.info(f"  Max time: {metrics['max_time']:.4f}s")
    
    def reset_metrics(self):
        """Reset all metrics"""
        self.metrics = {}
        self.start_time = time.time()

# Global performance monitor instance
performance_monitor = PerformanceMonitor()

# Convenience decorators
def monitor_performance(func_name: str = None):
    """Decorator to monitor function performance"""
    return performance_monitor.time_function(func_name)

def monitor_sentiment_analysis(func):
    """Specific decorator for sentiment analysis functions"""
    return performance_monitor.time_function("sentiment_analysis")(func)

def monitor_database_operation(func):
    """Specific decorator for database operations"""
    return performance_monitor.time_function("database_operation")(func)

def monitor_api_endpoint(func):
    """Specific decorator for API endpoints"""
    return performance_monitor.time_function("api_endpoint")(func)

# Context manager for timing code blocks
class TimeBlock:
    """Context manager to time code blocks"""
    
    def __init__(self, name: str):
        self.name = name
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        execution_time = time.time() - self.start_time
        if exc_type is None:
            logger.info(f"Block '{self.name}' executed in {execution_time:.4f}s")
        else:
            logger.error(f"Block '{self.name}' failed after {execution_time:.4f}s")

# Usage examples:
# 
# @monitor_performance("custom_function")
# def my_function():
#     pass
#
# @monitor_sentiment_analysis
# def analyze_text(text):
#     pass
#
# with TimeBlock("data_processing"):
#     # Your code here
#     pass
