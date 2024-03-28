
function decreaseQuantity(itemId) {
    // Call your Django view to decrease quantity
    updateQuantity(itemId, -1);
}

function increaseQuantity(itemId) {
    // Call your Django view to increase quantity
    updateQuantity(itemId, 1);
}

function updateQuantity(itemId, change) {
    fetch('/update_cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({itemId: itemId, change: change})
    })
    .then(response => response.json())
    .then(data => {
    if (parseInt(data.newQuantity) <= 0) {
        console.log('Removing item from cart');
        $('#tr_' + itemId).remove();
    } else {
        document.getElementById('quantity_' + itemId).innerText = data.newQuantity;
    }
    })
    .catch(error => console.error('Error:', error));
}

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function(){
// Function to fetch cart data with AJAX
function fetchCartData() {
    $.ajax({
        url: '/fetch-cart-data/', // URL to fetch cart data
        method: 'GET',
        success: function(response) {
            // Populate cart items in the overlay
            // console.log(response);
            $('#cart-items').html(response.cart_items);
            showCartOverlay(); // Show cart overlay once data is fetched
        },
        error: function(xhr, status, error) {
            console.error('Error fetching cart data:', error);
        }
    });
}

// Event listener for cart button click
$('#cart-button').click(function() {
    fetchCartData(); // Fetch cart data when cart button is clicked
});
    // Function to hide the cart overlay
    function hideCartOverlay() {
        $('.cart-overlay').css('display', 'none'); // Set display to none
        $('.cart-overlay').fadeOut(); // Fade out the cart overlay
    }

    // Event listener to close cart overlay when clicking outside of it
    $(document).on('click', function(event) {
        
        // Check if the clicked element is not inside the cart overlay and not the cart button
        if (!$(event.target).closest('.cart-overlay').length && !$(event.target).is('#cart-button')) {
            // console.log('clicked');
            hideCartOverlay(); // Hide cart overlay if clicked outside of it
        }
    });


    // Function to show the cart overlay (replace this with your own function)
    function showCartOverlay() {
        $('.cart-overlay').fadeIn(); // Fade in the cart overlay
    }

    // Example event listener to show the cart overlay (replace this with your own event listener)
    // $('#cart-button').on('click', function() {
    //     showCartOverlay(); // Show cart overlay when cart button is clicked
    // });
    $('#addToCart').click(function() {
        var updatedData = [];

        $('.ingredientQuantity').each(function() {
        var itemId = $(this).data('item-id');
        var itemName = $(this).data('item-name');
        var quantity = $(this).val();
        console.log(itemId, quantity);
        updatedData.push({ id: itemId, name: itemName, quantity: quantity });
        });

        var csrftoken = '{{ csrf_token }}';

        // Send updatedData to the server via AJAX
        $.ajax({
            url: '/addToCart/',
            method: 'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify({ updated_data: updatedData }),
            success: function(response) {
                if (response.success) {
                    console.log('Data successfully updated:', response);
                    $('.ingredientQuantity').remove();
                    $('.ingredientQuantityHeading').remove();
                    // Remove Add to Cart button
                    $('#addToCart').remove();
                    // Add View Cart button
                    $('#cartButtons').append('<button id="viewCart" class="btn btn-success">View Cart</button>');
                    fetchCartData();
                    // Handle success response
                } else {
                    console.error('Server returned an error:', response.error);
                    // Handle server error
                }
            },
            error: function(xhr, status, error) {
                console.error('Error sending request:', error);
                // Handle AJAX error
            }
        });
    });

    $(document).on('click', '#viewCart', function() {
        console.log('View cart button clicked');
        fetchCartData(); // Show cart overlay when cart button is clicked
    });
});
$(document).ready(function(){
    $.ajax({
        url: '/check_session_variable/',
        type: 'GET',
        success: function(data) {
            if(data.exists) {
                console.log("Session variable exists.");
                $('.ingredientQuantity').remove();
                $('.ingredientQuantityHeading').remove();
                // Remove Add to Cart button
                $('#addToCart').remove();
                // Add View Cart button
                $('#cartButtons').append('<button id="viewCart" class="btn btn-success">View Cart</button>');
                fetchCartData();
                
                // Do something if session variable exists
            } else {
                console.log("Session variable does not exist.");
                // Do something if session variable does not exist
            }
        }
    });
});
