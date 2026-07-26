import streamlit as st
from datetime import datetime
from components.navbar import render_navbar
from components.charts import area_chart, donut_chart
from utils.dashboard_data import load_orders, compute_kpis, revenue_trend, sales_by_category
from utils.ml_cache import cached_segments
from utils.insights_data import generate_all_insights
from utils.ai_narrative import generate_narrative
from utils.export_csv import orders_to_csv, segments_to_csv
from utils.export_excel import build_excel_report
from utils.export_pdf import build_pdf_report

render_navbar()
st.markdown("## Reports")
st.caption("Export real Nova Commerce data as CSV, Excel, or PDF.")

df = load_orders()
kpis = compute_kpis(df)
rfm, summary = cached_segments(df)

today_str = datetime.now().strftime("%Y-%m-%d")

st.markdown("#### CSV Export")
c1, c2 = st.columns(2)
with c1:
    st.download_button(
        "⬇️ Download Sales Data (CSV)",
        data=orders_to_csv(df),
        file_name=f"nova_commerce_sales_{today_str}.csv",
        mime="text/csv",
        use_container_width=True,
    )
with c2:
    st.download_button(
        "⬇️ Download Customer Segments (CSV)",
        data=segments_to_csv(rfm),
        file_name=f"nova_commerce_segments_{today_str}.csv",
        mime="text/csv",
        use_container_width=True,
    )

st.markdown("---")
st.markdown("#### Excel Export")
st.caption("Multi-sheet workbook: Executive Summary, Sales Detail, Customer Segments.")

if st.button("Generate Excel Report"):
    with st.spinner("Building workbook..."):
        sales_report_cols = [
            "order_id", "order_purchase_timestamp", "order_status", "nova_category",
            "customer_state", "payment_type", "payment_value", "freight_value",
            "delivery_days", "is_delayed",
        ]
        sales_export_df = df[sales_report_cols].copy()
        sales_export_df.columns = [
            "Order ID", "Purchase Date", "Status", "Category", "State",
            "Payment Type", "Payment Value", "Freight Value", "Delivery Days", "Delayed",
        ]
        excel_bytes = build_excel_report(kpis, sales_export_df, rfm)
    st.download_button(
        "⬇️ Download Excel Report",
        data=excel_bytes,
        file_name=f"nova_commerce_report_{today_str}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )

st.markdown("---")
st.markdown("#### PDF Export")
st.caption("Branded executive report with KPIs, AI narrative, and key charts.")

if st.button("Generate PDF Report"):
    with st.spinner("Building PDF (rendering charts, this may take a few seconds)..."):
        trend = revenue_trend(df)
        cat = sales_by_category(df)
        rev_fig = area_chart(trend["order_month"], trend["payment_value"])
        cat_fig = donut_chart(cat["nova_category"], cat["payment_value"])

        insights = generate_all_insights(df)
        narrative = generate_narrative(insights) or " ".join(i["text"] for i in insights)

        pdf_bytes = build_pdf_report(kpis, rev_fig, cat_fig, narrative)

    st.download_button(
        "⬇️ Download PDF Report",
        data=pdf_bytes,
        file_name=f"nova_commerce_report_{today_str}.pdf",
        mime="application/pdf",
        use_container_width=True,
    )