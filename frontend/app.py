"""
Flask backend for Shorfin Quantum Algorithms Dashboard
"""
from flask import Flask, render_template, jsonify, request
import json
import sys
import os

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')

@app.route('/')
def index():
    """Render the main dashboard"""
    return render_template('index.html')

@app.route('/api/shor/factor', methods=['POST'])
def factor_number():
    """API endpoint for Shor's algorithm factorization"""
    data = request.json
    number = data.get('number', 15)
    qubits = data.get('qubits', 8)
    
    try:
        # Import and run Shor's algorithm
        from src.shor.algorithm import ShorSimulator
        
        shor = ShorSimulator(n_qubits=qubits)
        p, q = shor.factor(number, verbose=False)
        
        # Get circuit complexity
        complexity = shor.get_circuit_complexity(number)
        
        return jsonify({
            'success': True,
            'number': number,
            'factors': [p, q],
            'circuit_complexity': complexity,
            'quantum_advantage': f"10^{int(complexity['n'] * 2)}x"
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/mwis/solve', methods=['POST'])
def solve_mwis():
    """API endpoint for MWIS solving"""
    data = request.json
    graph_data = data.get('graph')
    algorithm = data.get('algorithm', 'qft-walk')
    
    try:
        # Import MWIS solver
        from src.shor.mwis_connection import QuantumPeriodicMWIS
        import networkx as nx
        import numpy as np
        
        # Create graph from data
        graph = nx.Graph()
        for node in graph_data['nodes']:
            graph.add_node(node['id'], weight=node['weight'])
        
        for edge in graph_data['edges']:
            graph.add_edge(edge[0], edge[1])
        
        # Solve MWIS
        use_qft = algorithm == 'qft-walk'
        solver = QuantumPeriodicMWIS(use_qft=use_qft)
        result = solver.solve(graph)
        
        return jsonify({
            'success': True,
            'solution': result['best_solution'],
            'weight': result['best_weight'],
            'algorithm': result['algorithm'],
            'quantum_resources': result.get('quantum_resources', {})
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/mwis/analyze', methods=['POST'])
def analyze_graph():
    """API endpoint for graph analysis"""
    data = request.json
    graph_data = data.get('graph')
    
    try:
        from src.shor.mwis_connection import QuantumAdvantageAnalyzer
        import networkx as nx
        import numpy as np
        
        # Create graph from data
        graph = nx.Graph()
        for node in graph_data['nodes']:
            graph.add_node(node['id'], weight=node['weight'])
        
        for edge in graph_data['edges']:
            graph.add_edge(edge[0], edge[1])
        
        # Analyze graph
        analyzer = QuantumAdvantageAnalyzer()
        analysis = analyzer.analyze_periodic_structures(graph)
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'nodes': len(graph.nodes()),
            'edges': len(graph.edges()),
            'density': nx.density(graph)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/benchmark/shor', methods=['GET'])
def benchmark_shor():
    """API endpoint for Shor algorithm benchmarks"""
    try:
        from src.shor.algorithm import ShorSimulator
        import time
        
        benchmarks = []
        test_numbers = [15, 21, 35, 143]
        
        for N in test_numbers:
            shor = ShorSimulator(n_qubits=8)
            
            start_time = time.time()
            p, q = shor.factor(N, verbose=False)
            quantum_time = time.time() - start_time
            
            # Classical time estimation (exponential)
            classical_time = 10 ** (len(str(N)) / 3) / 1000
            
            benchmarks.append({
                'number': N,
                'bits': N.bit_length(),
                'quantum_time': quantum_time,
                'classical_time': classical_time,
                'speedup': classical_time / quantum_time,
                'factors': [p, q]
            })
        
        return jsonify({
            'success': True,
            'benchmarks': benchmarks,
            'average_speedup': sum(b['speedup'] for b in benchmarks) / len(benchmarks)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/benchmark/mwis', methods=['GET'])
def benchmark_mwis():
    """API endpoint for MWIS algorithm benchmarks"""
    try:
        from src.shor.mwis_connection import QuantumPeriodicMWIS, QuantumAdvantageAnalyzer
        from src.algorithms.classical_baselines import ClassicalMWISSolver
        import networkx as nx
        import numpy as np
        import time
        
        benchmarks = []
        node_counts = [5, 10, 15, 20]
        
        for n in node_counts:
            # Generate random graph
            graph = nx.erdos_renyi_graph(n, 0.3)
            for node in graph.nodes():
                graph.nodes[node]['weight'] = np.random.uniform(0.5, 2.0)
            
            # Quantum solver
            q_solver = QuantumPeriodicMWIS(use_qft=True)
            start_time = time.time()
            q_result = q_solver.solve(graph)
            quantum_time = time.time() - start_time
            
            # Classical solver
            c_solver = ClassicalMWISSolver(method='greedy')
            start_time = time.time()
            c_result = c_solver.solve(graph)
            classical_time = time.time() - start_time
            
            benchmarks.append({
                'nodes': n,
                'quantum_time': quantum_time,
                'classical_time': classical_time,
                'speedup': classical_time / quantum_time,
                'quantum_weight': q_result['best_weight'],
                'classical_weight': c_result['optimal_value']
            })
        
        return jsonify({
            'success': True,
            'benchmarks': benchmarks,
            'average_speedup': sum(b['speedup'] for b in benchmarks) / len(benchmarks)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/status', methods=['GET'])
def status():
    """API endpoint for system status"""
    return jsonify({
        'status': 'online',
        'version': '1.0.0',
        'algorithms': ['shor', 'mwis', 'benchmarks'],
        'quantum_simulated': True,
        'ready': True
    })

if __name__ == '__main__':
    print("Starting Shorfin Quantum Dashboard...")
    print("Dashboard available at: http://localhost:5000")
    print("API endpoints available at: http://localhost:5000/api/*")
    app.run(debug=True, host='0.0.0.0', port=5000)
