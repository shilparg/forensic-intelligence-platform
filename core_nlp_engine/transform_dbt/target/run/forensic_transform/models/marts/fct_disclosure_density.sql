
  
    

    create or replace table `forensic-accounting-bot`.`forensic_data`.`fct_disclosure_density`
      
    
    

    OPTIONS()
    as (
      

WITH unified_metrics AS (
    -- We reference the fully joined Hub we built in Phase 2
    SELECT * FROM `forensic-accounting-bot`.`forensic_data`.`int_forensic_metrics`
)

SELECT
    *,
    -- The 'Red Flag' Logic (The most important part for your text audit)
    CASE 
        WHEN word_count > 15000 AND sentiment_score < 0 THEN 'POTENTIAL OBFUSCATION'
        WHEN sentiment_score < -0.2 THEN 'HIGH NEGATIVE RISK'
        ELSE 'NORMAL'
    END AS forensic_label
FROM unified_metrics
    );
  