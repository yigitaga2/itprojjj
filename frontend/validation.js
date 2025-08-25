// Form validation utilities for the School Feedback Platform

class FormValidator {
    /**
     * Validate email format
     */
    static validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    /**
     * Validate password strength
     */
    static validatePassword(password) {
        const errors = [];
        
        if (password.length < 8) {
            errors.push('Wachtwoord moet minimaal 8 karakters lang zijn');
        }
        
        if (!/[A-Z]/.test(password)) {
            errors.push('Wachtwoord moet minimaal één hoofdletter bevatten');
        }
        
        if (!/[a-z]/.test(password)) {
            errors.push('Wachtwoord moet minimaal één kleine letter bevatten');
        }
        
        if (!/[0-9]/.test(password)) {
            errors.push('Wachtwoord moet minimaal één cijfer bevatten');
        }
        
        return {
            isValid: errors.length === 0,
            errors: errors
        };
    }

    /**
     * Validate feedback text
     */
    static validateFeedbackText(text) {
        const errors = [];
        
        if (!text || text.trim().length === 0) {
            errors.push('Feedback tekst is verplicht');
        }
        
        if (text.trim().length < 10) {
            errors.push('Feedback moet minimaal 10 karakters bevatten');
        }
        
        if (text.trim().length > 1000) {
            errors.push('Feedback mag maximaal 1000 karakters bevatten');
        }
        
        return {
            isValid: errors.length === 0,
            errors: errors
        };
    }

    /**
     * Validate required field
     */
    static validateRequired(value, fieldName) {
        if (!value || value.trim().length === 0) {
            return {
                isValid: false,
                errors: [`${fieldName} is verplicht`]
            };
        }
        
        return {
            isValid: true,
            errors: []
        };
    }

    /**
     * Show validation errors on form
     */
    static showFieldError(fieldElement, errors) {
        // Remove existing error messages
        this.clearFieldError(fieldElement);
        
        if (errors.length > 0) {
            fieldElement.classList.add('error');
            
            const errorDiv = document.createElement('div');
            errorDiv.className = 'field-error';
            errorDiv.innerHTML = errors.join('<br>');
            
            fieldElement.parentNode.insertBefore(errorDiv, fieldElement.nextSibling);
        }
    }

    /**
     * Clear validation errors from field
     */
    static clearFieldError(fieldElement) {
        fieldElement.classList.remove('error');
        
        const existingError = fieldElement.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }
    }

    /**
     * Validate entire form
     */
    static validateForm(formData, rules) {
        const errors = {};
        let isValid = true;
        
        for (const [field, value] of Object.entries(formData)) {
            if (rules[field]) {
                const fieldErrors = [];
                
                for (const rule of rules[field]) {
                    const result = rule(value);
                    if (!result.isValid) {
                        fieldErrors.push(...result.errors);
                    }
                }
                
                if (fieldErrors.length > 0) {
                    errors[field] = fieldErrors;
                    isValid = false;
                }
            }
        }
        
        return {
            isValid: isValid,
            errors: errors
        };
    }
}
