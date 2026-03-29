select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select forensic_label
from `forensic-accounting-bot`.`forensic_data`.`fct_disclosure_density`
where forensic_label is null



      
    ) dbt_internal_test