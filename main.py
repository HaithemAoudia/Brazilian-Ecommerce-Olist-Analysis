import streamlit as st
import pandas as pd

st.set_page_config(page_title="Olist E-commerce Case Study", layout="wide")



st.title("Driving Olist’s Success with Data-Powered Decisions 🚀")

st.write("""Welcome to my solution for the Olist Case Study! As a **Membership Analyst** at Olist, my goal is to **deepen our understanding of customer behavior** and uncover **valuable insights** that drive actionable business opportunities.        

### **What do I aim to achieve through my solution?**
1️⃣ **Maximize the success** of Olist's Membership initiative through a **data-driven and customer centric approach**.  
2️⃣ Gain a **deep understanding** of customer purchase patterns.  
3️⃣ Understand **customer perceptions** of Olist, identifying their points of **satisfaction** and **dissatisfaction**.
""")

st.header("1. Database Structure")

# Create two columns
col1, col2 = st.columns([1.2, 1])  # Adjust the width ratio as needed

# Add the text to the left column
with col1:
    st.write("""
    The Brazilian Ecommerce Dataset includes 8 datasets covering different areas of the ecommerce business. To generate 
    a database structure it is key to first understand the business requirement and what the use case of the database is.
    As the goal here is to create a data structure to easily query consumer insights in a scalable way that aligns with 
    the requirements of the Analytics Team, it is clear that the use case here is analytical. Therefore, a dimensional data model 
    rather than a relational data model is chosen as the main database structure to be adopted.
    
    This is due to the following reasons:
    - More scalable for analytics as the data volume and query complexity increases.
    - More optimal query performance and minimizes the number of joins required.
    - Business users can more easily understand the relationships between data.
             
    The Fact_Order_Item is chosen as the central Fact table as it represents the lowest level of granularity in our data.
         To capture the business measures for Olist, Dim_Order, Dim_Product, Dim_Seller, Dim_Customer, Dim_Review and Dim_Payment are
         added as dimensions in the database structure. 
    """)

# Add the image to the right column
with col2:
    st.image("Dimensional Data Model.png", caption="Ecommerce Dimensional Data Model")

st.write("""
### Example Query:

What is the average review score and total sales revenue for each product category?
""")

st.code("""
SELECT dp.product_category_name AS category, 
       AVG(dr.review_score) AS average_review_score, 
       SUM(foi.price) AS total_sales_revenue
FROM Fact_Order_Items foi
JOIN Dim_Product dp ON foi.product_id = dp.product_id
JOIN Dim_Review dr ON foi.review_id = dr.review_id
GROUP BY dp.product_category_name
ORDER BY total_sales_revenue DESC;
""", language='sql')



st.header("2. Data Analysis")
st.write("""This section covers the data analysis carried out, focusing on three areas. First, a customer value and segmentation analysis to explore 
         opportunities for implementing a potential membership program. Secondly, a product analysis focusing on product purchase behavoirs. Thirdly, a 
         customer review analysis to a uncover the key points of satisfaction and dissatisfaction for customers.""")

st.subheader("2.1 Customer Value & Segmentation Analysis")
st.write("""As a membership analyst, I believe its first important to understand who your customers and what are the different consumer segments
             that are purchasing from you. Hence, I will first start with segmenting the consumer base based on how valuable they are to the business using 
             the RFM model as a proxy for overall customer value and the K means clustering algorthim to cluster the customers into distinct group based on their value 
             to Olist. The RFM model is chosen as it captures the important aspects of customer behavoiur that directly correlate with business value in a very efficient and simple way.""")
st.markdown("""
#### RFM Model:
- **Recency**: How recently did the customer place the last order?
- **Frequency**: How often does the customer place orders?
- **Monetary**: How much does the customer spend on average?
""")


data = {
    "Cluster": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11],
    "Recency": [516.072424, 395.454216, 276.699048, 171.436615, 69.354288, 78.038850, 77.031320, 86.897727, 74.600000, 55.571429, 25.000000],
    "Frequency": [1.000000, 1.012036, 1.017486, 1.025930, 1.035763, 1.292541, 1.604027, 2.488636, 3.360000, 6.428571, 4.000000],
    "Monetary": [122.366956, 161.204814, 170.608983, 187.985479, 211.200966, 871.955598, 2385.228322, 4474.276136, 6310.330000, 2029.744286, 27935.460000],
    "Segment Value": [
        "Low-Value",  
        "Low-Value", 
        "Low-Value",  
        "Low-Value",  
        "Mid-Value", 
        "Mid-Value",  
        "Mid-Value",  
        "High-Value", 
        "High-Value", 
        "High-Value", 
        "High-Value", 
    ]
}


