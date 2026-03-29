
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select ticker
from `forensic-accounting-bot-491604`.`forensic_data`.`int_forensic_metrics`
where ticker is null



  
  
      
    ) dbt_internal_test