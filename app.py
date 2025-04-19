from flask import Flask, render_template, request, jsonify
import random
import string
import secrets
from typing import List, Dict, Union
from functools import wraps

app = Flask(__name__)

# Configuration
app.config['MAX_PASSWORD_LENGTH'] = 128
app.config['MIN_PASSWORD_LENGTH'] = 4
app.config['DEFAULT_PASSWORD_LENGTH'] = 16

def validate_input(f):
    """Decorator to validate password generation input"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        data = request.get_json()
        
        # Validate length
        try:
            length = int(data.get('length', app.config['DEFAULT_PASSWORD_LENGTH']))
            if not (app.config['MIN_PASSWORD_LENGTH'] <= length <= app.config['MAX_PASSWORD_LENGTH']):
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({
                'error': f'Password length must be an integer between {app.config["MIN_PASSWORD_LENGTH"]} and {app.config["MAX_PASSWORD_LENGTH"]}'
            }), 400
        
        # Validate at least one character set is selected
        char_options = ['uppercase', 'lowercase', 'digits', 'special']
        if not any(data.get(opt, True) for opt in char_options):
            return jsonify({
                'error': 'At least one character set must be selected'
            }), 400
            
        return f(*args, **kwargs)
    return wrapper

def calculate_password_strength(password: str) -> Dict[str, Union[int, str]]:
    """Calculate password strength metrics"""
    strength = 0
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)
    length = len(password)
    
    # Score calculation
    strength += length * 4
    if has_upper: strength += 10
    if has_lower: strength += 10
    if has_digit: strength += 10
    if has_special: strength += 15
    
    # Strength categories
    if strength < 60:
        category = "Weak"
    elif strength < 90:
        category = "Moderate"
    elif strength < 120:
        category = "Strong"
    else:
        category = "Very Strong"
    
    return {
        'score': min(strength, 100),
        'category': category,
        'length': length,
        'has_upper': has_upper,
        'has_lower': has_lower,
        'has_digit': has_digit,
        'has_special': has_special
    }

def generate_password(
    length: int = 12,
    use_uppercase: bool = True,
    use_lowercase: bool = True,
    use_digits: bool = True,
    use_special: bool = True
) -> str:
    """
    Generate a cryptographically secure random password with specified criteria.
    
    Args:
        length: Length of the password
        use_uppercase: Include uppercase letters
        use_lowercase: Include lowercase letters
        use_digits: Include digits
        use_special: Include special characters
        
    Returns:
        Generated password string
    """
    character_sets = []
    
    if use_uppercase:
        character_sets.append(string.ascii_uppercase)
    if use_lowercase:
        character_sets.append(string.ascii_lowercase)
    if use_digits:
        character_sets.append(string.digits)
    if use_special:
        character_sets.append(string.punctuation)
    
    if not character_sets:
        raise ValueError("At least one character set must be selected")
    
    # Combine all character sets
    all_chars = ''.join(character_sets)
    
    # Ensure the password contains at least one character from each selected set
    password = []
    if use_uppercase:
        password.append(secrets.choice(string.ascii_uppercase))
    if use_lowercase:
        password.append(secrets.choice(string.ascii_lowercase))
    if use_digits:
        password.append(secrets.choice(string.digits))
    if use_special:
        password.append(secrets.choice(string.punctuation))
    
    # Fill the rest with random characters from all sets
    remaining_length = length - len(password)
    password.extend(secrets.choice(all_chars) for _ in range(remaining_length))
    
    # Shuffle to avoid predictable patterns
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)

@app.route('/')
def home():
    """Render the password generator UI"""
    return render_template('base.html')

@app.route('/api/generate', methods=['POST'])
@validate_input
def api_generate():
    """API endpoint for password generation"""
    data = request.get_json()
    
    try:
        password = generate_password(
            length=int(data.get('length', app.config['DEFAULT_PASSWORD_LENGTH'])),
            use_uppercase=data.get('uppercase', True),
            use_lowercase=data.get('lowercase', True),
            use_digits=data.get('digits', True),
            use_special=data.get('special', True)
        )
        
        strength = calculate_password_strength(password)
        
        return jsonify({
            'password': password,
            'strength': strength,
            'error': None
        })
        
    except Exception as e:
        app.logger.error(f"Password generation failed: {str(e)}")
        return jsonify({
            'password': None,
            'strength': None,
            'error': 'Failed to generate password'
        }), 500

@app.route('/api/strength', methods=['POST'])
def api_strength():
    """API endpoint to check password strength"""
    data = request.get_json()
    password = data.get('password', '')
    
    if not password:
        return jsonify({
            'error': 'No password provided'
        }), 400
        
    strength = calculate_password_strength(password)
    
    return jsonify({
        'strength': strength,
        'error': None
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)