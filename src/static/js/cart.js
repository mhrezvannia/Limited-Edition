$(document).ready(function () {
    // Add product to cart
    $('.add-to-cart').on('click', function () {
        const productId = $(this).data('product_id');
        const quantity = 1; // Adjust as necessary

        $.ajax({
            url: '/api/v1/cart/add/',  // Adjust if you change your URL patterns
            method: 'POST',
            data: JSON.stringify({ product_id: productId, quantity: quantity }),
            contentType: 'application/json',
            success: function (data) {
                console.log('Product added to cart:', data);
                // Optionally update the cart UI here
            },
            error: function (error) {
                console.error('Error adding product to cart:', error);
            }
        });
    });

    $('.update-cart-item').on('change', function () {
        const cartProductId = $(this).data('cart-product-id');
        const newQuantity = $(this).val();

        $.ajax({
            url: '/api/v1/cart/update/' + cartProductId + '/',
            method: 'PUT',
            data: JSON.stringify({ quantity: newQuantity }),
            contentType: 'application/json',
            success: function (data) {
                console.log('Cart item updated:', data);
                // Optionally update the cart UI here
            },
            error: function (error) {
                console.error('Error updating cart item:', error);
            }
        });
    });

    // Remove product from cart
    $('.remove-cart-item').on('click', function () {
        const cartProductId = $(this).data('cart-product-id');

        $.ajax({
            url: '/api/v1/cart/remove/' + cartProductId + '/',
            method: 'DELETE',
            success: function () {
                console.log('Cart item removed');
                // Optionally refresh the cart UI here
            },
            error: function (error) {
                console.error('Error removing cart item:', error);
            }
        });
    });

    // The clear cart functionality is removed, as there's no defined endpoint
});

$(document).ready(function() {
    // Update item quantity
    $('.update-quantity').on('change', function() {
        const productId = $(this).data('product-id');
        const newQuantity = $(this).val();

        $.ajax({
            url: '/api/v1/cart/update/', // Your update cart endpoint
            type: 'PUT',
            contentType: 'application/json',
            data: JSON.stringify({
                product_id: productId,
                quantity: newQuantity
            }),
            success: function(response) {
                // Handle success
                console.log('Updated cart item:', response);
                // Optionally update the UI with new totals
            },
            error: function(xhr) {
                console.error('Error updating cart:', xhr.responseJSON.error);
            }
        });
    });

    // Remove item from cart
    $('.remove-item').on('click', function() {
        const productId = $(this).data('product-id');

        $.ajax({
            url: '/api/v1/cart/remove/', // Your remove cart item endpoint
            type: 'DELETE',
            contentType: 'application/json',
            data: JSON.stringify({
                product_id: productId
            }),
            success: function(response) {
                // Handle success
                console.log('Removed cart item:', response);
                // Optionally remove the item from the UI
                location.reload(); // Reload the page to reflect changes
            },
            error: function(xhr) {
                console.error('Error removing cart item:', xhr.responseJSON.error);
            }
        });
    });
});