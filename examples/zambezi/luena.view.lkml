
view: LUEANA_LATEST { 
  sql_table_name: "CIMPRESS"."ZAMBEZI"."LUENA" ;;

  dimension: is_active {
    description: "Is Active"
    type: yesno
    sql: ${TABLE}."JSON":"isActive"::boolean ;;
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
    
  dimension: transaction_id {
    description: "Transaction Id"
    type: string
    sql: ${TABLE}."JSON":"transactionId"::string ;;
  }
    
  dimension: id {
    description: "Id"
    type: string
    sql: ${TABLE}."JSON":"_datalakeMetadata":"id"::string ;;
	group_label:"_datalakeMetadata"
  }
    
  dimension: principal {
    description: "Principal"
    type: string
    sql: ${TABLE}."JSON":"_datalakeMetadata":"principal"::string ;;
	group_label:"_datalakeMetadata"
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
    
  dimension: category {
    description: "Category"
    type: string
    sql: ${TABLE}."JSON":"category"::string ;;
  }
    
  dimension: price {
    description: "Price"
    type: string
    sql: ${TABLE}."JSON":"price"::string ;;
  }
    
  dimension: stream_id {
    description: "Stream Id"
    type: string
    sql: ${TABLE}."JSON":"_datalakeMetadata":"streamId"::string ;;
	group_label:"_datalakeMetadata"
  }
    
  dimension: mcpsku {
    description: "Mcpsku"
    type: string
    sql: ${TABLE}."JSON":"mcpSKU"::string ;;
  }
    
}

view: fulfillerList { 

  dimension: fulfiller {
    description: "Fulfiller"
    type: string
    sql: ${TABLE}.VALUE:"fulfiller"::string ;;
  }
    
}
