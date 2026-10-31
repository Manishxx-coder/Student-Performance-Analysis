import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

st.set_page_config(page_title="Student Performance Big Data Analysis", page_icon="🎓", layout="wide")
st.title("🎓 Student Performance Analysis")
st.caption("Big Data mini-project using Python, PySpark, Pandas, and Streamlit")

st.info("Upload a CSV with columns: student_id, name, mathematics, science, english. "
        "PySpark processes the records; Streamlit displays the results.")

@st.cache_resource
def get_spark():
    return (SparkSession.builder
            .appName("StudentPerformanceAnalysis")
            .master("local[*]")
            .config("spark.ui.showConsoleProgress", "false")
            .getOrCreate())

uploaded = st.file_uploader("Upload student CSV", type=["csv"])
sample_path = "data/students.csv"
use_sample = st.checkbox("Use included sample dataset", value=True)

if uploaded is not None:
    pdf = pd.read_csv(uploaded)
    source_name = uploaded.name
elif use_sample:
    pdf = pd.read_csv(sample_path)
    source_name = "data/students.csv"
else:
    st.warning("Upload a CSV or select the sample dataset.")
    st.stop()

required = ["student_id", "name", "mathematics", "science", "english"]
missing = [c for c in required if c not in pdf.columns]
if missing:
    st.error("Missing required columns: " + ", ".join(missing))
    st.stop()

for c in ["student_id", "mathematics", "science", "english"]:
    pdf[c] = pd.to_numeric(pdf[c], errors="coerce")
pdf = pdf.dropna(subset=required).copy()
if pdf.empty:
    st.error("No valid records found in the CSV.")
    st.stop()

spark = get_spark()
schema = StructType([
    StructField("student_id", IntegerType(), False),
    StructField("name", StringType(), False),
    StructField("mathematics", IntegerType(), False),
    StructField("science", IntegerType(), False),
    StructField("english", IntegerType(), False),
])
records = [(int(r.student_id), str(r.name), int(r.mathematics), int(r.science), int(r.english))
           for r in pdf[required].itertuples(index=False)]
sdf = spark.createDataFrame(records, schema=schema)

analyzed = (sdf
    .withColumn("total", F.col("mathematics") + F.col("science") + F.col("english"))
    .withColumn("average", F.round(F.col("total") / F.lit(3.0), 2))
    .withColumn("grade",
        F.when(F.col("average") >= 90, "A")
         .when(F.col("average") >= 75, "B")
         .when(F.col("average") >= 60, "C")
         .when(F.col("average") >= 40, "D")
         .otherwise("F")))

result = analyzed.orderBy(F.desc("average")).toPandas()
subject_avg = analyzed.agg(
    F.round(F.avg("mathematics"), 2).alias("Mathematics"),
    F.round(F.avg("science"), 2).alias("Science"),
    F.round(F.avg("english"), 2).alias("English")
).toPandas().iloc[0]

c1, c2, c3 = st.columns(3)
c1.metric("Students analyzed", f"{len(result):,}")
c2.metric("Overall average", f"{result['average'].mean():.2f}")
c3.metric("Top performer", str(result.iloc[0]["name"]))

st.subheader("Student results (ranked by average)")
st.dataframe(result, use_container_width=True, hide_index=True)

st.subheader("Subject-wise average marks")
chart_data = pd.DataFrame({"Subject": subject_avg.index, "Average marks": subject_avg.values})
st.bar_chart(chart_data, x="Subject", y="Average marks", y_label="Average marks")

st.subheader("High performers (average ≥ 75)")
high = result[result["average"] >= 75]
st.dataframe(high, use_container_width=True, hide_index=True)

csv_bytes = result.to_csv(index=False).encode("utf-8")
st.download_button("Download analyzed results (CSV)", data=csv_bytes,
                   file_name="student_performance_results.csv", mime="text/csv")

st.caption(f"Data source: {source_name}. This is a local demonstration using Spark local mode, not a multi-node cluster.")
