include: "luena.view.lkml"
   
explore: lueana_latest {
  view_name: lueana_latest
  from: lueana_latest
  label: "lueana_latest explore"
  description: "lueana_latest explore"

  join: fulfillerlist {
     from: fulfillerlist
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => LUEANA_LATEST."JSON":"fulfillerList") fulfillerlist;;
     relationship: one_to_many 
  }
  
}
