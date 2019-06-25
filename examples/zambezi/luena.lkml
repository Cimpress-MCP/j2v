include: "luena.view"
   
explore: LUEANA_LATEST {
  view_name: LUEANA_LATEST
  from: LUEANA_LATEST
  label: "LUEANA_LATEST explore"
  description: "LUEANA_LATEST explore"

  join: fulfillerList {
     from: fulfillerList
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => LUEANA_LATEST."JSON":"fulfillerList") fulfillerList;;
     relationship: one_to_many 
  }
  
}
