include: "parking.view.lkml"
   
explore: json_table {
  view_name: json_table
  from: json_table
  label: "json_table explore"
  description: "json_table explore"

  join: parkings {
     from: parkings
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => json_table."data_column":"parkings") parkings;;
     relationship: one_to_many 
  }
  
  join: parkings_cars {
     from: parkings_cars
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => parkings.VALUE:"cars") parkings_cars;;
     relationship: one_to_many 
     required_joins: [parkings]
  }
  
  join: parkings_cars_damages {
     from: parkings_cars_damages
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => parkings_cars.VALUE:"damages") parkings_cars_damages;;
     relationship: one_to_many 
     required_joins: [parkings_cars]
  }
  
}
