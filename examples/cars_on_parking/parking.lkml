include: "parking.view"
   
explore: parking {
  view_name: parking
  from: parking
  label: "parking explore"
  description: "parking explore"

  join: parkings {
     from: parkings
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => parking.data:parkings) parkings;;
     relationship: one_to_many 
  }
  
  join: cars {
     from: cars
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => parkings.VALUE:cars) cars;;
     relationship: one_to_many 
     required_joins: [parkings]
  }
  
  join: damages {
     from: damages
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => cars.VALUE:damages) damages;;
     relationship: one_to_many 
     required_joins: [cars]
  }
  
}
