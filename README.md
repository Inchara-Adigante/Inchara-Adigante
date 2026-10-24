<h1 align="center">Hi, I'm Inchara Adigante 👋</h1>

<p align="center">
  <b>Data & Machine Learning Engineer</b> · Northeastern University · Boston, MA (open to relocation)
</p>

<p align="center">
  <a href="https://linkedin.com/in/incharaadigante"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
  <a href="mailto:adiganteinchara@gmail.com"><img src="https://img.shields.io/badge/Email-EA4335?style=flat&logo=gmail&logoColor=white" alt="Email"></a>
  <a href="https://github.com/Inchara-Adigante"><img src="https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white" alt="GitHub"></a>
</p>

---

### About me

I'm a data engineer who builds platforms end to end: from raw, messy source data to trusted warehouse tables, then to the dashboards, models and AI assistants that people use to make decisions. I care about the unglamorous parts that make data reliable: incremental loads that match a full rebuild, quality gates that stop bad data before it's published, and pipelines that are safe to re-run.

- 🏗️ **Data engineering:** PySpark batch and Structured Streaming, data lakes on S3, star schemas with SCD Type 2, incremental loads and backfills, Airflow orchestration
- ✅ **Data quality & reliability:** write-audit-publish, automated quality checks, exactly-once streaming sinks, monitoring and runbooks
- 🤖 **ML & AI:** TensorFlow, scikit-learn, reliability analysis, LLM agents with tool use and grounded, cited answers
- ☁️ **Cloud & DevOps:** AWS (S3, Glue, Athena, Redshift) infrastructure as code, GCP, Azure, Terraform, Docker, CI/CD with GitHub Actions
- 📊 **Analytics:** SQL, DuckDB, Power BI (DAX), Streamlit, Splunk
- 📫 Open to **Data Engineer, Analytics Engineer and ML Engineer** roles

---

### Featured projects

#### 🛒 [ShopSense AI: Retail Intelligence and Real-Time Data Platform](https://github.com/Inchara-Adigante/Shopsense-AI)
A retail data platform that answers one business question: *which products will run out of stock, what is driving their demand, and what should the business do?* It runs from six months of simulated retail data through an S3-style lake, PySpark transformations and a star-schema warehouse, to a dashboard and an AI assistant.
- Incremental processing with write-audit-publish and 67 quality checks; an incremental build is **identical to a full rebuild** across all 10 warehouse tables
- SCD Type 2 dimensions with point-in-time lookups, so **100% of order lines** carry the price that was valid on their order date
- Spark Structured Streaming with watermarks and an exactly-once sink: **0 events lost or double-counted**, even after killing the job mid-stream
- AI assistant that answers from the warehouse through read-only SQL tools, cites the rows behind every number, and flags invented figures
- AWS infrastructure in Terraform (S3, Glue, Athena, Redshift Serverless), with CI on GitHub Actions

`PySpark` `Spark Streaming` `SQL` `DuckDB` `Airflow` `AWS` `Terraform` `Streamlit` `Claude API`

#### ⚡ [EV Reliability Intelligence & Failure Prediction Platform](https://github.com/Inchara-Adigante/ev-reliability-platform)
An end-to-end reliability analytics platform for a simulated fleet of 2,000 EVs. It runs from data generation through validation, a SQL Server warehouse, Weibull reliability analysis and a TensorFlow model that predicts component failures in the next 90 days.
- Validation and transformation pipeline that rejects bad records with reasons and logs every load to a `pipeline_log` table
- Censored Weibull fits that classify each component as infant mortality, random or wear-out
- Failure-risk model whose **High-risk tier holds 4.6% of components but catches 34% of failures (7.5× lift)**
- Power BI DAX measures and Splunk alerts for pipeline health, data quality and new high-risk parts

`Python` `SQL Server` `TensorFlow` `scikit-learn` `SciPy` `Power BI (DAX)` `Splunk` `Docker`

#### 🎯 [Jobzilla AI: AI-Powered Job Application Intelligence](https://github.com/Inchara-Adigante/JobzillaAI)
*Team project (3 people).* An application where AI agents debate how well your profile fits a job, then tailor your resume and cover letter. It uses semantic job matching, LangGraph multi-agent orchestration, MCP servers for GitHub and job-market context, and scheduled Airflow pipelines, deployed with CI/CD on GCP Cloud Run.

`Python` `LangGraph` `FastAPI` `Streamlit` `Pinecone` `PostgreSQL` `Airflow` `GCP`

---

### Tech stack

**Languages:** ![Python](https://img.shields.io/badge/Python-3670A0?style=flat&logo=python&logoColor=ffdd54) ![SQL](https://img.shields.io/badge/SQL-CC2927?style=flat&logo=microsoftsqlserver&logoColor=white) ![Go](https://img.shields.io/badge/Go-00ADD8?style=flat&logo=go&logoColor=white) ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)

**Data & ML:** ![Apache Spark](https://img.shields.io/badge/Apache%20Spark-E25A1C?style=flat&logo=apachespark&logoColor=white) ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white) ![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white) ![SciPy](https://img.shields.io/badge/SciPy-0C55A5?style=flat&logo=scipy&logoColor=white) ![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat&logo=scikit-learn&logoColor=white) ![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=flat&logo=tensorflow&logoColor=white) ![MLflow](https://img.shields.io/badge/MLflow-0194E2?style=flat&logo=mlflow&logoColor=white) ![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=flat)

**Databases:** ![SQL Server](https://img.shields.io/badge/SQL%20Server-CC2927?style=flat&logo=microsoftsqlserver&logoColor=white) ![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white) ![Cassandra](https://img.shields.io/badge/Cassandra-1287B1?style=flat&logo=apachecassandra&logoColor=white) ![DuckDB](https://img.shields.io/badge/DuckDB-FFF000?style=flat&logo=duckdb&logoColor=black) ![Amazon Redshift](https://img.shields.io/badge/Redshift-8C4FFF?style=flat&logo=amazonredshift&logoColor=white)

**Pipelines & DevOps:** ![Airflow](https://img.shields.io/badge/Airflow-017CEE?style=flat&logo=apacheairflow&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white) ![Terraform](https://img.shields.io/badge/Terraform-844FBA?style=flat&logo=terraform&logoColor=white) ![Jenkins](https://img.shields.io/badge/Jenkins-D24939?style=flat&logo=jenkins&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat&logo=githubactions&logoColor=white) ![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=flat&logo=selenium&logoColor=white)

**Cloud:** ![GCP](https://img.shields.io/badge/Google%20Cloud-4285F4?style=flat&logo=googlecloud&logoColor=white) ![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat&logo=amazonwebservices&logoColor=white) ![Azure](https://img.shields.io/badge/Azure-0078D4?style=flat&logo=microsoftazure&logoColor=white) ![Netlify](https://img.shields.io/badge/Netlify-00C7B7?style=flat&logo=netlify&logoColor=white)

**Analytics & Monitoring:** ![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=flat&logo=powerbi&logoColor=black) ![Splunk](https://img.shields.io/badge/Splunk-000000?style=flat&logo=splunk&logoColor=white) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)

---

### GitHub stats

<p align="center">
  <img height="165" src="https://github-readme-stats.shion.dev/api?username=Inchara-Adigante&theme=transparent&hide_border=true&show_icons=true" alt="GitHub stats">
  <img height="165" src="https://streak-stats.demolab.com/?user=Inchara-Adigante&theme=transparent&hide_border=true" alt="GitHub streak">
</p>
