include: "parking.view"
   
explore: parking_table {
  view_name: parking_table
  from: parking_table
  label: "parking_table explore"
  description: "parking_table explore"

  join: parkings {
     from: parkings
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => parking_table.data_column:parkings) parkings;;
     relationship: one_to_many 
  }
  
  join: damages {
     from: damages
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => cars.VALUE:damages) damages;;
     relationship: one_to_many 
     required_joins: [cars]
  }
  
}
