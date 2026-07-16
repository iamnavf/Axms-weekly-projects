from flask import Flask, render_template
import pandas as pd

"""import plotly.express as px
from plotly.offline import plot
import plotly.graph_objects as go"""

from flask import request
import math

app = Flask(__name__)

# Load dataset
df = pd.read_csv("data/df_master.csv")


@app.route("/")
def dashboard():
    total_revenue = round(df["price"].sum(), 2)
    total_orders = df["order_id"].nunique()
    total_customers = df["customer_unique_id"].nunique()
    total_sellers = df["seller_id"].nunique()
    avg_review_score = round(df["avg_review_score"].mean(), 2)
    avg_delivery_days = round(df["delivery_time_days"].mean(), 2)

  
    return render_template("dashboard.html",total_revenue=total_revenue,total_orders=total_orders,total_customers=total_customers,
        total_sellers=total_sellers,avg_review_score=avg_review_score,avg_delivery_days=avg_delivery_days )


@app.route("/sales")
def sales():

    total_revenue = round(df["price"].sum(), 2)

    total_orders = df["order_id"].nunique()

    avg_order_value = round(
        total_revenue / total_orders,
        2
    )

    top_category = (
        df.groupby("product_category_name_english")["price"]
        .sum()
        .idxmax()
    )

    top_state = (
        df.groupby("customer_state")["price"]
        .sum()
        .idxmax()
    )

    return render_template(
        "sales.html",

        total_revenue=total_revenue,
        avg_order_value=avg_order_value,
        top_category=top_category,
        top_state=top_state
    )

#customer route
@app.route("/customer")
def customer():
    #Total Customers
    total_customers = df["customer_unique_id"].nunique()

    #Repeat Customers
    customer_orders = (
        df.groupby("customer_unique_id")["order_id"].nunique())

    repeat_customers = (customer_orders > 1).sum()

    #Total Customer Cities
    total_cities = df["customer_city"].nunique()

    #Average Customer Spending
    total_revenue = df["price"].sum()
    avg_customer_spending = round(total_revenue / total_customers, 2)

    #Business Insights
    insight_1 = f"The platform has {total_customers:,} unique customers."

    insight_2 = f"{repeat_customers:,} customers placed more than one order."

    insight_3 = f"Customers are distributed across {total_cities:,} cities."

    insight_4 = ("Average customer spending is " f"R$ {avg_customer_spending:,.2f}.")

    return render_template("customers.html",total_customers=total_customers,repeat_customers=repeat_customers,total_cities=total_cities,
        avg_customer_spending=avg_customer_spending,insight_1=insight_1,insight_2=insight_2,insight_3=insight_3,insight_4=insight_4)

#product
@app.route("/product")
def product():

    #Total Products Sold
    total_products_sold = len(df)

    #Total Categories
    total_categories = df["product_category_name_english"].nunique()

    #Average Product Price
    avg_product_price = round(df["price"].mean(), 2)

    #Best Selling Category
    best_category = (df.groupby("product_category_name_english")["order_item_id"].count().sort_values(ascending=False))

    top_category = best_category.index[0]
    top_category_sales = best_category.iloc[0]

    # Key Insights
    insight_1 = f"A total of {total_products_sold:,} products were sold."

    insight_2 = f"The store offers {total_categories} different product categories."

    insight_3 = f"The average product price is R$ {avg_product_price:,.2f}."

    insight_4 = (f"{top_category} is the best-selling category "f"with {top_category_sales:,} products sold.")

    return render_template("products.html",total_products_sold=total_products_sold,total_categories=total_categories,
        avg_product_price=avg_product_price,top_category=top_category,top_category_sales=top_category_sales,
        insight_1=insight_1,insight_2=insight_2,insight_3=insight_3,insight_4=insight_4)

