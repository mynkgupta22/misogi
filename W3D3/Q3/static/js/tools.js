// JavaScript for the Tools page

class ToolsPage {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.setupAnimations();
    }

    initializeElements() {
        this.toolsGrid = document.getElementById('toolsGrid');
        this.toolCards = document.querySelectorAll('.tool-card');
    }

    bindEvents() {
        // Add click handlers for tool cards
        this.toolCards.forEach(card => {
            card.addEventListener('click', () => this.handleCardClick(card));
        });

        // Add hover effects
        this.toolCards.forEach(card => {
            card.addEventListener('mouseenter', () => this.handleCardHover(card, true));
            card.addEventListener('mouseleave', () => this.handleCardHover(card, false));
        });
    }

    setupAnimations() {
        // Animate tool cards on page load
        this.toolCards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 100);
        });

        // Add scroll animations
        this.setupScrollAnimations();
    }

    setupScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, observerOptions);

        // Observe all tool cards
        this.toolCards.forEach(card => {
            observer.observe(card);
        });
    }

    handleCardClick(card) {
        // Add click animation
        card.style.transform = 'scale(0.98)';
        setTimeout(() => {
            card.style.transform = '';
        }, 150);

        // Toggle detailed view (optional feature)
        this.toggleCardDetails(card);
    }

    handleCardHover(card, isHovering) {
        if (isHovering) {
            card.style.transform = 'translateY(-8px) scale(1.02)';
            card.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.15)';
        } else {
            card.style.transform = 'translateY(0) scale(1)';
            card.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.08)';
        }
    }

    toggleCardDetails(card) {
        const details = card.querySelector('.tool-details');
        if (details) {
            details.classList.toggle('expanded');
        }
    }

    // Search functionality (if needed)
    setupSearch() {
        const searchInput = document.createElement('input');
        searchInput.type = 'text';
        searchInput.placeholder = 'Search tools...';
        searchInput.className = 'tools-search';
        
        searchInput.addEventListener('input', (e) => {
            this.filterTools(e.target.value);
        });

        // Insert search before tools grid
        if (this.toolsGrid && this.toolsGrid.parentNode) {
            this.toolsGrid.parentNode.insertBefore(searchInput, this.toolsGrid);
        }
    }

    filterTools(searchTerm) {
        const term = searchTerm.toLowerCase();
        
        this.toolCards.forEach(card => {
            const toolName = card.querySelector('.tool-name').textContent.toLowerCase();
            const toolDescription = card.querySelector('.tool-description').textContent.toLowerCase();
            const capabilities = Array.from(card.querySelectorAll('.capability-tag'))
                .map(tag => tag.textContent.toLowerCase())
                .join(' ');

            const matches = toolName.includes(term) || 
                           toolDescription.includes(term) || 
                           capabilities.includes(term);

            if (matches) {
                card.style.display = 'block';
                card.style.opacity = '1';
            } else {
                card.style.opacity = '0.3';
                card.style.transform = 'scale(0.95)';
            }
        });
    }

    // Add smooth scrolling for anchor links
    setupSmoothScrolling() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    // Add copy functionality for code examples
    setupCopyButtons() {
        const copyButtons = document.querySelectorAll('.copy-example');
        copyButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.stopPropagation();
                const exampleText = button.closest('.example-container').textContent;
                this.copyToClipboard(exampleText);
                this.showCopySuccess(button);
            });
        });
    }

    async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
        } catch (error) {
            console.error('Copy failed:', error);
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
        }
    }

    showCopySuccess(button) {
        const originalText = button.textContent;
        button.textContent = 'Copied!';
        button.style.background = '#48bb78';
        
        setTimeout(() => {
            button.textContent = originalText;
            button.style.background = '';
        }, 2000);
    }
}

// Initialize the tools page when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const toolsPage = new ToolsPage();
    
    // Add search functionality if needed
    // toolsPage.setupSearch();
    
    // Setup smooth scrolling
    toolsPage.setupSmoothScrolling();
    
    // Setup copy buttons
    toolsPage.setupCopyButtons();
});

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
    .tool-card {
        transition: all 0.3s ease;
    }
    
    .tool-card.animate-in {
        animation: slideInUp 0.6s ease forwards;
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .tools-search {
        width: 100%;
        max-width: 400px;
        padding: 12px 16px;
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        font-size: 1rem;
        margin-bottom: 20px;
        transition: border-color 0.3s ease;
    }
    
    .tools-search:focus {
        outline: none;
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .copy-example {
        background: #667eea;
        color: white;
        border: none;
        padding: 6px 12px;
        border-radius: 4px;
        font-size: 0.8rem;
        cursor: pointer;
        transition: background 0.3s ease;
    }
    
    .copy-example:hover {
        background: #5a67d8;
    }
    
    .tool-details {
        max-height: 0;
        overflow: hidden;
        transition: max-height 0.3s ease;
    }
    
    .tool-details.expanded {
        max-height: 500px;
    }
`;
document.head.appendChild(style); 