# Data Analyst AI Agent - Testing Guide 🧪

This guide helps you verify all features of the Data Analyst AI Agent, including the new Charting capabilities.

## 1. Prerequisites
Ensure all three services are running in separate terminals:
1.  **React Frontend**: `npm run dev` (http://localhost:5173)
2.  **Spring Backend**: `./mvnw spring-boot:run` (http://localhost:8080)
3.  **Python AI Service**: `python app.py` (http://localhost:5000)

## 2. Test Data
We have created a complex dataset for you: `complex_retail_data.csv` (Located in project root).
It contains:
-   **Sales Transactions**: Revenue, Units Sold, Unit Price
-   **Categories**: Electronics, Clothing, Home, Garden
-   **Locations**: New York, Los Angeles, Chicago, etc.
-   **Time Series**: Dates from Jan to March 2024

## 3. Step-by-Step Test Scenario

### Step A: Upload & Processing
1.  Open the Dashboard: [http://localhost:5173/dashboard](http://localhost:5173/dashboard)
2.  Click the upload box.
3.  Select `complex_retail_data.csv`.
4.  **Observe**: Status should go from "Processing..." to ✅ automatically (approx. 5-10 seconds).
5.  Click **"Open Chat"**.

### Step B: General Analysis (Text)
Ask these questions to verify the AI understands the data structure:
*   *"What columns are in this dataset?"*
*   *"What is the total revenue generated across all stores?"*
*   *"Which product category has the highest average customer rating?"*

### Step C: Charting & Visualization 📊
Ask these specific questions to trigger the new Chart Renderer:

**1. Bar Chart**
> "Show me a bar chart of Total Revenue by Category."
*(Expect: A bar chart comparing Electronics, Clothing, etc.)*

**2. Pie Chart**
> "Show me a pie chart of Units Sold by Store Location."
*(Expect: A circular chart showing market share of each city.)*

**3. Line Chart (Trend)**
> "Show me a line chart of Total Revenue over Date."
*(Expect: A time-series graph showing sales trends from Jan to March.)*

### Step D: Complex Queries
*   *"Compare the sales performance of New York vs Los Angeles using a chart."*
*   *"What is the return rate for Electronics? Show me the data."*

## Troubleshooting
-   **Charts not showing?** Ensure specific keywords like "chart", "graph", or "visualize" are in your query.
-   **Processing stuck?** Check the Python terminal for errors.
-   **"Upload Failed"?** Ensure the Backend is running and connected to Firebase.
