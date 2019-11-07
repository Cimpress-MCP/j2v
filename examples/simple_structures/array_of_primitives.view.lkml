
view: json_table { 
  sql_table_name: table_with_JSON_column ;;

}

view: json_table_json { 

  dimension: value {
    description: "Value"
    type: number
    sql: ${TABLE}.VALUE::number ;;
  }
    
}
