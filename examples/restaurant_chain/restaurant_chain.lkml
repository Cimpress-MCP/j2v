include: "restaurant_chain.view"
   
explore: chains {
  view_name: chains
  from: chains
  label: "chains explore"
  description: "chains explore"

  join: restaurants {
     from: restaurants
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => chains.raw_data:restaurants) restaurants;;
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
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => chains.raw_data:headquater:building:floors) floors;;
     relationship: one_to_many 
  }
  
  join: chains_restaurants {
     from: chains_restaurants
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => chains.raw_data:restaurants) chains_restaurants;;
     relationship: one_to_many 
  }
  
}
