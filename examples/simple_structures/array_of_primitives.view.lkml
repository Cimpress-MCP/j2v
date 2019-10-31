
view: json_table_json { 

  dimension: value {
    description: "Value"
    type: number
    sql: ${TABLE}.VALUE::number ;;
  }
    
}
