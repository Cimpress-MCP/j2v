include: "luena.view.lkml"
   
explore: lueana_latest {
  view_name: lueana_latest
  from: lueana_latest
  label: "lueana_latest explore"
  description: "lueana_latest explore"

  join: fulfiller_list {
     from: fulfiller_list
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => lueana_latest."JSON":"fulfillerList") fulfiller_list;;
     relationship: one_to_many 
  }
  
}
