// Main application JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const taskForm = document.getElementById('taskForm');
    const taskDescription = document.getElementById('taskDescription');
    const submitBtn = document.getElementById('submitBtn');
    const clearBtn = document.getElementById('clearBtn');
    const loadingSection = document.getElementById('loadingSection');
    const resultsSection = document.getElementById('resultsSection');
    const errorSection = document.getElementById('errorSection');
    const analysisGrid = document.getElementById('analysisGrid');
    const recommendationsGrid = document.getElementById('recommendationsGrid');

    // Form submission handler
    taskForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const description = taskDescription.value.trim();
        if (!description) {
            showError('Please enter a task description');
            return;
        }

        // Show loading state
        showLoading();
        hideError();
        hideResults();

        try {
            const response = await fetch('/recommend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    task_description: description
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to get recommendations');
            }

            // Display results
            displayResults(data);
            
        } catch (error) {
            console.error('Error:', error);
            showError(error.message);
        } finally {
            hideLoading();
        }
    });

    // Clear button handler
    clearBtn.addEventListener('click', function() {
        taskDescription.value = '';
        hideResults();
        hideError();
        taskDescription.focus();
    });

    // Display results
    function displayResults(data) {
        const { recommendations, task_analysis } = data;
        
        // Display task analysis
        displayTaskAnalysis(task_analysis);
        
        // Display recommendations
        displayRecommendations(recommendations);
        
        // Show results section
        showResults();
        
        // Smooth scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    // Display task analysis
    function displayTaskAnalysis(analysis) {
        analysisGrid.innerHTML = '';
        
        const analysisItems = [
            { label: 'Complexity', value: analysis.complexity },
            { label: 'Word Count', value: analysis.word_count },
            { label: 'Languages', value: analysis.languages.length > 0 ? analysis.languages.join(', ') : 'Not specified' },
            { label: 'Domains', value: analysis.domains.length > 0 ? analysis.domains.join(', ') : 'General' },
            { label: 'Has Code Snippets', value: analysis.has_code_snippets ? 'Yes' : 'No' }
        ];

        analysisItems.forEach(item => {
            const analysisItem = document.createElement('div');
            analysisItem.className = 'analysis-item';
            analysisItem.innerHTML = `
                <div class="analysis-label">${item.label}</div>
                <div class="analysis-value">${item.value}</div>
            `;
            analysisGrid.appendChild(analysisItem);
        });

        // Add requirement scores if available
        if (analysis.requirements) {
            Object.entries(analysis.requirements).forEach(([requirement, score]) => {
                if (score > 0) {
                    const analysisItem = document.createElement('div');
                    analysisItem.className = 'analysis-item';
                    analysisItem.innerHTML = `
                        <div class="analysis-label">${requirement.replace('_', ' ').toUpperCase()}</div>
                        <div class="analysis-value">${Math.round(score * 100)}%</div>
                    `;
                    analysisGrid.appendChild(analysisItem);
                }
            });
        }
    }

    // Display recommendations
    function displayRecommendations(recommendations) {
        recommendationsGrid.innerHTML = '';
        
        recommendations.forEach((rec, index) => {
            const recommendationCard = document.createElement('div');
            recommendationCard.className = 'recommendation-card';
            
            const agent = rec.agent;
            const rank = rec.rank;
            const score = rec.score;
            const matchPercentage = rec.match_percentage;
            const justification = rec.justification;

            recommendationCard.innerHTML = `
                <div class="recommendation-header">
                    <div class="recommendation-info">
                        <h3>${agent.name}</h3>
                        <div class="recommendation-score">
                            <span class="score-badge">Score: ${score}</span>
                            <span class="match-percentage">${matchPercentage}% match</span>
                        </div>
                        <p>${agent.description}</p>
                    </div>
                    <div class="recommendation-rank">${rank}</div>
                </div>
                
                <div class="recommendation-justification">
                    <div class="justification-text">${justification}</div>
                </div>
                
                <div class="agent-details">
                    <div class="capabilities-preview">
                        <strong>Key Capabilities:</strong>
                        <div class="capabilities-tags">
                            ${agent.capabilities.slice(0, 3).map(cap => 
                                `<span class="capability-tag">${cap}</span>`
                            ).join('')}
                        </div>
                    </div>
                    
                    <div class="strengths-preview">
                        <strong>Strengths:</strong>
                        <ul>
                            ${agent.strengths.slice(0, 2).map(strength => 
                                `<li>${strength}</li>`
                            ).join('')}
                        </ul>
                    </div>
                </div>
            `;
            
            recommendationsGrid.appendChild(recommendationCard);
        });
    }

    // Show/hide functions
    function showLoading() {
        loadingSection.style.display = 'block';
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
    }

    function hideLoading() {
        loadingSection.style.display = 'none';
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-search"></i> Get Recommendations';
    }

    function showResults() {
        resultsSection.style.display = 'block';
    }

    function hideResults() {
        resultsSection.style.display = 'none';
    }

    function showError(message) {
        const errorMessage = document.getElementById('errorMessage');
        errorMessage.textContent = message;
        errorSection.style.display = 'block';
        hideLoading();
    }

    function hideError() {
        errorSection.style.display = 'none';
    }

    // Global function for error hiding (used in HTML)
    window.hideError = hideError;

    // Add some nice animations
    function addAnimations() {
        // Animate cards on scroll
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);

        // Observe all cards
        document.querySelectorAll('.card, .recommendation-card, .agent-card').forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(card);
        });
    }

    // Initialize animations
    addAnimations();

    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to submit
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            taskForm.dispatchEvent(new Event('submit'));
        }
        
        // Escape to clear
        if (e.key === 'Escape') {
            clearBtn.click();
        }
    });

    // Add character counter
    taskDescription.addEventListener('input', function() {
        const maxLength = 1000;
        const currentLength = this.value.length;
        const remaining = maxLength - currentLength;
        
        // Update placeholder or add counter if needed
        if (currentLength > maxLength * 0.8) {
            this.style.borderColor = remaining < 0 ? '#f56565' : '#ed8936';
        } else {
            this.style.borderColor = '#e2e8f0';
        }
    });

    // Focus on textarea when page loads
    taskDescription.focus();
}); 