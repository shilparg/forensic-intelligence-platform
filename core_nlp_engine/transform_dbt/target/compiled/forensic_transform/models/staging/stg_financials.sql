

WITH raw_financials AS (
    SELECT * FROM `forensic-accounting-bot-491604`.`raw_sec_landing`.`raw_financials`
)

SELECT
    UPPER(CAST(ticker AS STRING)) AS ticker,
    CAST(short_ratio AS FLOAT64) AS short_ratio,
    CAST(debt_to_equity AS FLOAT64) AS debt_to_equity,
    CAST(return_on_equity AS FLOAT64) AS return_on_equity,
    CAST(operating_margin AS FLOAT64) AS operating_margin,
    CAST(held_institutions AS FLOAT64) AS held_institutions,
    CAST(insider_ownership AS FLOAT64) AS insider_ownership,
    CAST(current_ratio AS FLOAT64) AS current_ratio,
    CAST(quick_ratio AS FLOAT64) AS quick_ratio,
    CAST(revenue_growth AS FLOAT64) AS revenue_growth,
    CAST(earnings_growth AS FLOAT64) AS earnings_growth,
    CAST(profit_margins AS FLOAT64) AS profit_margins,
    CAST(free_cashflow AS FLOAT64) AS free_cashflow
FROM raw_financials
WHERE ticker IS NOT NULL