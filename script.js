// Basic form validation and confirmation
document.addEventListener('DOMContentLoaded', function () {
    const transactionForm = document.querySelector('form');

    if (transactionForm) {
        transactionForm.addEventListener('submit', function (event) {
            const amount = document.getElementById('amount').value;
            const confirmation = confirm(`You are about to send ${amount}. Do you want to proceed?`);
            
            if (!confirmation) {
                event.preventDefault();
            }
        });
    }
});
