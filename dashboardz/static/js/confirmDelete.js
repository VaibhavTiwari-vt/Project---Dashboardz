window.onload = function () {
    window.openModal = function (itemId, itemName) {
      const modal = document.getElementById('deleteModal');
      modal.classList.remove('hidden');
      document.getElementById('confirm').setAttribute('data-id', itemId);
    };
  
    // Close Modal
    function closeModal() {
      document.getElementById('deleteModal').classList.add('hidden');  // Hide modal
    }
  
    // Close modal on cancel button click
    document.getElementById('cancel').addEventListener('click', closeModal);
  
// Close modal when clicking outside
    window.onclick = function (event) {
      const modal = document.getElementById('deleteModal');
      if (event.target === modal) {
        closeModal();
      }
    };
  
// Delete Confirmation
    document.getElementById('confirm').addEventListener('click', function () {
      const itemId = this.getAttribute('data-id');  // Get stored item ID
  
      fetch(`/delete-table-data/${itemId}/`, {
        method: 'POST',
        headers: { 
          'X-CSRFToken': getCSRFToken(),
          'Content-Type': 'application/json'
        }
      })
      .then(response => {
        if (response.ok) {
          window.location.reload();
        } else {
          alert('Error deleting item');
        }
      })
      .catch(error => console.error('Error:', error));
    });

// Function to get CSRF token for Django
    function getCSRFToken() {
      return document.cookie.split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
    }
  };
  