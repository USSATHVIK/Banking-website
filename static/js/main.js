// Language translations
const translations = {
    en: {
        welcome: "Welcome to Rural Bank",
        tagline: "Simple, Secure, and Reliable Banking for Everyone",
        startBanking: "Start Banking",
        learnMore: "Learn More",
        checkBalance: "Check Balance",
        moneyTransfer: "Money Transfer",
        applyLoan: "Apply for Loan",
        support: "24/7 Support"
    },
    hi: {
        welcome: "ग्रामीण बैंक में आपका स्वागत है",
        tagline: "सभी के लिए सरल, सुरक्षित और विश्वसनीय बैंकिंग",
        startBanking: "बैंकिंग शुरू करें",
        learnMore: "और जानें",
        checkBalance: "बैलेंस देखें",
        moneyTransfer: "पैसे भेजें",
        applyLoan: "लोन के लिए आवेदन करें",
        support: "24/7 सहायता"
    }
};

// Function to toggle language
function toggleLanguage(lang) {
    const elements = document.querySelectorAll('[data-translate]');
    elements.forEach(element => {
        const key = element.getAttribute('data-translate');
        if (translations[lang][key]) {
            element.textContent = translations[lang][key];
        }
    });
    
    // Store language preference
    localStorage.setItem('preferredLanguage', lang);
}

// Initialize animations
document.addEventListener('DOMContentLoaded', () => {
    // Add smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Load preferred language
    const preferredLanguage = localStorage.getItem('preferredLanguage') || 'en';
    toggleLanguage(preferredLanguage);
});

// Form validation helper
function validateForm(formElement) {
    const inputs = formElement.querySelectorAll('input[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('error');
        } else {
            input.classList.remove('error');
        }
    });
    
    return isValid;
}

// Add loading indicators
function showLoading(buttonElement) {
    buttonElement.disabled = true;
    buttonElement.innerHTML = '<span class="spinner"></span> Loading...';
}

function hideLoading(buttonElement, originalText) {
    buttonElement.disabled = false;
    buttonElement.textContent = originalText;
}

// Toast notification system
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}
