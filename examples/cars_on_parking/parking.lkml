include: "parking.view"
   
explore: parking_table {
  view_name: parking_table
  from: parking_table
  label: "parking_table explore"
  description: "parking_table explore"

  join: parkings {
     from: parkings
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => parking_table."data_column":"parkings") parkings;;
     relationship: one_to_many 
  }
  
  join: parkings_VALUEcars {
     from: parkings_VALUEcars
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => parkings.VALUE:"cars") parkings_VALUEcars;;
     relationship: one_to_many 
     required_joins: [parkings]
  }
  
  join: parkings_VALUEcars_VALUEdamages {
     from: parkings_VALUEcars_VALUEdamages
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => parkings_VALUEcars.VALUE:"damages") parkings_VALUEcars_VALUEdamages;;
     relationship: one_to_many 
     required_joins: [parkings_VALUEcars]
  }
  
}
