include: "luena.view.lkml"
   
explore: lueana_latest {
  view_name: lueana_latest
  from: lueana_latest
  label: "lueana_latest explore"
  description: "lueana_latest explore"

  join: FULFILLERSLIST {
     from: FULFILLERSLIST
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => lueana_latest."JSON":"FULFILLERSLIST") FULFILLERSLIST;;
     relationship: one_to_many 
  }
  
}
