// Vue application for the cart page
const { createApp, ref, computed, onMounted } = Vue;

createApp({
    delimiters: ['[[', ']]'],
    setup() {
        const cartItems = ref([]);
        
        // Computed properties
        const subtotal = computed(() => {
            return cartItems.value.reduce((sum, item) => {
                return sum + (item.product.price * item.quantity);
            }, 0);
        });
        
        const totalItems = computed(() => {
            return cartItems.value.reduce((sum, item) => sum + item.quantity, 0);
        });
        
        // Methods
        const fetchCart = async () => {
            try {
                const response = await axios.get('/api/cart');
                cartItems.value = response.data;
                updateCartCount();
            } catch (error) {
                console.error('Error fetching cart:', error);
            }
        };
        
        const updateCartItem = async (item) => {
            try {
                await axios.post('/api/cart', {
                    product_id: item.product_id,
                    action: 'set',
                    quantity: item.quantity
                });
                updateCartCount();
            } catch (error) {
                console.error('Error updating cart item:', error);
            }
        };
        
        const updateQuantity = (item, change) => {
            const newQuantity = item.quantity + change;
            if (newQuantity >= 1) {
                item.quantity = newQuantity;
                updateCartItem(item);
            }
        };
        
        const removeFromCart = async (item) => {
            try {
                await axios.post('/api/cart', {
                    product_id: item.product_id,
                    action: 'remove'
                });
                await fetchCart();
                updateCartCount();
            } catch (error) {
                console.error('Error removing from cart:', error);
            }
        };
        
        const checkout = () => {
            // Get the checkout URL from the data attribute
            const checkoutUrl = document.getElementById('app').dataset.checkoutUrl;
            // Navigate to the checkout page
            window.location.href = checkoutUrl;
        };
        
        const updateCartCount = () => {
            const count = cartItems.value.reduce((total, item) => total + item.quantity, 0);
            document.getElementById('cart-count').textContent = count;
        };
        
        // Lifecycle hooks
        onMounted(() => {
            fetchCart();
        });
        
        return {
            cartItems,
            subtotal,
            totalItems,
            updateQuantity,
            updateCartItem,
            removeFromCart,
            checkout
        };
    }
}).mount('#app');
