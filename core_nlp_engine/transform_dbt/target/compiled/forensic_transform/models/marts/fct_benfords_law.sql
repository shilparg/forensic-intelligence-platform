

WITH extracted_digits AS (
    SELECT 
        ticker,
        fiscal_year,
        CAST(digit AS INT64) as leading_digit
    FROM `forensic-accounting-bot-491604`.`forensic_data`.`stg_sec_filings`,
    -- The core mathematical extraction engine: Grabs the leading digit of ANY number mentioned in the 10-K
    UNNEST(REGEXP_EXTRACT_ALL(filing_text, r'\b([1-9])\d*')) AS digit
),

digit_counts AS (
    SELECT 
        ticker,
        fiscal_year,
        leading_digit,
        COUNT(*) as digit_freq
    FROM extracted_digits
    WHERE leading_digit > 0 AND leading_digit < 10
    GROUP BY ticker, fiscal_year, leading_digit
),

total_counts AS (
    SELECT 
        ticker,
        fiscal_year,
        SUM(digit_freq) as total_digits
    FROM digit_counts
    GROUP BY ticker, fiscal_year
),

benfords_distribution AS (
    SELECT
        d.ticker,
        d.fiscal_year,
        d.leading_digit,
        d.digit_freq,
        t.total_digits,
        -- Calculate actual frequency % vs expected mathematical curve
        SAFE_DIVIDE(d.digit_freq, t.total_digits) AS actual_distribution,
        LOG10(1 + 1/CAST(d.leading_digit AS FLOAT64)) AS expected_distribution
    FROM digit_counts d
    JOIN total_counts t ON d.ticker = t.ticker AND d.fiscal_year = t.fiscal_year
)

SELECT
    ticker,
    fiscal_year,
    -- A higher sum means the actual numbers deviate further from Benford's biological logarithmic curve (Huge Fraud Risk!)
    SUM(ABS(actual_distribution - expected_distribution)) as benfords_deviation
FROM benfords_distribution
WHERE total_digits > 100 -- Ensure statistical significance of the sample size
GROUP BY ticker, fiscal_year