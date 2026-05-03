from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import dataclasses
import sys
import os

# Add parent directory to sys.path to import compiler/runtime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.semantic import SemanticAnalyzer
from compiler.codegen import CodeGenerator
from compiler.errors import PlainscriptError
from runtime.executor import Executor

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/tokenize', methods=['POST'])
def tokenize():
    code = request.json.get('code', '')
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        return jsonify({
            "tokens": [t.to_dict() for t in tokens if t.type != 'TK_EOF']
        })
    except PlainscriptError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Internal Error: {str(e)}"}), 500

@app.route('/parse', methods=['POST'])
def parse():
    code = request.json.get('code', '')
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens, code)
        ast = parser.parse()
        return jsonify({"ast": dataclasses.asdict(ast)})
    except PlainscriptError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Internal Error: {str(e)}"}), 500

@app.route('/run', methods=['POST'])
def run():
    code = request.json.get('code', '')
    inputs = request.json.get('inputs', [])
    try:
        # Full compilation pipeline
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens, code)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        generator = CodeGenerator()
        python_code = generator.generate(ast)
        
        executor = Executor()
        result = executor.run(python_code, inputs=inputs)
        
        return jsonify({
            "output": result["output"],
            "error": result["error"],
            "generated_python": python_code
        })
        
    except PlainscriptError as e:
        return jsonify({
            "output": "",
            "error": str(e),
            "generated_python": ""
        }), 400
    except Exception as e:
        return jsonify({
            "output": "",
            "error": f"Internal Error: {str(e)}",
            "generated_python": ""
        }), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
