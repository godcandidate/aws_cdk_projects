// Create floating DevOps tool icons
const createFloatingIcons = () => {
    const icons = [
        'fab fa-docker',
        'fab fa-kubernetes',
        'fab fa-aws',
        'fab fa-jenkins',
        'fab fa-github',
        'fab fa-python',
        'fab fa-linux'
    ];
    
    const container = document.querySelector('.floating-icons');
    
    icons.forEach((iconClass, index) => {
        const icon = document.createElement('i');
        icon.className = `${iconClass} floating-icon`;
        
        // Random position and animation duration
        const left = Math.random() * 100;
        const delay = Math.random() * -15;
        const duration = 15 + Math.random() * 10;
        
        icon.style.cssText = `
            left: ${left}%;
            animation-delay: ${delay}s;
            animation-duration: ${duration}s;
            font-size: ${24 + Math.random() * 24}px;
        `;
        
        container.appendChild(icon);
    });
};

// Handle resume download
const handleResumeDownload = () => {
    const downloadBtn = document.getElementById('download-resume');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', (e) => {
            e.preventDefault();
            // Add your resume download logic here
            alert('Resume download functionality to be implemented');
        });
    }
};

// Add smooth scrolling
const addSmoothScrolling = () => {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
};

// Initialize all animations and functionality
const init = () => {
    createFloatingIcons();
    handleResumeDownload();
    addSmoothScrolling();
};

// Run initialization when DOM is loaded
document.addEventListener('DOMContentLoaded', init);
