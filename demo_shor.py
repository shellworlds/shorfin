#!/usr/bin/env python3
"""
Demo script for Shor's algorithm and MWIS quantum advantage
"""
import sys
sys.path.append('src')

from shor.algorithm import ShorSimulator
from shor.mwis_connection import QuantumPeriodicMWIS
import networkx as nx
import numpy as np

def main():
    print("Shorfin Repository - Quantum Algorithms Demo")
    print("=" * 60)
    
    # Part 1: Shor's Algorithm
    print("\n1. SHOR'S ALGORITHM DEMONSTRATION")
    print("-" * 40)
    
    shor = ShorSimulator()
    
    # Factor some numbers
    test_numbers = [15, 21, 35]
    for N in test_numbers:
        print(f"\nFactoring N = {N}:")
        p, q = shor.factor(N, verbose=False)
        print(f"  Result: {p} × {q} = {N}")
    
    # Part 2: Quantum Advantage for MWIS
    print("\n\n2. QUANTUM ADVANTAGE FOR MWIS")
    print("-" * 40)
    
    # Create a graph with periodic structure
    graph = nx.random_regular_graph(3, 12)
    for node in graph.nodes():
        graph.nodes[node]['weight'] = np.random.uniform(0.5, 2.0)
    
    print(f"\nGraph with {len(graph.nodes())} nodes, {len(graph.edges())} edges")
    print(f"Average degree: {sum(d for _, d in graph.degree()) / len(graph.nodes()):.2f}")
    
    # Solve with quantum approaches
    solver = QuantumPeriodicMWIS(use_qft=True)
    result = solver.solve(graph)
    
    print(f"\nQuantum Solution:")
    print(f"  Algorithm: {result['algorithm']}")
    print(f"  Best weight: {result['best_weight']:.2f}")
    print(f"  Quantum resources: {result['quantum_resources']['qubits']} qubits")
    
    # Part 3: Circuit Complexity
    print("\n\n3. QUANTUM CIRCUIT COMPLEXITY")
    print("-" * 40)
    
    complexity = shor.get_circuit_complexity(2047)  # 11-bit number
    print("\nFor factoring 2047 (11-bit RSA number):")
    print(f"  Total qubits needed: {complexity['total_qubits']}")
    print(f"  Gate count estimate: {complexity['gate_count_estimate']:,}")
    print(f"  Time complexity: {complexity['time_complexity']}")
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("For interactive examples, run: jupyter notebook notebooks/shor_demo.ipynb")
    print("Or open in Colab: https://colab.research.google.com/github/shellworlds/shorfin/blob/main/notebooks/shor_demo.ipynb")

if __name__ == "__main__":
    main()
