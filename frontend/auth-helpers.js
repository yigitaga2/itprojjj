// Authentication helper functions for the School Feedback Platform

class AuthHelpers {
    /**
     * Check if user is currently logged in
     */
    static isLoggedIn() {
        const token = localStorage.getItem('authToken');
        return token !== null && token !== undefined && token !== '';
    }

    /**
     * Get current user's token
     */
    static getToken() {
        return localStorage.getItem('authToken');
    }

    /**
     * Store authentication token
     */
    static setToken(token) {
        localStorage.setItem('authToken', token);
    }

    /**
     * Remove authentication token
     */
    static removeToken() {
        localStorage.removeItem('authToken');
    }

    /**
     * Check if token is expired (basic check)
     */
    static isTokenExpired(token) {
        if (!token) return true;
        
        try {
            // Basic JWT token structure check
            const parts = token.split('.');
            if (parts.length !== 3) return true;
            
            // Decode payload (basic check, not cryptographically secure)
            const payload = JSON.parse(atob(parts[1]));
            const currentTime = Math.floor(Date.now() / 1000);
            
            return payload.exp && payload.exp < currentTime;
        } catch (error) {
            console.error('Error checking token expiration:', error);
            return true;
        }
    }

    /**
     * Get user role from token
     */
    static getUserRole() {
        const token = this.getToken();
        if (!token) return null;
        
        try {
            const parts = token.split('.');
            if (parts.length !== 3) return null;
            
            const payload = JSON.parse(atob(parts[1]));
            return payload.role || null;
        } catch (error) {
            console.error('Error getting user role:', error);
            return null;
        }
    }

    /**
     * Check if current user has specific role
     */
    static hasRole(requiredRole) {
        const userRole = this.getUserRole();
        return userRole === requiredRole;
    }

    /**
     * Check if current user is admin
     */
    static isAdmin() {
        return this.hasRole('admin');
    }

    /**
     * Logout user
     */
    static logout() {
        this.removeToken();
        
        // Clear any user-specific data
        sessionStorage.clear();
        
        // Redirect to login or home page
        window.location.reload();
    }

    /**
     * Handle authentication errors
     */
    static handleAuthError(error) {
        console.error('Authentication error:', error);
        
        // If token is invalid, logout user
        if (error.status === 401 || error.status === 403) {
            this.logout();
            UIComponents.showToast('Sessie verlopen. Log opnieuw in.', 'error');
        }
    }

    /**
     * Auto-refresh token if needed
     */
    static async refreshTokenIfNeeded() {
        const token = this.getToken();
        
        if (!token || this.isTokenExpired(token)) {
            this.logout();
            return false;
        }
        
        return true;
    }

    /**
     * Setup automatic token refresh
     */
    static setupAutoRefresh() {
        // Check token every 5 minutes
        setInterval(() => {
            this.refreshTokenIfNeeded();
        }, 5 * 60 * 1000);
    }
}
