include: "restaurant_chain.view"
   
explore: JSON_VIEW {
  view_name: JSON_VIEW
  from: JSON_VIEW
  label: "JSON_VIEW explore"
  description: "JSON_VIEW explore"

  join: restaurants {
     from: restaurants
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => JSON_VIEW."DATA":"restaurants") restaurants;;
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
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => JSON_VIEW."DATA":"headquater":"building":"floors") headquater_building_floors;;
     relationship: one_to_many 
  }
  
}
