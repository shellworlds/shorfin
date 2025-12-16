#!/usr/bin/env python3
"""Test Shor's algorithm locally"""
import sys
import os

# Add src to path
sys.path.append('src')

try:
    from shor.algorithm import ShorSimulator
    print("✅ Import successful")
    
    # Test
    shor = ShorSimulator(n_qubits=8)
    numbers = [15, 21, 35, 143]
    
    for N in numbers:
        print(f"\nFactoring N = {N}:")
        print("-" * 30)
        
        import time
        start = time.time()
        p, q = shor.factor(N, verbose=True)
        elapsed = time.time() - start
        
        print(f"Result: {p} × {q} = {N}")
        print(f"Time: {elapsed:.3f} seconds")
        
        # Verify
        if p * q == N:
            print("✅ Verification passed!")
        else:
            print("⚠️ Verification failed")
            
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
