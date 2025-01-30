// Project data
const projectsData = {
    "projects": [
        {
            "name": "Todo",
            "description": "A full-stack Todo app built using the MERN stack. Features include task creation, updates, and deletion. The app is containerized using Docker and includes CI/CD pipelines powered by Semaphore and GitHub Actions for seamless deployments.",
            "icon": "fa-tasks",
            "tools": [
                "MERN Stack",
                "Docker",
                "Semaphore CI",
                "GitHub Actions"
            ],
            "docUrl": "https://docs.todo-app.com",
            "githubUrl": "https://github.com/yourusername/todo-app"
        },
        {
            "name": "TaskFlow",
            "description": "A task management system leveraging AWS Serverless architecture. The backend is built with Lambda Functions, Cognito for user authentication, SES for email notifications, and API Gateway. The system is deployed via Amplify, with CI/CD pipelines implemented using GitHub Actions.",
            "icon": "fa-cloud",
            "tools": [
                "AWS Serverless",
                "Lambda",
                "Cognito",
                "API Gateway",
                "Amplify"
            ],
            "docUrl": "https://docs.taskflow.com",
            "githubUrl": "https://github.com/yourusername/taskflow"
        },
        {
            "name": "Kubernetes Monitoring Stack",
            "description": "Automated deployment of Prometheus and Grafana for comprehensive cluster monitoring. Includes custom dashboards and alerting rules.",
            "icon": "fa-kubernetes",
            "tools": [
                "Kubernetes",
                "Prometheus",
                "Grafana"
            ],
            "docUrl": "https://docs.k8s-monitoring.com",
            "githubUrl": "https://github.com/yourusername/k8s-monitoring"
        },
        {
            "name": "Container Orchestration",
            "description": "Docker Compose and Kubernetes configurations for a microservices architecture. Features auto-scaling and load balancing.",
            "icon": "fa-docker",
            "tools": [
                "Docker",
                "Kubernetes",
                "Helm"
            ],
            "docUrl": "https://docs.container-orch.com",
            "githubUrl": "https://github.com/yourusername/container-orchestration"
        }
    ]
};

// Function to create a project card
const createProjectCard = (project) => {
    return `
        <article class="project-card">
            <div class="project-icon">
                <i class="fas ${project.icon}"></i>
            </div>
            <div class="project-content">
                <h2>${project.name}</h2>
                <p>${project.description}</p>
                <div class="tech-stack">
                    ${project.tools.map(tool => `<span>${tool}</span>`).join('')}
                </div>
                <div class="project-actions">
                    <a href="${project.docUrl}" class="btn primary" data-tooltip="View detailed documentation">
                        <i class="fas fa-book"></i> View Documentation
                    </a>
                    <a href="${project.githubUrl}" class="btn secondary" target="_blank">
                        <i class="fab fa-github"></i> Source
                    </a>
                </div>
            </div>
        </article>
    `;
};

// Function to load and render projects
const loadProjects = async () => {
    const container = document.getElementById('projects-container');
    
    try {
        // Use the embedded project data directly
        container.innerHTML = projectsData.projects.map(project => createProjectCard(project)).join('');
        
        // Initialize animations after loading projects
        observeProjectCards();
        addTechStackHoverEffect();
    } catch (error) {
        console.error('Error loading projects:', error);
        container.innerHTML = `
            <div class="error-message">
                <i class="fas fa-exclamation-triangle"></i>
                <p>Failed to load projects. Please try again later.</p>
                <p class="error-details">${error.message}</p>
            </div>
        `;
    }
};

// Add smooth reveal animation for project cards
const observeProjectCards = () => {
    const cards = document.querySelectorAll('.project-card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1
    });
    
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(card);
    });
};

// Add hover effect for tech stack tags
const addTechStackHoverEffect = () => {
    const tags = document.querySelectorAll('.tech-stack span');
    
    tags.forEach(tag => {
        tag.addEventListener('mouseover', () => {
            tag.style.transform = 'scale(1.1)';
            tag.style.transition = 'transform 0.3s ease';
        });
        
        tag.addEventListener('mouseout', () => {
            tag.style.transform = 'scale(1)';
        });
    });
};

// Add error styling
const style = document.createElement('style');
style.textContent = `
    .error-message {
        text-align: center;
        padding: 2rem;
        color: var(--secondary-color);
    }
    .error-message i {
        font-size: 3rem;
        color: var(--accent-color);
        margin-bottom: 1rem;
    }
    .error-details {
        font-size: 0.9rem;
        margin-top: 1rem;
        color: var(--accent-color);
    }
`;
document.head.appendChild(style);

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', loadProjects);
