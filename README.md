# 🛍️ Customer Segmentation using Machine Learning

## 📌 Overview

This project aims to segment customers based on their **demographic, behavioral**, and **purchase history** using unsupervised machine learning techniques. By identifying distinct customer groups, businesses can personalize marketing strategies, optimize promotions, and improve customer engagement.

---

## 📂 Dataset

* **Source:** [Marketing Campaign Dataset](https://www.kaggle.com/datasets/rodsaldanha/arketing-campaign)
* **Rows:** 2,240+
* **Type:** Unsupervised (Clustering)
* **Goal:** Identify **customer personas** using clustering algorithms.

### **Features:**

| Feature                                   | Description                           |
| ----------------------------------------- | ------------------------------------- |
| ID                                        | Unique customer ID                    |
| Year\_Birth                               | Year of birth                         |
| Education                                 | Education level                       |
| Marital\_Status                           | Marital status                        |
| Income                                    | Yearly income of the customer         |
| Kidhome, Teenhome                         | Number of kids/teens in household     |
| Dt\_Customer                              | Customer enrollment date              |
| Recency                                   | Days since last purchase              |
| MntWines, ..., MntGoldProds               | Amount spent on various products      |
| NumDealsPurchases, ..., NumWebVisitsMonth | Customer purchase behavior            |
| AcceptedCmp1–5                            | Whether campaign offers were accepted |
| Complain                                  | If customer ever complained           |
| Z\_CostContact, Z\_Revenue                | Constant values (can be dropped)      |
| Response                                  | Response to last campaign             |

---

## ⚙️ Project Workflow

1️⃣ **Data Preprocessing**

* Handling missing values (e.g., Income)
* Converting date fields
* Creating meaningful features (e.g., Age, total kids, total spend)
* One-hot encoding categorical variables
* Scaling numerical features
* Removing low-variance or constant columns

2️⃣ **Exploratory Data Analysis (EDA)**

* Customer demographics distributions
* Spending patterns by segments
* Correlation heatmaps
* Purchase behavior visualization

3️⃣ **Feature Engineering**

* `Age` = current year - `Year_Birth`
* `TotalChildren` = `Kidhome` + `Teenhome`
* `TotalSpend` = sum of all `Mnt*` columns
* `CustomerTenure` from `Dt_Customer`

4️⃣ **Clustering Algorithms**

* **KMeans** (primary)
* DBSCAN / Agglomerative Clustering (optional comparison)
* **Elbow Method** and **Silhouette Score** used for optimal cluster count

5️⃣ **Model Evaluation**

* Internal metrics: **Silhouette Score**, **Inertia**
* Visualizations: PCA/TSNE plots for cluster separation
* Business validation: interpreting cluster characteristics

6️⃣ **Cluster Profiling**

* Analyze clusters by:

  * Age groups
  * Income levels
  * Product preferences
  * Response to campaigns
* Assign cluster labels (e.g., “Luxury Shopper”, “Discount Seeker”)

---

## 📊 Sample Results

| Cluster | Key Characteristics                       |
| ------- | ----------------------------------------- |
| 0       | High income, frequent online shoppers     |
| 1       | Low income, price-sensitive, promo-driven |
| 2       | Middle-aged, store-preferred, loyal       |
| 3       | Young, low spend, low engagement          |

---

## 🛠 Tech Stack

* **Languages & Libraries:** Python, Pandas, NumPy, Scikit-learn
* **Visualization:** Matplotlib, Seaborn, Plotly
* **Web Framework:** FastAPI (for UI & API interaction)
* **Cloud Services:** AWS S3 (for storing models/data)
* **Containerization:** Docker
* **CI/CD:** GitHub Actions
* **Model Deployment:** AWS EC2

---

## 🚀 How to Run

```bash
git clone https://github.com/your-username/customer-segmentation.git
cd customer-segmentation
pip install -r requirements_dev.txt

# Run training
python main.py

# Run FastAPI app
uvicorn app:app --reload
```

You can create a global (project-specific) environment like this:
```
conda env create -f environment.yaml
```

You can create a local (project-specific) environment like this:

```
conda env create --prefix ./venv -f environment.yaml
```

To activate the local environment:

```
conda activate ./env
```


---

## 🛰️ Deployment Plan

The model is deployed as a **REST API** using **FastAPI**, containerized with Docker and hosted on **AWS EC2**.

### ⚙️ Deployment Stack

* **FastAPI** → REST API serving cluster predictions
* **AWS S3** → Store trained model artifacts
* **AWS ECR** → Docker image repository
* **AWS EC2** → Host the web app and API
* **GitHub Actions** → Automate build & deploy pipeline
* **Docker** → Containerize training and inference services

### ✅ CI/CD Workflow

1. **Push code to GitHub** → Triggers CI/CD
2. **GitHub Actions:**

   * Run unit tests with `pytest`
   * Build Docker image
   * Push image to AWS ECR
   * Deploy to AWS EC2
3. **FastAPI API** → `/predict` endpoint returns cluster ID for customer input
4. **Model artifacts** → Loaded from AWS S3 at runtime

![Deployment-Architecture](/docs/AWS-CI:CD.jpg)

---

<!-- ## 🧪 Testing

* Unit tests using **pytest**
* Test FastAPI endpoints with **pytest + HTTPX**
* Model outputs validated via clustering metrics and manual sanity checks

--- -->

## 📧 Contact

For questions or collaboration:

📧 [rahulshelke3399@gmail.com](mailto:rahulshelke3399@gmail.com)
🔗 [LinkedIn](https://www.linkedin.com/in/rahulshelke981)