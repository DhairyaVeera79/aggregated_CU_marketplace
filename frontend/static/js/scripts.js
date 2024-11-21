document.addEventListener('DOMContentLoaded', function () {
    // Fetch items from the backend API
    fetch('/api/items')
        .then(response => response.json())
        .then(items => {
            const itemsContainer = document.getElementById('items-container');
            items.forEach(item => {
                const itemCard = document.createElement('div');
                itemCard.classList.add('col-md-3', 'd-flex', 'align-items-stretch');
                itemCard.innerHTML = `
                    <div class="card mb-4 h-100">
                        <img src="data:image/jpeg;base64,${item.image_data}" class="card-img-top" alt="Item Image">
                        <div class="card-body d-flex flex-column">
                            <h5 class="card-title">${item.item_name}</h5>
                            <p class="card-text">${item.description}</p>
                            <p class="card-text"><small class="text-muted">$${item.price}</small></p>
                            <a href="/item/${item.id}" class="btn btn-cu-gold">View Details</a>
                        </div>
                    </div>
                `;
                itemsContainer.appendChild(itemCard);
            });
        })
        .catch(error => console.error('Error fetching items:', error));
});