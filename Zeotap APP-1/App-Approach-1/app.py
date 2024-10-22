from flask import Flask, request, jsonify, render_template, g
import json
import sqlite3

app = Flask(__name__)

# Database connection management
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('rules.db')
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Initialize the database
def init_db():
    with app.app_context():
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS rules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rule TEXT NOT NULL
                )
            ''')
            conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_rule', methods=['POST'])
def create_rule():
    data = request.get_json()
    rule_string = data['rule_string']
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO rules (rule) VALUES (?)", (rule_string,))
        conn.commit()
    return jsonify({'message': 'Rule created successfully'})

@app.route('/combine_rules', methods=['POST'])
def combine_rules():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT rule FROM rules")
        rules = cursor.fetchall()
        # Filter out None values and combine rules
        combined_rule = ' AND '.join([rule[0] for rule in rules if rule[0] is not None])
    return jsonify({'combined_rule': combined_rule})

@app.route('/evaluate_rules', methods=['POST'])
def evaluate_rules():
    try:
        data = request.get_json()
        combined_rule = data['combined_rule']
        context_string = data['context']  # Expect context as a JSON string
        
        # Parse the context string into a dictionary
        try:
            context = json.loads(context_string)
        except json.JSONDecodeError as e:
            return jsonify({'error': 'Invalid JSON format', 'details': str(e)}), 400
        
        # Normalize the combined rule for evaluation
        normalized_rule = normalize_expression(combined_rule)
        
        # Evaluate the combined rule safely
        result = safe_eval(normalized_rule, context)
        
        # Return true or false based on the evaluation result
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def normalize_expression(expression):
    expression = expression.replace(' AND ', ' and ').replace(' OR ', ' or ')
    expression = expression.replace('=', '==')
    return expression

def safe_eval(expression, context):
    try:
        allowed_names = {name: context[name] for name in context if name in context}
        return bool(eval(expression, {"__builtins__": None}, allowed_names))
    except Exception as e:
        raise ValueError(f"Failed to evaluate expression '{expression}': {str(e)}")

def create_ast(rule_string):
    tokens = rule_string.replace('(', ' ( ').replace(')', ' ) ').split()
    return parse_tokens(tokens)

@app.route('/result')
def result():
    result = request.args.get('result')
    return render_template('result.html', result=result)

def parse_tokens(tokens):
    if not tokens:
        return None
    token = tokens.pop(0)
    if token == '(':
        left = parse_tokens(tokens)
        op = tokens.pop(0)
        right = parse_tokens(tokens)
        tokens.pop(0)  # Remove the closing parenthesis
        return RuleNode('operator', left, right, op)
    else:
        return RuleNode('operand', value=token)

class RuleNode:
    def __init__(self, type, left=None, right=None, value=None):
        self.type = type
        self.left = left
        self.right = right
        self.value = value

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True, port=5001)  # Run on port 5001