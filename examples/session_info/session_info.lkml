include: "session_info.view.lkml"
   
explore: JSON_TABLE {
  view_name: JSON_TABLE
  from: JSON_TABLE
  label: "JSON_TABLE explore"
  description: "JSON_TABLE explore"

  join: description {
     from: description
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => JSON_TABLE."session_user":"description") description;;
     relationship: one_to_many 
  }
  
}
