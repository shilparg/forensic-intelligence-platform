select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select ticker
from `forensic-accounting-bot`.`forensic_data`.`stg_sec_filings`
where ticker is null



      
    ) dbt_internal_test