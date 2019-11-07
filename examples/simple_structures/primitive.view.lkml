
view: json_table { 
  sql_table_name: table_with_JSON_column ;;

  dimension: value {
    description: "Value"
    type: string
    sql: ${TABLE}."JSON"::string ;;
  }
    
}
