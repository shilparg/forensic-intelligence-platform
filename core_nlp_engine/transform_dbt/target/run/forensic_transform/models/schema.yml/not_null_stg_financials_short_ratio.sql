select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select short_ratio
from `forensic-accounting-bot`.`forensic_data`.`stg_financials`
where short_ratio is null



      
    ) dbt_internal_test