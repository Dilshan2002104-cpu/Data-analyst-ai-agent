# Sample Questions for Testing SQL Integration

Based on the `test_database_mysql.sql` schema, here are questions you can ask in the Unified Chat:

## Basic Queries (Beginner)

### Customer Questions
1. "How many customers do we have?"
2. "Show me all customers"
3. "Which customers are from the North region?"
4. "What's the email address for Acme Corporation?"
5. "List all customers who signed up in 2023"

### Product Questions
6. "How many products do we sell?"
7. "Show me all products in the Electronics category"
8. "What's the price of the Laptop Pro 15?"
9. "Which products cost less than $50?"
10. "How many products are in stock?"

### Order Questions
11. "How many orders do we have?"
12. "Show me all completed orders"
13. "How many pending orders are there?"
14. "What orders were placed in January 2024?"
15. "Show me orders with status 'Shipped'"

## Intermediate Queries (Analysis)

### Sales Analysis
16. "What's the total revenue from all completed orders?"
17. "What's the average order value?"
18. "Show me the top 5 customers by total spending"
19. "Which region has the highest sales?"
20. "What's the total revenue by month?"

### Product Performance
21. "Which product has been sold the most?"
22. "Show me the top 10 products by revenue"
23. "What's the total revenue for Electronics category?"
24. "Which products have never been ordered?"
25. "What's the average quantity per order?"

### Customer Insights
26. "Which customer has placed the most orders?"
27. "Show me customers who have spent more than $5000"
28. "What's the average customer lifetime value?"
29. "Which region has the most customers?"
30. "Show me customers who haven't placed any orders"

## Advanced Queries (Complex Analysis)

### Trend Analysis
31. "Show me the sales trend from January to February 2024"
32. "Compare January sales with February sales"
33. "What's the month-over-month growth rate?"
34. "Which day of the week has the most orders?"
35. "Show me sales by region over time"

### Cross-Table Analysis
36. "Show me the most popular product in each region"
37. "What's the average order value by customer region?"
38. "Which products are frequently bought together?"
39. "Show me customer purchase patterns"
40. "What's the revenue contribution by product category?"

### Business Intelligence
41. "What percentage of orders are completed vs pending?"
42. "Show me the top 3 products by profit margin"
43. "Which customers contribute to 80% of revenue?" (Pareto analysis)
44. "What's the customer retention rate?"
45. "Show me seasonal trends in product sales"

## Chart-Specific Questions

### Bar Charts
46. "Show me a bar chart of sales by region"
47. "Create a bar chart of top 10 products by revenue"
48. "Show me a chart comparing order status distribution"

### Line Charts
49. "Show me a line chart of monthly sales trend"
50. "Create a line chart of customer signups over time"

### Pie Charts
51. "Show me a pie chart of revenue by product category"
52. "Create a pie chart of order status distribution"

## Cross-Source Questions (CSV + SQL)

If you also have a CSV file uploaded, try these:

53. "Compare sales.csv with the database sales"
54. "Is the CSV data consistent with the database?"
55. "Show me discrepancies between the CSV and database"
56. "Which source has higher total revenue?"
57. "Create a chart comparing both data sources"

## Specific to Test Database Schema

### Using Views
58. "Show me the sales summary by region"
59. "What are the top products based on total revenue?"

### Join Queries
60. "Show me all orders with customer names"
61. "List all order items with product names"
62. "Show me customers and their total number of orders"

### Aggregation
63. "What's the total quantity sold for each product?"
64. "Show me the average order value by region"
65. "What's the total revenue per customer?"

### Date-Based
66. "Show me orders from the last 30 days"
67. "What's the total revenue for February 2024?"
68. "Which month had the highest sales?"

### Filtering
69. "Show me orders over $2000"
70. "Which customers have email addresses ending in .com?"
71. "Show me products with stock less than 100"

## Testing SQL Agent Capabilities

### Natural Language Understanding
72. "Who are our biggest spenders?"
73. "What's selling well?"
74. "Are we running low on any products?"
75. "Which customers should we focus on?"

### Complex Conditions
76. "Show me customers from USA regions who have spent more than $3000"
77. "List products in Electronics category with price between $50 and $200"
78. "Show me completed orders from January with total over $2000"

### Calculations
79. "What's the profit margin on each product?" (if cost data available)
80. "Calculate the average items per order"
81. "What's the conversion rate from pending to completed?"

## Quick Verification Questions

### Data Validation
82. "How many records are in each table?"
83. "Are there any null values in customer emails?"
84. "Show me duplicate customer names"
85. "What's the date range of our orders?"

### Schema Understanding
86. "What tables are in the database?"
87. "Show me the structure of the orders table"
88. "What columns does the products table have?"

## Example Conversation Flow

**Start Simple:**
1. "How many customers do we have?" → Should return 10
2. "What's the total revenue?" → Should return ~$32,100

**Build Up:**
3. "Show me the top 5 customers by spending"
4. "Which region has the highest sales?"

**Get Insights:**
5. "Compare January and February sales"
6. "Show me a chart of sales by region"

**Cross-Source (if CSV uploaded):**
7. "Compare this with my sales.csv file"

## Expected Results (For Verification)

- **Total Customers**: 10
- **Total Products**: 10
- **Total Orders**: 15
- **Completed Orders**: 11
- **Total Revenue (Completed)**: $32,100
- **Regions**: 6 (North, South, East, West, Europe, Asia)
- **Product Categories**: Electronics, Accessories

## Tips for Best Results

1. **Be Specific**: "Show me top 5 customers" is better than "Show me customers"
2. **Use Natural Language**: The SQL Agent understands conversational queries
3. **Request Charts**: Add "show me a chart" or "create a bar chart" to visualize
4. **Compare Data**: Try cross-source queries if you have both CSV and SQL
5. **Ask Follow-ups**: Build on previous answers with related questions

## Testing the Orchestrator

To test the Orchestrator's routing logic:

1. **CSV Only**: "What's in my uploaded file?"
2. **SQL Only**: "What's in the database?"
3. **Both**: "Compare my file with the database"
4. **Specific**: "Show me sales from sales.csv and customers from the database"

Start with simple questions and gradually increase complexity to test the system's capabilities!
