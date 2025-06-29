// Agents page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const searchBtn = document.getElementById('searchBtn');
    const agentsGrid = document.getElementById('agentsGrid');
    const noResults = document.getElementById('noResults');
    
    let allAgents = [];
    let filteredAgents = [];

    // Load all agents on page load
    loadAllAgents();

    // Search functionality
    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });

    // Real-time search (optional)
    searchInput.addEventListener('input', function() {
        if (this.value.length >= 3) {
            performSearch();
        } else if (this.value.length === 0) {
            showAllAgents();
        }
    });

    async function loadAllAgents() {
        try {
            const response = await fetch('/api/agents');
            const agents = await response.json();
            allAgents = agents;
            filteredAgents = agents;
            renderAgents(agents);
        } catch (error) {
            console.error('Error loading agents:', error);
            showError('Failed to load agents. Please refresh the page.');
        }
    }

    function performSearch() {
        const query = searchInput.value.trim().toLowerCase();
        
        if (!query) {
            showAllAgents();
            return;
        }

        const results = allAgents.filter(agent => {
            // Search in name
            if (agent.name.toLowerCase().includes(query)) return true;
            
            // Search in description
            if (agent.description.toLowerCase().includes(query)) return true;
            
            // Search in capabilities
            if (agent.capabilities.some(cap => cap.toLowerCase().includes(query))) return true;
            
            // Search in strengths
            if (agent.strengths.some(strength => strength.toLowerCase().includes(query))) return true;
            
            // Search in weaknesses
            if (agent.weaknesses.some(weakness => weakness.toLowerCase().includes(query))) return true;
            
            // Search in best_for
            if (agent.best_for.some(useCase => useCase.toLowerCase().includes(query))) return true;
            
            return false;
        });

        filteredAgents = results;
        renderAgents(results);
        
        if (results.length === 0) {
            showNoResults();
        } else {
            hideNoResults();
        }
    }

    function showAllAgents() {
        filteredAgents = allAgents;
        renderAgents(allAgents);
        hideNoResults();
    }

    function renderAgents(agents) {
        agentsGrid.innerHTML = '';
        
        agents.forEach(agent => {
            const agentCard = createAgentCard(agent);
            agentsGrid.appendChild(agentCard);
        });
    }

    function createAgentCard(agent) {
        const card = document.createElement('div');
        card.className = 'agent-card';
        card.setAttribute('data-agent-id', agent.id);
        
        card.innerHTML = `
            <div class="agent-header">
                <h3 class="agent-name">${agent.name}</h3>
                <div class="agent-badge">
                    <i class="fas fa-robot"></i>
                </div>
            </div>
            
            <p class="agent-description">${agent.description}</p>
            
            <div class="agent-capabilities">
                <h4>Capabilities</h4>
                <div class="capabilities-list">
                    ${agent.capabilities.map(cap => `<span class="capability-tag">${cap}</span>`).join('')}
                </div>
            </div>
            
            <div class="agent-strengths">
                <h4>Strengths</h4>
                <ul class="strengths-list">
                    ${agent.strengths.map(strength => `<li><i class="fas fa-check"></i> ${strength}</li>`).join('')}
                </ul>
            </div>
            
            <div class="agent-weaknesses">
                <h4>Weaknesses</h4>
                <ul class="weaknesses-list">
                    ${agent.weaknesses.map(weakness => `<li><i class="fas fa-times"></i> ${weakness}</li>`).join('')}
                </ul>
            </div>
            
            <div class="agent-best-for">
                <h4>Best For</h4>
                <div class="best-for-tags">
                    ${agent.best_for.map(useCase => `<span class="use-case-tag">${useCase}</span>`).join('')}
                </div>
            </div>
            
            <div class="agent-scores">
                <h4>Capability Scores</h4>
                <div class="scores-grid">
                    ${Object.entries(agent.score_weights).map(([capability, score]) => `
                        <div class="score-item">
                            <span class="score-label">${capability.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}</span>
                            <div class="score-bar">
                                <div class="score-fill" style="width: ${score * 100}%"></div>
                            </div>
                            <span class="score-value">${Math.round(score * 100)}%</span>
                        </div>
                    `).join('')}
                </div>
            </div>
            
            <div class="agent-system-prompt">
                <h4>System Prompt</h4>
                <div class="prompt-content">
                    <p>${agent.system_prompt}</p>
                </div>
            </div>
        `;
        
        return card;
    }

    function showNoResults() {
        noResults.style.display = 'block';
        agentsGrid.style.display = 'none';
    }

    function hideNoResults() {
        noResults.style.display = 'none';
        agentsGrid.style.display = 'grid';
    }

    function showError(message) {
        // Create a simple error notification
        const errorDiv = document.createElement('div');
        errorDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #f56565;
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 1000;
            max-width: 300px;
        `;
        errorDiv.textContent = message;
        
        document.body.appendChild(errorDiv);
        
        // Remove after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 5000);
    }

    // Global function for clearing search (used in HTML)
    window.clearSearch = function() {
        searchInput.value = '';
        showAllAgents();
        searchInput.focus();
    };

    // Add animations
    function addAnimations() {
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

        // Observe all agent cards
        document.querySelectorAll('.agent-card').forEach(card => {
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
        // Ctrl/Cmd + F to focus search
        if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
            e.preventDefault();
            searchInput.focus();
        }
        
        // Escape to clear search
        if (e.key === 'Escape') {
            clearSearch();
        }
    });

    // Add search suggestions (optional)
    function addSearchSuggestions() {
        const suggestions = [
            'Python', 'JavaScript', 'Web Development', 'Mobile Development',
            'Code Completion', 'Debugging', 'Testing', 'AWS', 'Cloud',
            'Real-time', 'IDE Integration', 'Complex Problem Solving'
        ];

        const datalist = document.createElement('datalist');
        datalist.id = 'search-suggestions';
        
        suggestions.forEach(suggestion => {
            const option = document.createElement('option');
            option.value = suggestion;
            datalist.appendChild(option);
        });

        searchInput.setAttribute('list', 'search-suggestions');
        document.body.appendChild(datalist);
    }

    // Initialize search suggestions
    addSearchSuggestions();

    // Add filter by capability (optional feature)
    function addCapabilityFilters() {
        const capabilities = new Set();
        allAgents.forEach(agent => {
            agent.capabilities.forEach(cap => capabilities.add(cap));
        });

        const filterContainer = document.createElement('div');
        filterContainer.className = 'capability-filters';
        filterContainer.style.cssText = `
            margin-bottom: 20px;
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        `;

        capabilities.forEach(capability => {
            const filterBtn = document.createElement('button');
            filterBtn.className = 'filter-btn';
            filterBtn.textContent = capability;
            filterBtn.style.cssText = `
                padding: 8px 16px;
                border: 2px solid #e2e8f0;
                background: white;
                border-radius: 20px;
                cursor: pointer;
                transition: all 0.3s ease;
                font-size: 0.9rem;
            `;

            filterBtn.addEventListener('click', function() {
                const isActive = this.classList.contains('active');
                
                // Toggle active state
                document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
                if (!isActive) {
                    this.classList.add('active');
                    this.style.background = '#667eea';
                    this.style.color = 'white';
                    this.style.borderColor = '#667eea';
                }

                // Filter agents
                const activeFilters = Array.from(document.querySelectorAll('.filter-btn.active'))
                    .map(btn => btn.textContent);

                if (activeFilters.length === 0) {
                    showAllAgents();
                } else {
                    const filtered = allAgents.filter(agent => 
                        activeFilters.some(filter => 
                            agent.capabilities.includes(filter)
                        )
                    );
                    renderAgents(filtered);
                }
            });

            filterContainer.appendChild(filterBtn);
        });

        // Insert before agents grid
        agentsGrid.parentNode.insertBefore(filterContainer, agentsGrid);
    }

    // Initialize capability filters after agents are loaded
    setTimeout(addCapabilityFilters, 100);
}); 