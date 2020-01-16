
view: lueana_latest { 
  sql_table_name: ZAMBEZI ;;
  label: Lueana Latest

  dimension: category {
    label: "Category"
    description: "Category"
    type: string
    sql: ${TABLE}."JSON":"category"::string ;;
  }
    
  dimension: id {
    label: "Id"
    description: "Id"
    type: string
    sql: ${TABLE}."JSON":"_datalakeMetadata":"id"::string ;;
    group_label: "Datalake metadata"
  }
    
  dimension: is_active {
    label: "Is Active"
    description: "Is Active"
    type: yesno
    sql: ${TABLE}."JSON":"isActive"::boolean ;;
  }
    
  dimension: mcpsku {
    label: "Mcpsku"
    description: "Mcpsku"
    type: string
    sql: ${TABLE}."JSON":"mcpSKU"::string ;;
  }
    
  dimension: price {
    label: "Price"
    description: "Price"
    type: string
    sql: ${TABLE}."JSON":"price"::string ;;
  }
    
  dimension: principal {
    label: "Principal"
    description: "Principal"
    type: string
    sql: ${TABLE}."JSON":"_datalakeMetadata":"principal"::string ;;
    group_label: "Datalake metadata"
  }
    
  dimension: stream_id {
    label: "Stream Id"
    description: "Stream Id"
    type: string
    sql: ${TABLE}."JSON":"_datalakeMetadata":"streamId"::string ;;
    group_label: "Datalake metadata"
  }
    
  dimension: transaction_id {
    label: "Transaction Id"
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

view: fulfiller_list { 
  label: Fulfiller List

  dimension: fulfiller {
    label: "Fulfiller"
    description: "Fulfiller"
    type: string
    sql: ${TABLE}.VALUE:"fulfiller"::string ;;
  }
    
}
