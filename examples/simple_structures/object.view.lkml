
view: json_table { 
  sql_table_name: table_with_JSON_column ;;

  dimension: a {
    label: "A"
    description: "A"
    type: number
    sql: ${TABLE}."JSON":"a"::number ;;
  }
    
  dimension: a_a {
    label: "A"
    description: "A"
    type: number
    sql: ${TABLE}."JSON":"aa":"a":"a"::number ;;
    group_label: "A"
  }
    
  dimension: aa {
    label: "Aa"
    description: "Aa"
    type: number
    sql: ${TABLE}."JSON":"aa":"aa"::number ;;
    group_label: "Aa"
  }
    
}
