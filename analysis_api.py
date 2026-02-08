from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from algorithm_analyzer import AlgorithmAnalyzer

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Jobealieu:therealworld@localhost:3306/algo_analyzer'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

my_db = SQLAlchemy(app)

# ========== DATABASE MODEL ==========
class AnalysisResults(my_db.Model):
    """Database model to store algorithm analysis results"""
    
    __tablename__ = "analysis_results"
    id = my_db.Column(my_db.Integer, primary_key=True)
    algorithm = my_db.Column(my_db.String(50), nullable=False)
    items = my_db.Column(my_db.Integer, nullable=False)
    steps = my_db.Column(my_db.Integer, nullable=False)
    start_time = my_db.Column(my_db.Float, nullable=False)
    end_time = my_db.Column(my_db.Float, nullable=False)
    total_time = my_db.Column(my_db.Float, nullable=False)
    time_complexity = my_db.Column(my_db.String(20), nullable=False)
    graph_image_path = my_db.Column(my_db.Text, nullable=False)

    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            "id": self.id,
            "algo": self.algorithm,
            "items": self.items,
            "steps": self.steps,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "total_time_ms": self.total_time,
            "time_complexity": self.time_complexity,
            "path_to_graph": self.graph_image_path
        }


# ========== API ENDPOINTS ==========

@app.route('/analyze', methods=['GET'])
def analyze():
    """
    Endpoint 1: Analyze algorithm performance
    
    Query Parameters:
        - algo: Algorithm name (bubble, linear, binary, nested, exponential)
        - n: Number of elements to analyze
        - steps: Number of steps for analysis
    
    Example: /analyze?algo=bubble&n=1000&steps=10
    """
    try:
        # Get query parameters
        algo = request.args.get('algo', type=str)
        n = request.args.get('n', type=int)
        steps = request.args.get('steps', type=int)
        
        # Validate parameters
        if not algo:
            return jsonify({"error": "Missing 'algo' parameter"}), 400
        if not n:
            return jsonify({"error": "Missing 'n' parameter"}), 400
        if not steps:
            return jsonify({"error": "Missing 'steps' parameter"}), 400
        
        # Validate algorithm name
        valid_algos = ["bubble", "linear", "binary", "nested", "exponential"]
        if algo not in valid_algos:
            return jsonify({
                "error": f"Invalid algorithm. Must be one of: {', '.join(valid_algos)}"
            }), 400
        
        # Perform analysis
        result = AlgorithmAnalyzer.analyze_algorithm(algo, n, steps)
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/save_analysis', methods=['POST'])
def save_analysis():
    """
    Endpoint 2: Save analysis results to database
    
    Request Body (JSON):
    {
        "algo": "bubble sort",
        "items": 1000,
        "steps": 10,
        "start_time": 36458241,
        "end_time": 239759234,
        "total_time_ms": 3,
        "time_complexity": "O(n²)",
        "path_to_graph": "<base64_string>"
    }
    
    Returns: Success status with the saved record ID
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['algo', 'items', 'steps', 'start_time', 'end_time', 
                          'total_time_ms', 'time_complexity', 'path_to_graph']
        
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Create new AnalysisResults instance
        new_analysis = AnalysisResults(
            algorithm=data['algo'],
            items=data['items'],
            steps=data['steps'],
            start_time=data['start_time'],
            end_time=data['end_time'],
            total_time=data['total_time_ms'],
            time_complexity=data['time_complexity'],
            graph_image_path=data['path_to_graph']
        )
        
        # Save to database
        my_db.session.add(new_analysis)
        my_db.session.commit()
        
        # Return success response with the ID
        return jsonify({
            "status": "success",
            "message": "Analysis saved successfully",
            "id": new_analysis.id,
            "data": new_analysis.to_dict()
        }), 201
    
    except Exception as e:
        my_db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/retrieve_analysis', methods=['GET'])
def retrieve_analysis():
    """
    Endpoint 3: Retrieve saved analysis by ID
    
    Query Parameters:
        - id: The analysis ID to retrieve
    
    Example: /retrieve_analysis?id=5
    
    Returns: JSON with the same format as /analyze endpoint
    """
    try:
        # Get ID from query parameters
        analysis_id = request.args.get('id', type=int)
        
        if not analysis_id:
            return jsonify({"error": "Missing 'id' parameter"}), 400
        
        # Query database for the analysis
        analysis = AnalysisResults.query.get(analysis_id)
        
        if not analysis:
            return jsonify({"error": f"No analysis found with id: {analysis_id}"}), 404
        
        # Return the analysis data
        return jsonify(analysis.to_dict()), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API documentation"""
    return jsonify({
        "message": "Algorithm Complexity Analyzer API",
        "endpoints": {
            "/analyze": {
                "method": "GET",
                "description": "Analyze algorithm performance",
                "parameters": {
                    "algo": "Algorithm name (bubble, linear, binary, nested, exponential)",
                    "n": "Number of elements",
                    "steps": "Number of analysis steps"
                },
                "example": "/analyze?algo=bubble&n=1000&steps=10"
            },
            "/save_analysis": {
                "method": "POST",
                "description": "Save analysis results to database",
                "content_type": "application/json"
            },
            "/retrieve_analysis": {
                "method": "GET",
                "description": "Retrieve saved analysis by ID",
                "parameters": {
                    "id": "Analysis ID"
                },
                "example": "/retrieve_analysis?id=1"
            }
        }
    }), 200


if __name__ == '__main__':
    # Create all database tables
    with app.app_context():
        print("Starting Algorithm Complexity Analyzer API...")
        my_db.create_all()
        print("Database tables created!")
        print("Server running on http://0.0.0.0:8080")
    
    app.run(host="0.0.0.0", port=8080, debug=True)
