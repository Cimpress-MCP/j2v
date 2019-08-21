
view: JSON_TABLE { 
  sql_table_name: parking_table ;;

  dimension: payload_primary_key_value {
    description: "Payload Primary Key Value"
    type: string
    sql: ${TABLE}."data_column":"payloadPrimaryKeyValue"::string ;;
  }
    
  dimension: data_provider {
    description: "Data Provider"
    type: string
    sql: ${TABLE}."data_column":"dataProvider"::string ;;
  }
    
  dimension: api_version {
    description: "Api Version"
    type: string
    sql: ${TABLE}."data_column":"apiVersion"::string ;;
  }
    
  dimension_group: data_generation_timestamp {
    description: "Data Generation Timestamp"
    type: time
    timeframes: [
        raw,
        time,
        date,
        week,
        month,
        quarter,
        year
    ]
    sql: ${TABLE}."data_column":"dataGenerationTimestamp"::timestamp ;;
  }
    
}

view: parkings { 

  dimension: status_is_broken {
    description: "Status Is Broken"
    type: yesno
    sql: ${TABLE}.VALUE:"status":"isBroken"::boolean ;;
  }
    
  dimension: owner {
    description: "Owner"
    type: string
    sql: ${TABLE}.VALUE:"owner"::string ;;
  }
    
  dimension: id {
    description: "Id"
    type: number
    sql: ${TABLE}.VALUE:"id"::number ;;
  }
    
  dimension: price_unit {
    description: "Price Unit"
    type: string
    sql: ${TABLE}.VALUE:"priceUnit"::string ;;
  }
    
  dimension: status_is_opened {
    description: "Status Is Opened"
    type: yesno
    sql: ${TABLE}.VALUE:"status":"isOpened"::boolean ;;
  }
    
  dimension: capacity {
    description: "Capacity"
    type: number
    sql: ${TABLE}.VALUE:"capacity"::number ;;
  }
    
  dimension: name {
    description: "Name"
    type: string
    sql: ${TABLE}.VALUE:"name"::string ;;
  }
    
  dimension: price_currency {
    description: "Price Currency"
    type: string
    sql: ${TABLE}.VALUE:"priceCurrency"::string ;;
  }
    
  dimension: status_cars_now {
    description: "Status Cars Now"
    type: number
    sql: ${TABLE}.VALUE:"status":"carsNow"::number ;;
  }
    
  dimension: price {
    description: "Price"
    type: number
    sql: ${TABLE}.VALUE:"price"::number ;;
  }
    
}

view: parkings_cars { 

  dimension: cars_plate {
    description: "Cars Plate"
    type: string
    sql: ${TABLE}.VALUE:"plate"::string ;;
  }
    
  dimension_group: cars_start_time {
    description: "Cars Start Time"
    type: time
    timeframes: [
        raw,
        time,
        date,
        week,
        month,
        quarter,
        year
    ]
    sql: ${TABLE}.VALUE:"startTime"::timestamp ;;
  }
    
  dimension: cars_spot {
    description: "Cars Spot"
    type: number
    sql: ${TABLE}.VALUE:"spot"::number ;;
  }
    
}

view: parkings_cars_damages { 

  dimension: cars_damages_state {
    description: "Cars Damages State"
    type: string
    sql: ${TABLE}.VALUE:"state"::string ;;
  }
    
  dimension: cars_damages_side {
    description: "Cars Damages Side"
    type: string
    sql: ${TABLE}.VALUE:"side"::string ;;
  }
    
}
