
view: LUEANA_LATEST { 
  sql_table_name: "CIMPRESS"."ZAMBEZI"."LUENA" ;;

  dimension: category {
    description: "Category"
    type: string
    sql: ${TABLE}."JSON":"category"::string ;;
  }
    
  dimension: mcpsku {
    description: "Mcpsku"
    type: string
    sql: ${TABLE}."JSON":"mcpSKU"::string ;;
  }
    
  dimension: modified {
    description: "Modified"
    type: date_time
    sql: ${TABLE}."JSON":"modified"::string ;;
  }
    
  dimension: transaction_id {
    description: "Transaction Id"
    type: string
    sql: ${TABLE}."JSON":"transactionId"::string ;;
  }
    
  dimension: principal {
    description: "Principal"
    type: string
    sql: ${TABLE}."JSON":"_datalakeMetadata":"principal"::string ;;
  }
    
  dimension: stream_id {
    description: "Stream Id"
    type: string
    sql: ${TABLE}."JSON":"_datalakeMetadata":"streamId"::string ;;
  }
    
  dimension: price {
    description: "Price"
    type: string
    sql: ${TABLE}."JSON":"price"::string ;;
  }
    
  dimension: id {
    description: "Id"
    type: string
    sql: ${TABLE}."JSON":"_datalakeMetadata":"id"::string ;;
  }
    
  dimension: is_active {
    description: "Is Active"
    type: yesno
    sql: ${TABLE}."JSON":"isActive"::boolean ;;
  }
    
  dimension: received {
    description: "Received"
    type: date_time
    sql: ${TABLE}."JSON":"_datalakeMetadata":"received"::string ;;
  }
    
}

view: fulfillerList { 

  dimension: fulfiller {
    description: "Fulfiller"
    type: string
    sql: ${TABLE}.VALUE:"fulfiller"::string ;;
  }
    
}
