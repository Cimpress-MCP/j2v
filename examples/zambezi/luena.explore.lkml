include: "luena.view.lkml"
   
explore: LUEANA_LATEST {
  view_name: LUEANA_LATEST
  from: LUEANA_LATEST
  label: "LUEANA_LATEST explore"
  description: "LUEANA_LATEST explore"

  join: fulfillerlist {
     from: fulfillerlist
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => LUEANA_LATEST."JSON":"fulfillerList") fulfillerlist;;
     relationship: one_to_many 
  }
  
}
