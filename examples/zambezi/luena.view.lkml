
view: LUEANA_LATEST { 
  sql_table_name: "CIMPRESS"."ZAMBEZI"."LUENA" ;;

  dimension: category {
    description: "Category"
    type: string
    sql: ${TABLE}."JSON":"category"::string ;;
  }
    
  dimension: id {
    description: "Id"
    primary_key: yes
    type: string
    sql: ${TABLE}."JSON":"_datalakeMetadata":"id"::string ;;
    group_label:"_datalakeMetadata"
  }
    
  dimension: is_active {
    description: "Is Active"
    type: yesno
    sql: ${TABLE}."JSON":"isActive"::boolean ;;
  }
    
  dimension: mcpsku {
    description: "Mcpsku"
    type: string
    sql: ${TABLE}."JSON":"mcpSKU"::string ;;
  }
    
  dimension: price {
    description: "Price"
    type: string
    sql: ${TABLE}."JSON":"price"::string ;;
  }
    
  dimension: principal {
    description: "Principal"
    type: string
    sql: ${TABLE}."JSON":"_datalakeMetadata":"principal"::string ;;
    group_label:"_datalakeMetadata"
  }
    
  dimension: stream_id {
    description: "Stream Id"
    type: string
    sql: ${TABLE}."JSON":"_datalakeMetadata":"streamId"::string ;;
    group_label:"_datalakeMetadata"
  }
    
  dimension: transaction_id {
    description: "Transaction Id"
    type: string
    sql: ${TABLE}."JSON":"transactionId"::string ;;
  }
    
  dimension_group: modified {
    description: "Modified"
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
    sql: ${TABLE}."JSON":"modified"::timestamp ;;
  }
    
  dimension_group: received {
    description: "Received"
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
    sql: ${TABLE}."JSON":"_datalakeMetadata":"received"::timestamp ;;
  }
    
}

view: fulfillerlist { 

  dimension: fulfiller {
    description: "Fulfiller"
    type: string
    sql: ${TABLE}.VALUE:"fulfiller"::string ;;
  }
    
}
