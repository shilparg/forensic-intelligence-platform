{{ config(materialized='table') }}

WITH unified_metrics AS (
    -- We reference the fully joined Hub we built in Phase 2
    SELECT * FROM {{ ref('int_forensic_metrics') }}
)

SELECT
    *
FROM unified_metrics