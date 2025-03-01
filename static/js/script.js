// Get all quick view buttons and modal
const quickViewBtns = document.querySelectorAll('.quick-view-btn');
const modal = document.getElementById('quick-view-modal');
const closeBtn = document.querySelector('.close-modal');

// Cookie ingredients database
const cookieIngredients = {
    'Chocolate Chip': [
        'All-Purpose Flour',
        'Unsalted Butter',
        'Brown Sugar',
        'Granulated Sugar',
        'Large Eggs',
        'Pure Vanilla Extract',
        'Premium Chocolate Chips',
        'Baking Soda',
        'Sea Salt'
    ],
    'Oatmeal Raisin': [
        'Old-Fashioned Oats',
        'All-Purpose Flour',
        'Unsalted Butter',
        'Brown Sugar',
        'Large Eggs',
        'Plump Raisins',
        'Ground Cinnamon',
        'Baking Soda',
        'Salt'
    ],
    'Sugar Cookies': [
        'All-Purpose Flour',
        'Unsalted Butter',
        'Granulated Sugar',
        'Large Eggs',
        'Pure Vanilla Extract',
        'Baking Powder',
        'Salt'
    ],
    'Double Chocolate Chip': [
        'All-Purpose Flour',
        'Dutch Cocoa Powder',
        'Unsalted Butter',
        'Brown Sugar',
        'Large Eggs',
        'Premium Chocolate Chips',
        'Pure Vanilla Extract',
        'Baking Soda',
        'Salt'
    ],
    'Peanut Butter': [
        'Creamy Peanut Butter',
        'All-Purpose Flour',
        'Unsalted Butter',
        'Brown Sugar',
        'Large Eggs',
        'Pure Vanilla Extract',
        'Baking Soda',
        'Salt'
    ],
    'White Chocolate Macadamia': [
        'All-Purpose Flour',
        'Unsalted Butter',
        'Brown Sugar',
        'Large Eggs',
        'White Chocolate Chips',
        'Macadamia Nuts',
        'Pure Vanilla Extract',
        'Baking Soda',
        'Salt'
    ]
};

// Add allergen information to cookie database
const cookieAllergens = {
    'Chocolate Chip': ['Contains: Wheat, Dairy, Eggs', 'May contain traces of nuts'],
    'Oatmeal Raisin': ['Contains: Wheat, Dairy, Eggs', 'May contain traces of nuts'],
    'Sugar Cookies': ['Contains: Wheat, Dairy, Eggs'],
    'Double Chocolate Chip': ['Contains: Wheat, Dairy, Eggs', 'May contain traces of nuts'],
    'Peanut Butter': ['Contains: Wheat, Dairy, Eggs, Peanuts', 'May contain traces of other nuts'],
    'White Chocolate Macadamia': ['Contains: Wheat, Dairy, Eggs, Tree Nuts (Macadamia)', 'May contain traces of peanuts']
};

// Add click event to all quick view buttons
if (quickViewBtns) {
    quickViewBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const productCard = this.closest('.product-card');
            
            // Get product details
            const productName = productCard.querySelector('h3').textContent;
            const productDesc = productCard.querySelector('.product-description').textContent;
            const productPrice = productCard.querySelector('.price').textContent;
            const productImage = productCard.querySelector('.product-image img').src;
            
            // Update modal content
            document.getElementById('modal-product-image').src = productImage;
            document.getElementById('modal-product-name').textContent = productName;
            document.getElementById('modal-product-description').textContent = productDesc;
            document.getElementById('modal-product-price').textContent = productPrice;

            // Add ingredients list
            const ingredients = cookieIngredients[productName] || [];
            const ingredientsList = ingredients.map(ing => `<li>${ing}</li>`).join('');
            
            // Add allergen warnings
            const allergens = cookieAllergens[productName] || [];
            const allergensList = allergens.map(allergy => `<p>${allergy}</p>`).join('');
            
            // Add ingredients section if it doesn't exist
            let ingredientsSection = document.querySelector('.modal-ingredients');
            if (!ingredientsSection) {
                const modalInfo = document.querySelector('.modal-info');
                ingredientsSection = document.createElement('div');
                ingredientsSection.className = 'modal-ingredients';
                modalInfo.insertBefore(ingredientsSection, document.querySelector('.quantity-selector'));
            }
            
            ingredientsSection.innerHTML = `
                <h3>Ingredients</h3>
                <ul class="ingredients-list">
                    ${ingredientsList}
                </ul>
                <div class="allergen-warning">
                    <h4>Allergy Information</h4>
                    ${allergensList}
                </div>
            `;
            
            // Show modal
            modal.style.display = 'block';
        });
    });
}

// Close modal when clicking the close button
if (closeBtn) {
    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });
}

// Close modal when clicking outside
window.addEventListener('click', function(event) {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});
