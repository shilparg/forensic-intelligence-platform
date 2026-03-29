

WITH engine_a_text AS (
    SELECT * FROM `forensic-accounting-bot`.`forensic_data`.`stg_sec_filings`
),

engine_b_financials AS (
    SELECT * FROM `forensic-accounting-bot`.`forensic_data`.`stg_financials`
),

benfords_law AS (
    SELECT * FROM `forensic-accounting-bot`.`forensic_data`.`fct_benfords_law`
),

text_calculations AS (
    SELECT 
        a.ticker,
        a.fiscal_year,
        a.sentiment_score,
        a.similarity_index,
        -- 1. Disclosure Density (Word count vs Sentiment)
        SAFE_DIVIDE(ARRAY_LENGTH(SPLIT(a.filing_text, ' ')), ABS(a.sentiment_score)) AS density_index,
        
        -- 2. Sentiment Volatility (Looking at standard deviation for the ticker over a trailing 3-year window)
        COALESCE(STDDEV_SAMP(a.sentiment_score) OVER (
            PARTITION BY a.ticker 
            ORDER BY a.fiscal_year 
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ), 0.0) AS sentiment_volatility,
        
        -- 3. Narrative Drift (YoY Similarity Change)
        COALESCE(a.similarity_index - LAG(a.similarity_index) OVER (
            PARTITION BY a.ticker ORDER BY a.fiscal_year
        ), 0.0) AS similarity_drift,

        -- Standard word count to maintain compatibility with the Streamlit narrative drift visualization
        ARRAY_LENGTH(SPLIT(a.filing_text, ' ')) AS word_count

    FROM engine_a_text a
)

SELECT 
    t.*,
    COALESCE(b.benfords_deviation, 0.0) AS benfords_deviation,
    COALESCE(f.short_ratio, 0.0) AS short_ratio,
    COALESCE(f.debt_to_equity, 0.0) AS debt_to_equity,
    COALESCE(f.return_on_equity, 0.0) AS return_on_equity,
    COALESCE(f.operating_margin, 0.0) AS operating_margin,
    COALESCE(f.held_institutions, 0.0) AS held_institutions,
    COALESCE(f.insider_ownership, 0.0) AS insider_ownership,
    COALESCE(f.current_ratio, 0.0) AS current_ratio,
    COALESCE(f.quick_ratio, 0.0) AS quick_ratio,
    COALESCE(f.revenue_growth, 0.0) AS revenue_growth,
    COALESCE(f.earnings_growth, 0.0) AS earnings_growth,
    COALESCE(f.profit_margins, 0.0) AS profit_margins,
    COALESCE(f.free_cashflow, 0.0) AS free_cashflow
FROM text_calculations t
-- Join the Benfords Math exactly on same year
LEFT JOIN benfords_law b 
    ON t.ticker = b.ticker AND t.fiscal_year = b.fiscal_year
-- Join the point-in-time Market Financials across all years for that ticker
LEFT JOIN engine_b_financials f 
    ON t.ticker = f.ticker