select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select ticker
from `forensic-accounting-bot`.`forensic_data`.`stg_financials`
where ticker is null



      
    ) dbt_internal_test