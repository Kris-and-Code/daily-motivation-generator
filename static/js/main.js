document.addEventListener('DOMContentLoaded', function() {
    const quoteForm = document.getElementById('quoteForm');
    const quoteResult = document.querySelector('.quote-result');
    const quoteText = document.querySelector('.quote-text');

    quoteForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const mood = document.getElementById('mood').value;
        const context = document.getElementById('context').value;

        try {
            // Show loading state
            const submitButton = quoteForm.querySelector('button[type="submit"]');
            submitButton.disabled = true;
            submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Generating...';

            const response = await fetch('/api/generate-quote', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ mood, context })
            });

            const data = await response.json();

            if (!data.is_unique) {
                // Show warning about non-unique quote
                showAlert('Warning: Similar quote already exists. Generating alternative...', 'warning');
                return;
            }

            // Display the quote
            quoteText.textContent = data.quote;
            quoteResult.classList.remove('d-none');

            // Add to history immediately
            addToHistory(data);

            // Smooth scroll to quote
            quoteResult.scrollIntoView({ behavior: 'smooth' });

        } catch (error) {
            console.error('Error:', error);
            showAlert('Failed to generate quote. Please try again.', 'danger');
        } finally {
            // Reset button state
            submitButton.disabled = false;
            submitButton.innerHTML = 'Generate Quote';
        }
    });

    function showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.role = 'alert';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        const container = document.querySelector('.main-content');
        container.insertBefore(alertDiv, container.firstChild);

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }

    function addToHistory(quoteData) {
        const historyContainer = document.getElementById('recentQuotes');
        if (!historyContainer) return;

        const quoteCard = document.createElement('div');
        quoteCard.className = 'col-md-6 mb-4';
        quoteCard.innerHTML = `
            <div class="card h-100">
                <div class="card-body">
                    <p class="card-text">${quoteData.quote}</p>
                    <div class="text-muted">
                        <small>Mood: ${quoteData.mood}</small>
                        ${quoteData.context ? `<br><small>Context: ${quoteData.context}</small>` : ''}
                    </div>
                </div>
            </div>
        `;

        historyContainer.insertBefore(quoteCard, historyContainer.firstChild);
    }
}); 