# Convert the data into a DataFrame
df = pd.DataFrame(data)

# Set OverallScore as the index
df.set_index("Cluster", inplace=True)

# Apply pandas Styler for formatting
styled_df = df.style.format(
    {
        "Recency": "{:.2f}",
        "Frequency": "{:.2f}",
        "Monetary": "${:,.2f}"
    }
).set_properties(
    **{'font-size': '14px', 'text-align': 'center'}
)

# Display the styled DataFrame in Streamlit
st.subheader("RFM Clusters")
st.write("""The clusters are formed by first calculating the Recency, Frequency, and Monetary of each customer. Thereafter the 
         KMeans clustering algorithm is used to segment customers into distinct groups based on the RFM values for each customer. The cluster labels are ordered where 
         higher clusters signifiy more valuable customers and lower cluster label signify lower valuable customers. For simplicity, 3 quantiles of the 12 clusters are formed
         consisting of low, mid and high value customers.""")
st.dataframe(styled_df, use_container_width=True)
st.image("Clusters.png", caption="RFM Customer Segmentation")
st.write("""Visually we get a good representation of how the high value customers are active customers that are purchasing more
         frequently and spending more money at Olist. Hence, this group represents the loyal customers at Olist that spend the most
         on average and are more likely to subscribe to a membership program at Olist. Therefore, its important to drill down further
         into this segment and understand what, when and where they purchase.""")
st.image("product_category_customers.png")
st.write("""Computer accessories and furniture decor are the most frequently purchased categories across high value customers compared
         to any other product category. Hence, a membership program for those categories specifically could be a potential option to engage
         and retain high value customers.""")

col1, col2, col3 = st.columns([1, 1, 1]) 

with col1:
    st.image("weekday_trend.png")

with col2:
    st.image("hourly_trend.png")

with col3:
    st.image("customer_city_distribution.png")

st.write("Peak purchase hour for high value customers is during the day at 2pm and during the week the peak day is thursday.")
st.write("The majority of the high value customers are situation in Sao Paulo. This is to be expected and is most likely the case with other consumer segments given Sao Paulo is biggest city in Brazil.")
st.subheader("2.2 Product Affinity")
st.write("""Gaining an understanding of customer purchase behaviour and what combination of products do they purchase is key to developing a
         holistic understanding of customer behaviour and product desirability. Hence, in this section I will focus on analyzing what 
         products do customer often purchase together.

As multiple items can be part of the same order, I calculated the number of times each product combination appears in a customer's purchase order.""")
st.image("product_affinity.png")
st.write("""Since the product name is anonymous in the dataset I will focus on product category name instead. The category computer accessories
         contains the most combination of products purchased together. Moreover, it interesting that the bed bath table category is frequently purchased with the home comfort category.
        Olist can recommed products to customers based on the specific product they are viewing. This also is a valuable cross-sell opportunity that Olist should take advantage of.""")
st.subheader("2.3 Customer Reviews")
st.write("""To understand the key talking points across all the reviews in an efficient manner I will extract the most frequent combination of words (Trigram) used together across all reviews. """)
st.write("**Postive Reviews**")
st.image("positive review.png")
st.write("""Most customers are frequently praising the delivery aspect of the business in terms the speed of the delivery and timeliness of it. 
         The prais of high-quality goods is also present in many reviews.""")
st.write("**Negative Reviews**")
st.image("negative review.png")
st.write("""In terms of negative reviews, most concerns are also regarding the deliveries 
         and the shipment including late deliveries, product not being delivered or wrong 
         product being shippped. Concerns outside of deliveries also include unresponsive customer service
         and defective products.""")
st.header("3.0 Main Insights and Conclusions")
st.write("""
         1.	High-value customers are primarily in São Paulo and predominantly purchasing from computer accessories and furniture décor categories, with peak purchasing activity occurring at 2 PM on Thursdays. Olist can roll out membership initiative 
         specilifically tailored towards High Value customer which in turn can increase loyalty and long term sales.
        2.	Customers often pair products from the computer accessories category, indicating strong purchase combinations 
         within this segment. Additionally, items from the largest product category, 
         Bed Bath & Table, are frequently combined with Home Comfort products. Olist can cross sell relevant products
         and improve thier recommendation systems to increase thier average order value (AOV).
        3.	Customers praise the fast delivery and high-quality goods while dissatisfaction arises from delayed deliveries, unresponsive customer service, defective products and wrong product being shipped. Olist can address these customer concerns which
         may increase the number of high value and loyal customers which in turn can improve long term sales and membership initiatives.
""")




