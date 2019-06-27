include: "luena.view"
   
explore: JSON_VIEW {
  view_name: JSON_VIEW
  from: JSON_VIEW
  label: "JSON_VIEW explore"
  description: "JSON_VIEW explore"

  join: fulfillerList {
     from: fulfillerList
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => JSON_VIEW."JSON":"fulfillerList") fulfillerList;;
     relationship: one_to_many 
  }
  
}
