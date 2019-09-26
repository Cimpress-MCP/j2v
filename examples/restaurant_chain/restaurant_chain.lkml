include: "restaurant_chain.view.lkml"
   
explore: JSON_TABLE {
  view_name: JSON_TABLE
  from: JSON_TABLE
  label: "JSON_TABLE explore"
  description: "JSON_TABLE explore"

  join: restaurants {
     from: restaurants
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => JSON_TABLE."DATA":"restaurants") restaurants;;
     relationship: one_to_many 
  }
  
  join: restaurants_menu {
     from: restaurants_menu
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => restaurants.VALUE:"menu") restaurants_menu;;
     relationship: one_to_many 
     required_joins: [restaurants]
  }
  
  join: restaurants_menu_ingredients {
     from: restaurants_menu_ingredients
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => restaurants_menu.VALUE:"ingredients") restaurants_menu_ingredients;;
     relationship: one_to_many 
     required_joins: [restaurants_menu]
  }
  
  join: headquarter_building_floors {
     from: headquarter_building_floors
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => JSON_TABLE."DATA":"headquarter":"building":"floors") headquarter_building_floors;;
     relationship: one_to_many 
  }
  
}
