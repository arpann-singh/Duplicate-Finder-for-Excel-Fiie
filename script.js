document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    let formData = new FormData();
    formData.append('file', document.getElementById('file').files[0]);
    formData.append('sheet_name', document.getElementById('sheet_name').value);

    fetch('https://duplicate-finder-backend.herokuapp.com/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            displayDuplicates(data.duplicates);
        }
    })
    .catch(error => {
        alert('Error: ' + error);
    });
});

function displayDuplicates(duplicates) {
    let tableBody = document.querySelector('#duplicates-table tbody');
    tableBody.innerHTML = '';
    
    duplicates.forEach(function(row, index) {
        let tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${index + 1}</td>
            <td>${row.Name}</td>
            <td>${JSON.stringify(row)}</td>
        `;
        tableBody.appendChild(tr);
    });
}