#seller
@app.route("/seller")
def seller():

    #Total Sellers
    total_sellers = df["seller_id"].nunique()

    #Seller States
    total_seller_states = df["seller_state"].nunique()

    #Top Seller by Revenue
    seller_revenue = (df.groupby("seller_id")["price"].sum().sort_values(ascending=False))

    top_seller = seller_revenue.index[0]
    top_seller_revenue = round(seller_revenue.iloc[0], 2)

    #Average Delivery Time
    avg_delivery_time = round(df["delivery_time_days"].mean(), 2)

    #Key Insights
    insight_1 = f"The platform has {total_sellers:,} active sellers."

    insight_2 = f"Sellers operate across {total_seller_states} states."

    insight_3 = (
        f"The highest revenue seller generated "
        f"R$ {top_seller_revenue:,.2f}.")

    insight_4 = (
        f"The average delivery time across all sellers is "
        f"{avg_delivery_time} days.")

    return render_template("sellers.html",total_sellers=total_sellers,total_seller_states=total_seller_states,
        top_seller=top_seller[:10] + "...",top_seller_revenue=top_seller_revenue,avg_delivery_time=avg_delivery_time,
        insight_1=insight_1,insight_2=insight_2,insight_3=insight_3,insight_4=insight_4)


@app.route("/delivery")
def delivery():

    #Average Delivery Time
    avg_delivery_time = round(df["delivery_time_days"].mean(), 2)

    #Delayed Deliveries
    delayed_deliveries = (df["delivery_status"] == "Delayed").sum()

    #On-Time Deliveries
    on_time_deliveries = (df["delivery_status"] == "On Time").sum()

    #Average Shipping Duration
    avg_shipping_duration = round(df["shipping_duration_days"].mean(), 2)

    #Key Insights
    insight_1 = f"The average delivery time is {avg_delivery_time} days."

    insight_2 = f"{delayed_deliveries:,} orders experienced delayed delivery."

    insight_3 = f"{on_time_deliveries:,} orders were delivered on time."

    insight_4 = (
        f"The average shipping duration is "
        f"{avg_shipping_duration} days.")

    return render_template("delivery.html",avg_delivery_time=avg_delivery_time,delayed_deliveries=delayed_deliveries,
        on_time_deliveries=on_time_deliveries,avg_shipping_duration=avg_shipping_duration,insight_1=insight_1,insight_2=insight_2,
        insight_3=insight_3,insight_4=insight_4)


@app.route("/payment_review")
def payment_review():


    most_payment_method = (df["primary_payment_type"].mode()[0])

    avg_payment_value = round(df["total_payment_value"].mean(), 2)

    avg_installments = round(df["max_installments"].mean(), 1)

    avg_review_score = round(df["avg_review_score"].mean(), 2)

    positive_reviews = (df["review_sentiment"] == "Positive").sum()

    negative_reviews = (df["review_sentiment"] == "Negative").sum()

    insight_1 = (f"{most_payment_method.title()} is the most preferred payment method.")

    insight_2 = (f"The average payment value is R$ {avg_payment_value:,.2f}.")

    insight_3 = (f"Customers use an average of {avg_installments} installments.")

    insight_4 = (f"The average customer review score is {avg_review_score}/5.")

    insight_5 = (f"There are {positive_reviews:,} positive reviews and "
        f"{negative_reviews:,} negative reviews.")

    return render_template(
        "payment_review.html",most_payment_method=most_payment_method,avg_payment_value=avg_payment_value,
        avg_installments=avg_installments,avg_review_score=avg_review_score,positive_reviews=positive_reviews,negative_reviews=negative_reviews,

        insight_1=insight_1,insight_2=insight_2,insight_3=insight_3,insight_4=insight_4,insight_5=insight_5)


@app.route("/explorer")
def explorer():

    search = request.args.get("search", "")
    state = request.args.get("state", "")
    page = request.args.get("page", 1, type=int)

    filtered_df = df.copy()

    # Search by Order ID or Customer City
    if search:
        filtered_df = filtered_df[
            filtered_df["order_id"].astype(str).str.contains(search, case=False)
            |
            filtered_df["customer_city"].astype(str).str.contains(search, case=False)
        ]

    # Filter by State
    if state:
        filtered_df = filtered_df[
            filtered_df["customer_state"] == state
        ]

    # Pagination
    per_page = 20

    total_rows = len(filtered_df)

    total_pages = math.ceil(total_rows / per_page)

    start = (page - 1) * per_page
    end = start + per_page

    table_data = filtered_df.iloc[start:end]

    states = sorted(df["customer_state"].dropna().unique())

    return render_template("explorer.html",table_data=table_data,page=page,
                           total_pages=total_pages,search=search,selected_state=state, states=states)

if __name__ == "__main__":
    app.run()

