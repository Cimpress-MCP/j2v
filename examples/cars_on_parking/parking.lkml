include: "parking.view.view.lkml"
   
explore: JSON_TABLE {
  view_name: JSON_TABLE
  from: JSON_TABLE
  label: "JSON_TABLE explore"
  description: "JSON_TABLE explore"

  join: parkings {
     from: parkings
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => JSON_TABLE."data_column":"parkings") parkings;;
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
