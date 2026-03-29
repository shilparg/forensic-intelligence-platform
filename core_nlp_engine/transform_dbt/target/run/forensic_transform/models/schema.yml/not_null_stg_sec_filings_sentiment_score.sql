
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select sentiment_score
from `forensic-accounting-bot-491604`.`forensic_data`.`stg_sec_filings`
where sentiment_score is null



  
  
      
    ) dbt_internal_test