
view: json_table { 
  sql_table_name: table_with_JSON_column ;;

}

view: json_table_json { 

  dimension: id {
    description: "Id"
    type: number
    sql: ${TABLE}.VALUE:"data":"id"::number ;;
    group_label: "Data"
  }
    
  dimension: name {
    description: "Name"
    type: string
    sql: ${TABLE}.VALUE:"data":"name"::string ;;
    group_label: "Data"
  }
    
}
