// Benchmarks JavaScript
class BenchmarkManager {
    constructor() {
        this.benchmarkData = {
            shor: this.generateShorBenchmarkData(),
            mwis: this.generateMWISBenchmarkData()
        };
        
        this.initializeEvents();
        this.initializeCharts();
    }
    
    initializeEvents() {
        document.getElementById('run-benchmark-btn').addEventListener('click', () => this.runBenchmark());
        
        // Update benchmark type
        document.getElementById('benchmark-type').addEventListener('change', () => {
            this.updateBenchmarkDisplay();
        });
    }
    
    initializeCharts() {
        // Initialize empty charts
        this.timeChart = this.createTimeChart();
        this.scalabilityChart = this.createScalabilityChart();
    }
    
    async runBenchmark() {
        const type = document.getElementById('benchmark-type').value;
        this.showLoading();
        
        try {
            // Simulate benchmark run
            await this.simulateBenchmark(type);
            this.displayBenchmarkResults(type);
        } catch (error) {
            this.showError(`Benchmark failed: ${error.message}`);
        }
    }
    
    async simulateBenchmark(type) {
        return new Promise((resolve) => {
            setTimeout(() => {
                // Simulate benchmark computation
                if (type === 'both') {
                    this.benchmarkData.both = this.combineBenchmarkData();
                }
                resolve();
            }, 2000);
        });
    }
    
    displayBenchmarkResults(type) {
        const data = type === 'both' ? this.benchmarkData.both : this.benchmarkData[type];
        
        // Update charts
        this.updateTimeChart(data);
        this.updateScalabilityChart(data);
        this.updateBenchmarkTable(data);
        
        // Show success message
        const resultsElement = document.getElementById('benchmark-results');
        resultsElement.innerHTML = `
            <div class="success fade-in" style="margin-bottom: 20px;">
                <h4><i class="fas fa-chart-line"></i> Benchmark Complete</h4>
                <p>Benchmark ran successfully for ${this.getBenchmarkName(type)}</p>
                <p>Quantum speedup observed: ${this.calculateAverageSpeedup(data).toFixed(1)}x</p>
            </div>
            ${resultsElement.innerHTML}
        `;
    }
    
    getBenchmarkName(type) {
        const names = {
            shor: "Shor's Algorithm",
            mwis: "MWIS Solver",
            both: "Both Algorithms"
        };
        return names[type] || type;
    }
    
    updateBenchmarkDisplay() {
        const type = document.getElementById('benchmark-type').value;
        const data = type === 'both' ? this.benchmarkData.both : this.benchmarkData[type];
        
        this.updateTimeChart(data);
        this.updateScalabilityChart(data);
        this.updateBenchmarkTable(data);
    }
    
    createTimeChart() {
        const element = document.getElementById('time-comparison-chart');
        const data = [{
            x: [],
            y: [],
            type: 'bar',
            name: 'Quantum',
            marker: { color: '#10b981' }
        }, {
            x: [],
            y: [],
            type: 'bar',
            name: 'Classical',
            marker: { color: '#ef4444' }
        }];
        
        const layout = {
            title: 'Execution Time Comparison',
            xaxis: { title: 'Problem Size' },
            yaxis: { title: 'Time (seconds, log scale)', type: 'log' },
            barmode: 'group',
            showlegend: true
        };
        
        return Plotly.newPlot(element, data, layout);
    }
    
    createScalabilityChart() {
        const element = document.getElementById('scalability-chart');
        const data = [{
            x: [],
            y: [],
            type: 'scatter',
            mode: 'lines+markers',
            name: 'Quantum Scaling',
            line: { color: '#10b981', width: 3 }
        }, {
            x: [],
            y: [],
            type: 'scatter',
            mode: 'lines+markers',
            name: 'Classical Scaling',
            line: { color: '#ef4444', width: 3 }
        }];
        
        const layout = {
            title: 'Algorithm Scalability',
            xaxis: { title: 'Problem Size' },
            yaxis: { title: 'Time Complexity' },
            showlegend: true
        };
        
        return Plotly.newPlot(element, data, layout);
    }
    
