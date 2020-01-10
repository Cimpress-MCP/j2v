
view: json_table { 
  sql_table_name: table_with_JSON_column ;;

  dimension: value {
    label: "Value"
    description: "Value"
    type: string
    sql: ${TABLE}."JSON"::string ;;
  }
    
}
