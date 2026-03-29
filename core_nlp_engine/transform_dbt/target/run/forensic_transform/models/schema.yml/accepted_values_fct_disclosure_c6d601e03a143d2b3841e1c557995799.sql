select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

with all_values as (

    select
        forensic_label as value_field,
        count(*) as n_records

    from `forensic-accounting-bot`.`forensic_data`.`fct_disclosure_density`
    group by forensic_label

)

select *
from all_values
where value_field not in (
    'NORMAL','HIGH NEGATIVE RISK','POTENTIAL OBFUSCATION'
)



      
    ) dbt_internal_test