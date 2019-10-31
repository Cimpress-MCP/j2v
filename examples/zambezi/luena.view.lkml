
view: lueana_latest { 
  sql_table_name: ZAMBEZI ;;

  dimension: category {
    description: "Category"
    type: string
    sql: ${TABLE}."JSON":"category"::string ;;
  }
    
  dimension: id {
    description: "Id"
    type: string
    sql: ${TABLE}."JSON":"_datalakeMetadata":"id"::string ;;
    group_label: "Datalake metadata"
  }
    
  dimension: is_active {
    description: "Is active"
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
    group_label: "Datalake metadata"
  }
    
  dimension: stream_id {
    description: "Stream id"
    type: string
    sql: ${TABLE}."JSON":"_datalakeMetadata":"streamId"::string ;;
    group_label: "Datalake metadata"
  }
    
  dimension: transaction_id {
    description: "Transaction id"
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

view: fulfiller_list { 

  dimension: fulfiller {
    description: "Fulfiller"
    type: string
    sql: ${TABLE}.VALUE:"fulfiller"::string ;;
  }
    
}
