# InsightForge — Processed Data Dictionary


## geo_master.parquet

Rows: 19015 | Columns: 5

| Column | Dtype | Non-null % |
|---|---|---|
| geolocation_zip_code_prefix | int64 | 100.0% |
| geolocation_lat | float64 | 100.0% |
| geolocation_lng | float64 | 100.0% |
| geolocation_city | object | 100.0% |
| geolocation_state | object | 100.0% |

## orders_master.parquet

Rows: 113425 | Columns: 28

| Column | Dtype | Non-null % |
|---|---|---|
| order_id | object | 100.0% |
| customer_id | object | 100.0% |
| order_status | object | 100.0% |
| order_purchase_timestamp | datetime64[ns] | 100.0% |
| order_approved_at | datetime64[ns] | 99.9% |
| order_delivered_carrier_date | datetime64[ns] | 98.3% |
| order_delivered_customer_date | datetime64[ns] | 97.2% |
| order_estimated_delivery_date | datetime64[ns] | 100.0% |
| order_item_id | float64 | 99.3% |
| product_id | object | 99.3% |
| seller_id | object | 99.3% |
| shipping_limit_date | object | 99.3% |
| price | float64 | 99.3% |
| freight_value | float64 | 99.3% |
| nova_category | object | 99.3% |
| product_weight_g | float64 | 99.3% |
| payment_value | float64 | 100.0% |
| payment_installments | float64 | 100.0% |
| payment_type | object | 100.0% |
| customer_unique_id | object | 100.0% |
| customer_zip_code_prefix | int64 | 100.0% |
| customer_city | object | 100.0% |
| customer_state | object | 100.0% |
| delivery_days | float64 | 97.2% |
| is_delayed | bool | 100.0% |
| profit_estimate | float64 | 99.3% |
| order_month | object | 100.0% |
| order_quarter | object | 100.0% |

## products_master.parquet

Rows: 32951 | Columns: 11

| Column | Dtype | Non-null % |
|---|---|---|
| product_id | object | 100.0% |
| product_category_name | object | 98.1% |
| product_name_lenght | float64 | 98.1% |
| product_description_lenght | float64 | 98.1% |
| product_photos_qty | float64 | 98.1% |
| product_weight_g | float64 | 100.0% |
| product_length_cm | float64 | 100.0% |
| product_height_cm | float64 | 100.0% |
| product_width_cm | float64 | 100.0% |
| product_category_name_english | object | 98.1% |
| nova_category | object | 100.0% |

## reviews_master.parquet

Rows: 98410 | Columns: 7

| Column | Dtype | Non-null % |
|---|---|---|
| review_id | object | 100.0% |
| order_id | object | 100.0% |
| review_score | int64 | 100.0% |
| review_comment_title | object | 11.7% |
| review_comment_message | object | 41.3% |
| review_creation_date | datetime64[ns] | 100.0% |
| review_answer_timestamp | datetime64[ns] | 100.0% |