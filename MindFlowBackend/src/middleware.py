from flask import request, jsonify, g
import time
import json
from functools import wraps
import gzip
import io

def request_logging_middleware():
    """Middleware to log request details for debugging"""
    g.start_time = time.time()
    
    # Log request details
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {request.method} {request.path}")
    print(f"  IP: {request.remote_addr}")
    print(f"  User-Agent: {request.headers.get('User-Agent', 'Unknown')}")
    print(f"  Content-Type: {request.headers.get('Content-Type', 'Unknown')}")
    
    if request.is_json:
        try:
            data = request.get_json()
            if data:
                print(f"  Request Data: {json.dumps(data, indent=2)[:200]}...")
        except:
            print("  Request Data: Invalid JSON")

def response_logging_middleware(response):
    """Middleware to log response details"""
    if hasattr(g, 'start_time'):
        duration = time.time() - g.start_time
        print(f"  Response Time: {duration:.3f}s")
        print(f"  Status Code: {response.status_code}")
    
    return response

def mobile_optimization_middleware():
    """Middleware to optimize responses for mobile devices"""
    user_agent = request.headers.get('User-Agent', '').lower()
    is_mobile = any(device in user_agent for device in ['mobile', 'android', 'iphone', 'ipad'])
    
    if is_mobile:
        # Add mobile-specific headers
        g.is_mobile = True
        g.mobile_optimizations = {
            'reduce_data': True,
            'compress_responses': True,
            'cache_aggressively': True
        }
    else:
        g.is_mobile = False
        g.mobile_optimizations = {
            'reduce_data': False,
            'compress_responses': True,
            'cache_aggressively': False
        }

def compression_middleware(response):
    """Middleware to compress responses"""
    if not g.get('mobile_optimizations', {}).get('compress_responses', True):
        return response
    
    # Check if response should be compressed
    content_type = response.headers.get('Content-Type', '')
    if not any(ct in content_type for ct in ['application/json', 'text/html', 'text/plain']):
        return response
    
    # Check if client accepts gzip
    if 'gzip' not in request.headers.get('Accept-Encoding', ''):
        return response
    
    # Compress response
    try:
        data = response.get_data()
        if len(data) < 1024:  # Don't compress small responses
            return response
        
        compressed_data = gzip.compress(data)
        response.set_data(compressed_data)
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Length'] = len(compressed_data)
        
        print(f"  Compressed response: {len(data)} -> {len(compressed_data)} bytes")
        
    except Exception as e:
        print(f"  Compression failed: {e}")
    
    return response

def error_handling_middleware(error):
    """Middleware to handle errors gracefully"""
    if hasattr(g, 'start_time'):
        duration = time.time() - g.start_time
        print(f"  Error occurred after {duration:.3f}s")
    
    # Log error details
    print(f"  Error: {error}")
    print(f"  Request: {request.method} {request.path}")
    print(f"  IP: {request.remote_addr}")
    
    # Return appropriate error response
    if hasattr(error, 'code'):
        status_code = error.code
    else:
        status_code = 500
    
    error_response = {
        'error': 'An error occurred',
        'message': 'Please try again later',
        'status_code': status_code
    }
    
    # Add more details in development
    if g.get('is_mobile', False):
        error_response['mobile_optimized'] = True
    
    return jsonify(error_response), status_code

def rate_limit_middleware():
    """Simple rate limiting middleware"""
    client_ip = request.remote_addr
    current_time = time.time()
    
    # Simple in-memory rate limiting (use Redis in production)
    if not hasattr(g, 'rate_limit_data'):
        g.rate_limit_data = {}
    
    if client_ip not in g.rate_limit_data:
        g.rate_limit_data[client_ip] = {'count': 0, 'reset_time': current_time + 60}
    
    if current_time > g.rate_limit_data[client_ip]['reset_time']:
        g.rate_limit_data[client_ip] = {'count': 0, 'reset_time': current_time + 60}
    
    # Check rate limit
    max_requests = 100 if g.get('is_mobile', False) else 200
    if g.rate_limit_data[client_ip]['count'] >= max_requests:
        return jsonify({
            'error': 'Rate limit exceeded',
            'message': 'Please try again later',
            'retry_after': int(g.rate_limit_data[client_ip]['reset_time'] - current_time)
        }), 429
    
    g.rate_limit_data[client_ip]['count'] += 1

def cache_control_middleware(response):
    """Middleware to add cache control headers"""
    # Add cache headers based on response type
    if request.path.startswith('/api/'):
        # API responses - short cache
        cache_time = 60 if g.get('is_mobile', False) else 300
        response.headers['Cache-Control'] = f'public, max-age={cache_time}'
    elif request.path.startswith('/static/'):
        # Static files - long cache
        response.headers['Cache-Control'] = 'public, max-age=31536000'  # 1 year
    else:
        # Other responses - no cache
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    
    # Add mobile-specific headers
    if g.get('is_mobile', False):
        response.headers['X-Mobile-Optimized'] = 'true'
    
    return response

def security_middleware(response):
    """Middleware to add security headers"""
    # Add security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # Add CORS headers if needed
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    
    return response

def apply_middleware(app):
    """Apply all middleware to the Flask app"""
    
    @app.before_request
    def before_request():
        """Run before each request"""
        request_logging_middleware()
        mobile_optimization_middleware()
        rate_limit_middleware()
    
    @app.after_request
    def after_request(response):
        """Run after each request"""
        response = response_logging_middleware(response)
        response = compression_middleware(response)
        response = cache_control_middleware(response)
        response = security_middleware(response)
        return response
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle all exceptions"""
        return error_handling_middleware(error)
    
    @app.errorhandler(404)
    def handle_404(error):
        """Handle 404 errors"""
        return jsonify({
            'error': 'Endpoint not found',
            'message': 'The requested resource does not exist',
            'status_code': 404
        }), 404
    
    @app.errorhandler(500)
    def handle_500(error):
        """Handle 500 errors"""
        return jsonify({
            'error': 'Internal server error',
            'message': 'Something went wrong on our end. Please try again later.',
            'status_code': 500
        }), 500 