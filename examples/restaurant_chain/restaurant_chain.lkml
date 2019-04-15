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
  
  join: restaurants_menu {
     from: restaurants_menu
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => restaurants.VALUE:"menu") restaurants_menu;;
     relationship: one_to_many 
     required_joins: [restaurants]
  }
  
  join: restaurants_menu_indegrients {
     from: restaurants_menu_indegrients
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => restaurants_menu.VALUE:"indegrients") restaurants_menu_indegrients;;
     relationship: one_to_many 
     required_joins: [restaurants_menu]
  }
  
  join: headquater_building_floors {
     from: headquater_building_floors
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => chains_table."raw_data_column":"headquater":"building":"floors") headquater_building_floors;;
     relationship: one_to_many 
  }
  
}
