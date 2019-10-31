
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
