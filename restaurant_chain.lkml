include: "restaurant_chain.view"
   
explore: chains_table {
  view_name: chains_table
  from: chains_table
  label: "chains_table explore"
  description: "chains_table explore"

  join: chains_table_raw_data_column_restaurants {
     from: chains_table_raw_data_column_restaurants
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => chains_table."raw_data_column":"restaurants") chains_table_raw_data_column_restaurants;;
     relationship: one_to_many 
  }
  
  join: restaurants_menu {
     from: restaurants_menu
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => chains_table_raw_data_column_restaurants.VALUE:"menu") restaurants_menu;;
     relationship: one_to_many 
     required_joins: [chains_table_raw_data_column_restaurants]
  }
  
  join: restaurants_menu_indegrients {
     from: restaurants_menu_indegrients
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => restaurants_menu.VALUE:"indegrients") restaurants_menu_indegrients;;
     relationship: one_to_many 
     required_joins: [restaurants_menu]
  }
  
  join: chains_table_raw_data_column_headquater_building_floors {
     from: chains_table_raw_data_column_headquater_building_floors
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => chains_table."raw_data_column":"headquater":"building":"floors") chains_table_raw_data_column_headquater_building_floors;;
     relationship: one_to_many 
  }
  
}
