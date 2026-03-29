select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select fiscal_year
from `forensic-accounting-bot`.`forensic_data`.`int_forensic_metrics`
where fiscal_year is null



      
    ) dbt_internal_test