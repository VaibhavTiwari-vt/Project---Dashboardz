window.onload = function () {
  window.openModal = function (id) {
    const modal = document.getElementById('deleteModal');
    const form = document.getElementById('deleteDataForm');
    form.action = `/delete-table-data/${id}`; 
    modal.classList.remove('hidden');
  };

  function closeModal() {
    document.getElementById('deleteModal').classList.add('hidden');
  }

  document.getElementById('cancel').addEventListener('click', closeModal);


  window.onclick = function (event) {
    const modal = document.getElementById('deleteModal');
    if (event.target === modal) {
      closeModal();
    }
  };
};
