select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select sentiment_volatility
from `forensic-accounting-bot`.`forensic_data`.`int_forensic_metrics`
where sentiment_volatility is null



      
    ) dbt_internal_test