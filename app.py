import streamlit as st
import ollama
import pandas as pd

st.set_page_config(
    page_title="AI Shopping Assistant",
    page_icon="🛒",
    layout="wide"
    
)

st.title("🛒 AI Shopping Assistant")
st.write("Find products using AI based on your needs and budget.")


# ==========================================
# PRODUCT DATABASE
# ==========================================

products = [

    # Smartphones
    {
        "name": "Samsung Galaxy A55",
        "category": "Smartphone",
        "price": 25999,
        "features": "Good camera, AMOLED display, long battery life"
    },
    {
        "name": "OnePlus Nord CE 4",
        "category": "Smartphone",
        "price": 24999,
        "features": "Fast charging, good performance, large battery"
    },
    {
        "name": "Redmi Note 14 Pro",
        "category": "Smartphone",
        "price": 22999,
        "features": "Good camera, AMOLED display, strong battery"
    },
    {
        "name": "Realme 13 Pro",
        "category": "Smartphone",
        "price": 26999,
        "features": "Good camera, AMOLED display, fast charging"
    },
    {
        "name": "iQOO Z10",
        "category": "Smartphone",
        "price": 21999,
        "features": "Powerful performance, large battery, fast charging"
    },

    # Laptops
    {
        "name": "HP 15",
        "category": "Laptop",
        "price": 54999,
        "features": "Intel processor, 16GB RAM, 512GB SSD"
    },
    {
        "name": "Lenovo IdeaPad Slim 3",
        "category": "Laptop",
        "price": 57999,
        "features": "Good performance, 16GB RAM, 512GB SSD"
    },
    {
        "name": "Dell Inspiron 15",
        "category": "Laptop",
        "price": 62999,
        "features": "Intel processor, 16GB RAM, 512GB SSD, Full HD display"
    },
    {
        "name": "ASUS Vivobook 15",
        "category": "Laptop",
        "price": 59999,
        "features": "Intel processor, 16GB RAM, 512GB SSD, lightweight design"
    },
    {
        "name": "Acer Aspire 5",
        "category": "Laptop",
        "price": 52999,
        "features": "Good performance, 16GB RAM, 512GB SSD"
    },

    # Headphones
    {
        "name": "Sony WH-CH520",
        "category": "Headphones",
        "price": 4499,
        "features": "Wireless, long battery life, comfortable design"
    },
    {
        "name": "JBL Tune 770NC",
        "category": "Headphones",
        "price": 5999,
        "features": "Wireless, noise cancellation, strong bass"
    },
    {
        "name": "boAt Rockerz 550",
        "category": "Headphones",
        "price": 1999,
        "features": "Wireless, long battery life, powerful sound"
    },

    # Tablets
    {
        "name": "Samsung Galaxy Tab A9+",
        "category": "Tablet",
        "price": 18999,
        "features": "Large display, good battery, suitable for studying"
    },
    {
        "name": "Redmi Pad SE",
        "category": "Tablet",
        "price": 12999,
        "features": "Large display, good battery, suitable for entertainment"
    },
    {
        "name": "OnePlus Pad Go",
        "category": "Tablet",
        "price": 19999,
        "features": "Large display, good performance, long battery life"
    },

    # Smartwatches
    {
        "name": "Apple Watch SE",
        "category": "Smartwatch",
        "price": 24999,
        "features": "Fitness tracking, notifications, GPS, health features"
    },
    {
        "name": "Samsung Galaxy Watch 6",
        "category": "Smartwatch",
        "price": 19999,
        "features": "Fitness tracking, AMOLED display, health monitoring"
    },
    {
        "name": "Noise ColorFit Pro",
        "category": "Smartwatch",
        "price": 2999,
        "features": "Fitness tracking, calling, notifications, long battery"
    }
]


# ==========================================
# SESSION STATE
# ==========================================

if "cart" not in st.session_state:
    st.session_state.cart = []

if "checkout" not in st.session_state:
    st.session_state.checkout = False

if "order_placed" not in st.session_state:
    st.session_state.order_placed = False


# ==========================================
# AVAILABLE PRODUCTS
# ==========================================

st.subheader("🛍️ Available Products")

