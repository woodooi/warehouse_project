async function fetchProducts() {
    console.log('Fetching products...');
    try {
        const response = await fetch('/products');
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const products = await response.json();
        const tbody = document.getElementById('products-table-body');
        const productSelect = document.getElementById('product-select');

        if (tbody) tbody.innerHTML = '';
        if (productSelect) productSelect.innerHTML = '<option value="">Select a product</option>';

        products.forEach(product => {
            // Update Table
            if (tbody) {
                const tr = document.createElement('tr');
                const supplierName = product.supplier ? product.supplier.name : 'No Supplier';
                tr.innerHTML = `
                    <td>${product.id}</td>
                    <td>${product.name}</td>
                    <td>${product.sku}</td>
                    <td>${supplierName}</td>
                    <td>${product.quantity}</td>
                    <td>${product.price}</td>
                    <td>${product.min_stock}</td>
                `;
                tbody.appendChild(tr);
            }

            // Update Select
            if (productSelect) {
                const option = document.createElement('option');
                option.value = product.id;
                option.textContent = `${product.name} (SKU: ${product.sku})`;
                productSelect.appendChild(option);
            }
        });
        console.log('Products loaded successfully');
    } catch (error) {
        console.error('Error fetching products:', error);
        alert('Failed to load products. Check console for details.');
    }
}

async function fetchSuppliers() {
    console.log('Fetching suppliers...');
    try {
        const response = await fetch('/suppliers');
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const suppliers = await response.json();
        console.log('Suppliers received:', suppliers);

        const supplierSelect = document.getElementById('prod-supplier');
        if (supplierSelect) {
            supplierSelect.innerHTML = '<option value="">No Supplier</option>';
            suppliers.forEach(supplier => {
                const option = document.createElement('option');
                option.value = supplier.id;
                option.textContent = supplier.name;
                supplierSelect.appendChild(option);
            });
            console.log(`Populated ${suppliers.length} suppliers in dropdown`);
        } else {
            console.warn('Dropdown "prod-supplier" not found in DOM');
        }
    } catch (error) {
        console.error('Error fetching suppliers:', error);
        alert('Failed to load suppliers. Check console for details.');
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
            fetchProducts();
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

async function handleProductCreate(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = {
        name: formData.get('name'),
        sku: formData.get('sku'),
        price: parseFloat(formData.get('price')),
        quantity: parseInt(formData.get('quantity')),
        min_stock: parseInt(formData.get('min_stock')),
        supplier_id: formData.get('supplier_id') ? parseInt(formData.get('supplier_id')) : null
    };

    try {
        const response = await fetch('/products', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            alert('Product created successfully');
            fetchProducts();
            event.target.reset();
        } else {
            const error = await response.json();
            alert(`Error: ${JSON.stringify(error.detail)}`);
        }
    } catch (error) {
        console.error('Error creating product:', error);
        alert('Failed to create product. Check console.');
    }
}

async function handleSupplierCreate(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = {
        name: formData.get('name'),
        contact_email: formData.get('contact_email')
    };

    try {
        const response = await fetch('/suppliers', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            alert('Supplier created successfully');
            fetchSuppliers();
            event.target.reset();
        } else {
            const error = await response.json();
            alert(`Error: ${JSON.stringify(error.detail)}`);
        }
    } catch (error) {
        console.error('Error creating supplier:', error);
        alert('Failed to create supplier. Check console.');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    console.log('App initialization...');
    fetchProducts();
    fetchSuppliers();

    const transForm = document.getElementById('transaction-form');
    if (transForm) transForm.addEventListener('submit', handleTransaction);

    const prodForm = document.getElementById('product-form');
    if (prodForm) prodForm.addEventListener('submit', handleProductCreate);

    const suppForm = document.getElementById('supplier-form');
    if (suppForm) suppForm.addEventListener('submit', handleSupplierCreate);
});

