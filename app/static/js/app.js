async function fetchProducts() {
    try {
        const response = await fetch('/products');
        const products = await response.json();
        const tbody = document.getElementById('products-table-body');
        const productSelect = document.getElementById('product-select');

        tbody.innerHTML = '';
        productSelect.innerHTML = '<option value="">Select a product</option>';

        products.forEach(product => {
            // Update Table
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${product.id}</td>
                <td>${product.name}</td>
                <td>${product.sku}</td>
                <td>${product.quantity}</td>
                <td>${product.price}</td>
                <td>${product.min_stock}</td>
            `;
            tbody.appendChild(tr);

            // Update Select
            const option = document.createElement('option');
            option.value = product.id;
            option.textContent = `${product.name} (SKU: ${product.sku})`;
            productSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error fetching products:', error);
    }
}

async function handleTransaction(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = {
        product_id: parseInt(formData.get('product_id')),
        quantity: parseInt(formData.get('quantity')),
        type: formData.get('type')
    };

    try {
        const response = await fetch('/transactions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            alert('Transaction successful');
            fetchProducts(); // Refresh list
            event.target.reset();
        } else {
            const error = await response.json();
            alert(`Error: ${error.detail}`);
        }
    } catch (error) {
        console.error('Error submitting transaction:', error);
        alert('Failed to submit transaction');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    fetchProducts();
    const form = document.getElementById('transaction-form');
    if (form) {
        form.addEventListener('submit', handleTransaction);
    }
});