for i, product in enumerate(products):

    with st.expander(
        f"{product['name']} - ₹{product['price']:,}"
    ):

        st.write(f"**Category:** {product['category']}")
        st.write(f"**Features:** {product['features']}")

        selected = st.checkbox(
            "🛒 Add to Cart",
            key=f"cart_{i}"
        )

        # Add product
        if selected:

            if product["name"] not in [
                item["name"] for item in st.session_state.cart
            ]:
                st.session_state.cart.append(product)

        # Remove product
        else:

            st.session_state.cart = [
                item
                for item in st.session_state.cart
                if item["name"] != product["name"]
            ]


# ==========================================
# SHOPPING CART
# ==========================================

st.divider()

st.subheader("🛒 My Shopping Cart")

if len(st.session_state.cart) > 0:

    total = 0

    for item in st.session_state.cart:

        st.write(
            f"🛍️ **{item['name']}** — ₹{item['price']:,}"
        )

        total += item["price"]

    st.success(
        f"💰 Total Amount: ₹{total:,}"
    )

    # ======================================
    # BUY NOW BUTTON
    # ======================================

    if st.button(
        "🛒 Buy Now",
        use_container_width=True
    ):
        st.session_state.checkout = True
        st.rerun()


else:

    st.info(
        "Your cart is empty. Select products above."
    )


# ==========================================
# CHECKOUT
# ==========================================

if st.session_state.checkout and len(st.session_state.cart) > 0:

    st.divider()

    st.subheader("🧾 Checkout")

    st.write("### Selected Products")

    checkout_total = 0

    for item in st.session_state.cart:

        st.write(
            f"• **{item['name']}** — ₹{item['price']:,}"
        )

        checkout_total += item["price"]

    # Total Amount
    st.success(
        f"💰 Total Amount: ₹{checkout_total:,}"
    )

    # ======================================
    # ADDRESS
    # ======================================

    st.subheader("📍 Delivery Address")

    with st.form("address_form"):

        name = st.text_input(
            "Full Name"
        )

        phone = st.text_input(
            "Phone Number"
        )

        address = st.text_area(
            "Full Address"
        )

        city = st.text_input(
            "City"
        )

        state = st.text_input(
            "State"
        )

        pincode = st.text_input(
            "Pincode"
        )

        submitted = st.form_submit_button(
            "✅ Place Order",
            use_container_width=True
        )
        
        if submitted:

            if (
                name
                and phone
                and address
                and city
                and state
                and pincode
            ):

                st.session_state.order_placed = True

                st.balloons()  # <--- HERE

                st.success(
                    "🎉 Order placed successfully!"
                )

                st.write(
                    f"**Products:** {len(st.session_state.cart)}"
                )

                st.write(
                    f"**Total Amount:** ₹{checkout_total:,}"
                )

                st.info(
                    f"📦 Delivery Address: "
                    f"{address}, {city}, {state} - {pincode}"
                )

            else:

                st.error(
                    "⚠️ Please fill all address details."
                )

        if submitted:

            if (
                name
                and phone
                and address
                and city
                and state
                and pincode
            ):

                st.session_state.order_placed = True

                st.success(
                    "🎉 Order placed successfully!"
                )

                st.write(
                    f"**Products:** {len(st.session_state.cart)}"
                )

                st.write(
                    f"**Total Amount:** ₹{checkout_total:,}"
                )

                st.info(
                    f"📦 Delivery Address: "
                    f"{address}, {city}, {state} - {pincode}"
                )

            else:

                st.error(
                    "⚠️ Please fill all address details."
                )


# ==========================================
# AI SHOPPING ASSISTANT
# ==========================================

st.divider()

st.subheader("🤖 Ask AI Shopping Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


user_input = st.chat_input(
    "Example: Suggest a phone under ₹25,000 with a good camera"
)


if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    product_text = ""

    for product in products:

        product_text += f"""
Product: {product['name']}
Category: {product['category']}
Price: ₹{product['price']}
Features: {product['features']}
---
"""

    prompt = f"""
You are an AI Shopping Assistant.

Here is the available product database:

{product_text}

User request:
{user_input}

Instructions:
1. Recommend products only from the provided database.
2. Consider the user's budget and requirements.
3. Explain why each recommended product matches.
4. If no product matches, clearly say so.
5. Do not invent products or specifications.
6. Keep the answer simple and useful.
"""

    with st.chat_message("assistant"):

        response = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        answer = response["message"]["content"]

        st.write(answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })