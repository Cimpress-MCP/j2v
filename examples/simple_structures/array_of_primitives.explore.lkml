include: "array_of_primitives.view.lkml"
   
explore: json_table {
  view_name: json_table
  from: json_table
  label: "json_table explore"
  description: "json_table explore"

  join: json_table_json {
     from: json_table_json
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => json_table."JSON") json_table_json;;
     relationship: one_to_many 
  }
  
}
