from flask import Blueprint, jsonify, request
from src.models.user import User, db
from functools import wraps
import time
import re

user_bp = Blueprint('user', __name__)

# Rate limiting storage for user routes
user_request_counts = {}

def user_rate_limit(max_requests=50, window=60):
    """Rate limiting decorator for user routes"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr
            current_time = time.time()
            
            if client_ip not in user_request_counts:
                user_request_counts[client_ip] = {'count': 0, 'reset_time': current_time + window}
            
            if current_time > user_request_counts[client_ip]['reset_time']:
                user_request_counts[client_ip] = {'count': 0, 'reset_time': current_time + window}
            
            if user_request_counts[client_ip]['count'] >= max_requests:
                return jsonify({
                    'error': 'User rate limit exceeded. Please try again later.',
                    'retry_after': int(user_request_counts[client_ip]['reset_time'] - current_time)
                }), 429
            
            user_request_counts[client_ip]['count'] += 1
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_user_data(required_fields=None, optional_fields=None):
    """User data validation decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.method == 'POST' or request.method == 'PUT':
                if not request.is_json:
                    return jsonify({'error': 'Content-Type must be application/json'}), 400
                
                data = request.get_json()
                if data is None:
                    return jsonify({'error': 'Invalid JSON data'}), 400
                
                # Check required fields
                if required_fields:
                    missing_fields = [field for field in required_fields if field not in data]
                    if missing_fields:
                        return jsonify({
                            'error': f'Missing required fields: {", ".join(missing_fields)}'
                        }), 400
                
                # Validate and sanitize data
                if 'username' in data:
                    if not isinstance(data['username'], str) or len(data['username'].strip()) == 0:
                        return jsonify({'error': 'Username must be a non-empty string'}), 400
                    # Sanitize username
                    data['username'] = re.sub(r'[<>"\']', '', data['username'].strip())[:50]
                
                if 'email' in data:
                    if not isinstance(data['email'], str) or len(data['email'].strip()) == 0:
                        return jsonify({'error': 'Email must be a non-empty string'}), 400
                    # Basic email validation
                    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                    if not re.match(email_pattern, data['email']):
                        return jsonify({'error': 'Invalid email format'}), 400
                    # Sanitize email
                    data['email'] = data['email'].strip()[:100]
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@user_bp.route('/users', methods=['GET'])
@user_rate_limit(max_requests=100, window=60)  # 100 user list requests per minute
def get_users():
    """Get all users with pagination and mobile optimization"""
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)  # Max 100 per page
        
        # Ensure reasonable limits
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 20
        
        # Get total count for pagination
        total_count = User.query.count()
        
        # Get paginated users
        offset = (page - 1) * per_page
        users = User.query.offset(offset).limit(per_page).all()
        
        result = []
        for i, user in enumerate(users):
            result.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'rank': offset + i + 1
            })
        
        return jsonify({
            'users': result,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_count': total_count,
                'total_pages': (total_count + per_page - 1) // per_page
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch users',
            'message': 'Please try again later'
        }), 500

@user_bp.route('/users', methods=['POST'])
@user_rate_limit(max_requests=10, window=60)  # 10 user creation requests per minute
@validate_user_data(required_fields=['username', 'email'])
def create_user():
    """Create a new user with improved validation"""
    try:
        data = request.get_json()
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({
                'error': 'User already exists',
                'message': 'A user with this email already exists'
            }), 409
        
        existing_username = User.query.filter_by(username=data['username']).first()
        if existing_username:
            return jsonify({
                'error': 'Username already taken',
                'message': 'This username is already in use'
            }), 409
        
        user = User(username=data['username'], email=data['email'])
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'created_at': user.created_at.isoformat() if user.created_at else None
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to create user',
            'message': 'Please try again later'
        }), 500

@user_bp.route('/users/<int:user_id>', methods=['GET'])
@user_rate_limit(max_requests=200, window=60)  # 200 user detail requests per minute
def get_user(user_id):
    """Get a specific user by ID"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'error': 'User not found',
                'message': 'No user found with this ID'
            }), 404
        
        return jsonify({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'created_at': user.created_at.isoformat() if user.created_at else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch user',
            'message': 'Please try again later'
        }), 500

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@user_rate_limit(max_requests=20, window=60)  # 20 user update requests per minute
@validate_user_data(optional_fields=['username', 'email'])
def update_user(user_id):
    """Update a user with improved validation"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'error': 'User not found',
                'message': 'No user found with this ID'
            }), 404
        
        data = request.get_json()
        
        # Check if new email already exists (if email is being updated)
        if 'email' in data and data['email'] != user.email:
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user:
                return jsonify({
                    'error': 'Email already exists',
                    'message': 'A user with this email already exists'
                }), 409
        
        # Check if new username already exists (if username is being updated)
        if 'username' in data and data['username'] != user.username:
            existing_user = User.query.filter_by(username=data['username']).first()
            if existing_user:
                return jsonify({
                    'error': 'Username already taken',
                    'message': 'This username is already in use'
                }), 409
        
        # Update user fields
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        
        db.session.commit()
        
        return jsonify({
            'message': 'User updated successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'created_at': user.created_at.isoformat() if user.created_at else None
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to update user',
            'message': 'Please try again later'
        }), 500

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@user_rate_limit(max_requests=10, window=60)  # 10 user deletion requests per minute
def delete_user(user_id):
    """Delete a user with confirmation"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'error': 'User not found',
                'message': 'No user found with this ID'
            }), 404
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User deleted successfully',
            'deleted_user_id': user_id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to delete user',
            'message': 'Please try again later'
        }), 500

@user_bp.route('/users/search', methods=['GET'])
@user_rate_limit(max_requests=50, window=60)  # 50 user search requests per minute
def search_users():
    """Search users by username or email with pagination"""
    try:
        query = request.args.get('q', '').strip()
        if not query or len(query) < 2:
            return jsonify({
                'error': 'Search query too short',
                'message': 'Please provide a search query with at least 2 characters'
            }), 400
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 50)  # Max 50 per page
        
        # Ensure reasonable limits
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 50:
            per_page = 20
        
        # Search users by username or email
        search_pattern = f'%{query}%'
        users_query = User.query.filter(
            db.or_(
                User.username.ilike(search_pattern),
                User.email.ilike(search_pattern)
            )
        )
        
        # Get total count for pagination
        total_count = users_query.count()
        
        # Get paginated results
        offset = (page - 1) * per_page
        users = users_query.offset(offset).limit(per_page).all()
        
        result = []
        for i, user in enumerate(users):
            result.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'rank': offset + i + 1
            })
        
        return jsonify({
            'users': result,
            'search_query': query,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_count': total_count,
                'total_pages': (total_count + per_page - 1) // per_page
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to search users',
            'message': 'Please try again later'
        }), 500
