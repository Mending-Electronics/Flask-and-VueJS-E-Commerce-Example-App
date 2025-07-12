// Main Vue application for the catalog page
const { createApp, ref, computed, onMounted } = Vue;

createApp({
    delimiters: ['[[', ']]'],
    setup() {
        const products = ref([]);
        const selectedCategory = ref('');
        
        // Computed properties
        const categories = computed(() => {
            const cats = new Set(products.value.map(p => p.category));
            return Array.from(cats).sort();
        });
        
        const filteredProducts = computed(() => {
            if (!selectedCategory.value) return products.value;
            return products.value.filter(p => p.category === selectedCategory.value);
        });
        
        // Methods
        const fetchProducts = async () => {
            try {
                const response = await axios.get('/api/products');
                products.value = response.data;
            } catch (error) {
                console.error('Error fetching products:', error);
            }
        };
        
        const addToCart = async (productId) => {
            try {
                await axios.post('/api/cart', {
                    product_id: productId,
                    action: 'add'
                });
                updateCartCount();
            } catch (error) {
                console.error('Error adding to cart:', error);
            }
        };
        
        const updateCartCount = async () => {
            try {
                const response = await axios.get('/api/cart');
                const count = response.data.reduce((total, item) => total + item.quantity, 0);
                document.getElementById('cart-count').textContent = count;
            } catch (error) {
                console.error('Error fetching cart:', error);
            }
        };
        
        // Lifecycle hooks
        onMounted(() => {
            fetchProducts();
            updateCartCount();
        });
        
        return {
            products,
            selectedCategory,
            categories,
            filteredProducts,
            addToCart,
            updateCartCount
        };
    }
}).mount('#app');
