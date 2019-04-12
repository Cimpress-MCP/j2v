include: "restaurant_chain.view"
   
explore: chains_table {
  view_name: chains_table
  from: chains_table
  label: "chains_table explore"
  description: "chains_table explore"

  join: restaurants {
     from: restaurants
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => chains_table."raw_data_column":"restaurants") restaurants;;
     relationship: one_to_many 
  }
  
  join: restaurants_VALUEmenu {
     from: restaurants_VALUEmenu
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => restaurants.VALUE:"menu") restaurants_VALUEmenu;;
     relationship: one_to_many 
     required_joins: [restaurants]
  }
  
  join: restaurants_VALUEmenu_VALUEindegrients {
     from: restaurants_VALUEmenu_VALUEindegrients
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => restaurants_VALUEmenu.VALUE:"indegrients") restaurants_VALUEmenu_VALUEindegrients;;
     relationship: one_to_many 
     required_joins: [restaurants_VALUEmenu]
  }
  
  join: headquater_building_floors {
     from: headquater_building_floors
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => chains_table."raw_data_column":"headquater":"building":"floors") headquater_building_floors;;
     relationship: one_to_many 
  }
  
}
