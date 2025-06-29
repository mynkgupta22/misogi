// Main application JavaScript for Adaptive Prompt Optimizer

class PromptOptimizer {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.currentResult = null;
    }

    initializeElements() {
        // Form elements
        this.form = document.getElementById('promptForm');
        this.basePromptInput = document.getElementById('basePrompt');
        this.targetToolSelect = document.getElementById('targetTool');
        
        // Buttons
        this.submitBtn = document.getElementById('submitBtn');
        this.analyzeBtn = document.getElementById('analyzeBtn');
        this.clearBtn = document.getElementById('clearBtn');
        this.copyOptimizedBtn = document.getElementById('copyOptimizedBtn');
        
        // Sections
        this.loadingSection = document.getElementById('loadingSection');
        this.analysisSection = document.getElementById('analysisSection');
        this.resultsSection = document.getElementById('resultsSection');
        this.errorSection = document.getElementById('errorSection');
        
        // Result elements
        this.originalPrompt = document.getElementById('originalPrompt');
        this.optimizedPrompt = document.getElementById('optimizedPrompt');
        this.analysisGrid = document.getElementById('analysisGrid');
        this.explanationsGrid = document.getElementById('explanationsGrid');
        this.improvementScoreFill = document.getElementById('improvementScoreFill');
        this.improvementScoreText = document.getElementById('improvementScoreText');
        this.errorMessage = document.getElementById('errorMessage');
    }

    bindEvents() {
        // Form submission
        this.form.addEventListener('submit', (e) => this.handleOptimize(e));
        
        // Button clicks
        this.analyzeBtn.addEventListener('click', () => this.handleAnalyze());
        this.clearBtn.addEventListener('click', () => this.handleClear());
        this.copyOptimizedBtn.addEventListener('click', () => this.handleCopyOptimized());
        
        // Input validation
        this.basePromptInput.addEventListener('input', () => this.validateForm());
        this.targetToolSelect.addEventListener('change', () => this.validateForm());
    }

    validateForm() {
        const hasPrompt = this.basePromptInput.value.trim().length > 0;
        const hasTool = this.targetToolSelect.value.length > 0;
        
        this.submitBtn.disabled = !(hasPrompt && hasTool);
        this.analyzeBtn.disabled = !hasPrompt;
        
        return hasPrompt && hasTool;
    }

    async handleOptimize(e) {
        e.preventDefault();
        
        if (!this.validateForm()) {
            this.showError('Please fill in all required fields.');
            return;
        }

        const data = {
            base_prompt: this.basePromptInput.value.trim(),
            target_tool: this.targetToolSelect.value
        };

        await this.performOptimization(data);
    }

    async handleAnalyze() {
        if (!this.basePromptInput.value.trim()) {
            this.showError('Please enter a prompt to analyze.');
            return;
        }

        const data = {
            base_prompt: this.basePromptInput.value.trim()
        };

        await this.performAnalysis(data);
    }

    async performOptimization(data) {
        this.showLoading();
        this.hideError();
        this.hideResults();
        this.hideAnalysis();

        try {
            const response = await fetch('/optimize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                this.currentResult = result.optimization;
                this.displayResults(result.optimization);
            } else {
                this.showError(result.error || 'Failed to optimize prompt.');
            }
        } catch (error) {
            console.error('Optimization error:', error);
            this.showError('Network error. Please try again.');
        } finally {
            this.hideLoading();
        }
    }

    async performAnalysis(data) {
        this.showLoading();
        this.hideError();
        this.hideResults();
        this.hideAnalysis();

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (response.ok) {
                this.displayAnalysis(result.analysis);
            } else {
                this.showError(result.error || 'Failed to analyze prompt.');
            }
        } catch (error) {
            console.error('Analysis error:', error);
            this.showError('Network error. Please try again.');
        } finally {
            this.hideLoading();
        }
    }

    displayResults(optimization) {
        // Display original and optimized prompts
        this.originalPrompt.textContent = optimization.original_prompt;
        this.optimizedPrompt.textContent = optimization.optimized_prompt;

        // Display analysis
        this.displayAnalysis(optimization.analysis);

        // Display explanations
        this.displayExplanations(optimization.explanations);

        // Display improvement score
        this.displayImprovementScore(optimization.improvement_score);

        this.showResults();
    }

    displayAnalysis(analysis) {
        const analysisHTML = `
            <div class="analysis-item">
                <div class="analysis-label">Complexity</div>
                <div class="analysis-value">${this.capitalizeFirst(analysis.complexity)}</div>
            </div>
            <div class="analysis-item">
                <div class="analysis-label">Intent</div>
                <div class="analysis-value">${analysis.intent.join(', ')}</div>
            </div>
            <div class="analysis-item">
                <div class="analysis-label">Languages</div>
                <div class="analysis-value">${analysis.languages.length > 0 ? analysis.languages.join(', ') : 'Not specified'}</div>
            </div>
            <div class="analysis-item">
                <div class="analysis-label">Domains</div>
                <div class="analysis-value">${analysis.domains.length > 0 ? analysis.domains.join(', ') : 'General'}</div>
            </div>
            <div class="analysis-item">
                <div class="analysis-label">Word Count</div>
                <div class="analysis-value">${analysis.characteristics.word_count}</div>
            </div>
            <div class="analysis-item">
                <div class="analysis-label">Clarity Score</div>
                <div class="analysis-value">${(analysis.characteristics.clarity_score * 100).toFixed(0)}%</div>
            </div>
        `;

        this.analysisGrid.innerHTML = analysisHTML;
        this.showAnalysis();
    }

    displayExplanations(explanations) {
        if (!explanations || explanations.length === 0) {
            this.explanationsGrid.innerHTML = '<p>No specific optimizations were applied.</p>';
            return;
        }

        const explanationsHTML = explanations.map(explanation => `
            <div class="explanation-item">
                <div class="explanation-title">${explanation.title}</div>
                <div class="explanation-description">${explanation.description}</div>
            </div>
        `).join('');

        this.explanationsGrid.innerHTML = explanationsHTML;
    }

    displayImprovementScore(score) {
        const percentage = Math.round(score * 100);
        this.improvementScoreFill.style.width = `${percentage}%`;
        this.improvementScoreText.textContent = `${percentage}%`;
    }

    handleClear() {
        this.form.reset();
        this.hideResults();
        this.hideAnalysis();
        this.hideError();
        this.validateForm();
    }

    async handleCopyOptimized() {
        if (!this.currentResult) return;

        try {
            await navigator.clipboard.writeText(this.currentResult.optimized_prompt);
            this.showCopySuccess();
        } catch (error) {
            console.error('Copy failed:', error);
            this.showError('Failed to copy to clipboard.');
        }
    }

    showCopySuccess() {
        const originalText = this.copyOptimizedBtn.innerHTML;
        this.copyOptimizedBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
        this.copyOptimizedBtn.style.background = '#48bb78';
        
        setTimeout(() => {
            this.copyOptimizedBtn.innerHTML = originalText;
            this.copyOptimizedBtn.style.background = '';
        }, 2000);
    }

    // UI State Management
    showLoading() {
        this.loadingSection.style.display = 'block';
        this.submitBtn.disabled = true;
        this.analyzeBtn.disabled = true;
    }

    hideLoading() {
        this.loadingSection.style.display = 'none';
        this.validateForm();
    }

    showResults() {
        this.resultsSection.style.display = 'block';
        this.scrollToElement(this.resultsSection);
    }

    hideResults() {
        this.resultsSection.style.display = 'none';
    }

    showAnalysis() {
        this.analysisSection.style.display = 'block';
        this.scrollToElement(this.analysisSection);
    }

    hideAnalysis() {
        this.analysisSection.style.display = 'none';
    }

    showError(message) {
        this.errorMessage.textContent = message;
        this.errorSection.style.display = 'block';
        this.scrollToElement(this.errorSection);
    }

    hideError() {
        this.errorSection.style.display = 'none';
    }

    scrollToElement(element) {
        element.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });
    }

    // Utility functions
    capitalizeFirst(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }
}

// Global function for error handling
function hideError() {
    const errorSection = document.getElementById('errorSection');
    if (errorSection) {
        errorSection.style.display = 'none';
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new PromptOptimizer();
});

// Add some example prompts for quick testing
const examplePrompts = [
    "Create a function to sort a list of numbers",
    "Build a REST API for user authentication",
    "Write a simple calculator app",
    "Create a web scraper for collecting data",
    "Build a machine learning model for classification",
    "Create a mobile app for task management"
];

// Add example prompts to the textarea placeholder rotation
let currentExampleIndex = 0;
const textarea = document.getElementById('basePrompt');

if (textarea) {
    setInterval(() => {
        currentExampleIndex = (currentExampleIndex + 1) % examplePrompts.length;
        textarea.placeholder = `Describe what you want to create. For example: "${examplePrompts[currentExampleIndex]}"`;
    }, 5000);
} 