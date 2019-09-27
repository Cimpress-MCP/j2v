
view: JSON_TABLE { 
  sql_table_name: parking_table ;;

  dimension: api_version {
    description: "Api Version"
    type: string
    sql: ${TABLE}."data_column":"apiVersion"::string ;;
  }
    
  dimension: client {
    description: "Client"
    type: string
    sql: ${TABLE}."data_column":"client"::string ;;
  }
    
  dimension: data_provider {
    description: "Data Provider"
    type: string
    sql: ${TABLE}."data_column":"dataProvider"::string ;;
  }
    
  dimension: payload_primary_key_value {
    description: "Payload Primary Key Value"
    type: string
    sql: ${TABLE}."data_column":"payloadPrimaryKeyValue"::string ;;
  }
    
  dimension_group: data_generation_timestamp {
    description: "Data Generation Timestamp"
    type: time
    timeframes: [
        raw,
        time,
        date,
        week,
        month,
        quarter,
        year
    ]
    sql: ${TABLE}."data_column":"dataGenerationTimestamp"::timestamp ;;
  }
    
}
