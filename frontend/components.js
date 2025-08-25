// Reusable UI components for the School Feedback Platform

class UIComponents {
    /**
     * Create a loading spinner element
     */
    static createLoadingSpinner() {
        const spinner = document.createElement('div');
        spinner.className = 'loading-spinner';
        spinner.innerHTML = `
            <div class="spinner-circle"></div>
            <span>Laden...</span>
        `;
        return spinner;
    }

    /**
     * Create a notification toast
     */
    static createToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <span class="toast-message">${message}</span>
                <button class="toast-close">&times;</button>
            </div>
        `;
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 5000);
        
        return toast;
    }

    /**
     * Create a confirmation modal
     */
    static createConfirmModal(title, message, onConfirm) {
        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        modal.innerHTML = `
            <div class="modal-content">
                <h3>${title}</h3>
                <p>${message}</p>
                <div class="modal-actions">
                    <button class="btn btn-secondary modal-cancel">Annuleren</button>
                    <button class="btn btn-primary modal-confirm">Bevestigen</button>
                </div>
            </div>
        `;
        
        // Event listeners
        modal.querySelector('.modal-cancel').addEventListener('click', () => {
            document.body.removeChild(modal);
        });
        
        modal.querySelector('.modal-confirm').addEventListener('click', () => {
            onConfirm();
            document.body.removeChild(modal);
        });
        
        return modal;
    }

    /**
     * Show toast notification
     */
    static showToast(message, type = 'info') {
        const toast = this.createToast(message, type);
        document.body.appendChild(toast);
    }

    /**
     * Show loading state
     */
    static showLoading(container) {
        const spinner = this.createLoadingSpinner();
        container.appendChild(spinner);
        return spinner;
    }

    /**
     * Hide loading state
     */
    static hideLoading(spinner) {
        if (spinner && spinner.parentNode) {
            spinner.parentNode.removeChild(spinner);
        }
    }
}
