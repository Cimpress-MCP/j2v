include: "restaurant_chain.view"
   
explore: chains_table {
  view_name: chains_table
  from: chains_table
  label: "chains_table explore"
  description: "chains_table explore"

  join: restaurants {
     from: restaurants
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => chains_table.raw_data_column:restaurants) restaurants;;
     relationship: one_to_many 
  }
  
  join: menu {
     from: menu
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => restaurants.VALUE:menu) menu;;
     relationship: one_to_many 
     required_joins: [restaurants]
  }
  
  join: indegrients {
     from: indegrients
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => menu.VALUE:indegrients) indegrients;;
     relationship: one_to_many 
     required_joins: [menu]
  }
  
  join: floors {
     from: floors
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => chains_table.raw_data_column:headquater:building:floors) floors;;
     relationship: one_to_many 
  }
  
}
