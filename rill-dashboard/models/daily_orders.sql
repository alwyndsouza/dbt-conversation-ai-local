-- @materialize: true
SELECT
  *
FROM read_parquet('data/fct_daily_orders.parquet')
ORDER BY order_date