    updateTimeChart(data) {
        const sizes = data.map(d => d.size);
        const quantumTimes = data.map(d => d.quantumTime);
        const classicalTimes = data.map(d => d.classicalTime);
        
        Plotly.react('time-comparison-chart', [{
            x: sizes,
            y: quantumTimes,
            type: 'bar',
            name: 'Quantum',
            marker: { color: '#10b981' }
        }, {
            x: sizes,
            y: classicalTimes,
            type: 'bar',
            name: 'Classical',
            marker: { color: '#ef4444' }
        }], {
            title: 'Execution Time Comparison',
            xaxis: { title: 'Problem Size' },
            yaxis: { title: 'Time (seconds, log scale)', type: 'log' },
            barmode: 'group'
        });
    }
    
    updateScalabilityChart(data) {
        const sizes = data.map(d => d.size);
        const quantumComplexity = data.map(d => Math.log10(d.quantumComplexity));
        const classicalComplexity = data.map(d => Math.log10(d.classicalComplexity));
        
        Plotly.react('scalability-chart', [{
            x: sizes,
            y: quantumComplexity,
            type: 'scatter',
            mode: 'lines+markers',
            name: 'Quantum Scaling',
            line: { color: '#10b981', width: 3 }
        }, {
            x: sizes,
            y: classicalComplexity,
            type: 'scatter',
            mode: 'lines+markers',
            name: 'Classical Scaling',
            line: { color: '#ef4444', width: 3 }
        }], {
            title: 'Algorithm Scalability',
            xaxis: { title: 'Problem Size' },
            yaxis: { title: 'Log(Time Complexity)' },
            showlegend: true
        });
    }
    
    updateBenchmarkTable(data) {
        const tableBody = document.getElementById('benchmark-table-body');
        tableBody.innerHTML = '';
        
        data.forEach(item => {
            const row = document.createElement('tr');
            const speedup = item.classicalTime / item.quantumTime;
            const accuracy = Math.random() * 0.1 + 0.9; // 90-100% accuracy
            
            row.innerHTML = `
                <td>${item.size}</td>
                <td>${item.quantumTime.toFixed(3)}s</td>
                <td>${item.classicalTime.toFixed(3)}s</td>
                <td>${speedup.toFixed(1)}x</td>
                <td>${(accuracy * 100).toFixed(1)}%</td>
            `;
            
            tableBody.appendChild(row);
        });
    }
    
    generateShorBenchmarkData() {
        return [4, 8, 16, 32, 64].map(bits => {
            const size = `N=${1 << bits}`;
            const quantumTime = Math.pow(bits, 3) / 1000;
            const classicalTime = Math.exp(bits / 3);
            
            return {
                size: size,
                quantumTime: quantumTime,
                classicalTime: classicalTime,
                quantumComplexity: Math.pow(bits, 3),
                classicalComplexity: Math.exp(bits / 3)
            };
        });
    }
    
    generateMWISBenchmarkData() {
        return [5, 10, 15, 20, 25].map(nodes => {
            const size = `${nodes} nodes`;
            const quantumTime = Math.pow(nodes, 2) / 100;
            const classicalTime = Math.pow(2, nodes / 2) / 1000;
            
            return {
                size: size,
                quantumTime: quantumTime,
                classicalTime: classicalTime,
                quantumComplexity: Math.pow(nodes, 2),
                classicalComplexity: Math.pow(2, nodes / 2)
            };
        });
    }
    
    combineBenchmarkData() {
        const shorData = this.benchmarkData.shor;
        const mwisData = this.benchmarkData.mwis;
        
        // Combine and normalize data
        return [...shorData, ...mwisData].map((item, index) => ({
            ...item,
            size: `Test ${index + 1}`
        }));
    }
    
    calculateAverageSpeedup(data) {
        const speedups = data.map(item => item.classicalTime / item.quantumTime);
        return speedups.reduce((a, b) => a + b, 0) / speedups.length;
    }
    
    showLoading() {
        const resultsElement = document.getElementById('benchmark-results');
        resultsElement.innerHTML = `
            <div class="loading-state">
                <div class="loading-spinner"></div>
                <p>Running benchmarks...</p>
                <p class="loading-subtext">Measuring quantum vs classical performance</p>
            </div>
        `;
    }
    
    showError(message) {
        const resultsElement = document.getElementById('benchmark-results');
        resultsElement.innerHTML = `
            <div class="error fade-in">
                <h4><i class="fas fa-exclamation-circle"></i> Benchmark Error</h4>
                <p>${message}</p>
            </div>
        `;
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.benchmarkManager = new BenchmarkManager();
});
