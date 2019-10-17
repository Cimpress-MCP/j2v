
view: json_table { 
  sql_table_name: parking_table ;;

  dimension: api_version {
    description: "Api Version"
    type: string
    sql: ${TABLE}."data_column":"apiVersion"::string ;;
  }
    
  dimension: client {
    description: "Client"
    type: string
    sql: ${TABLE}."data_column":"client"::string ;;
  }
    
  dimension: data_provider {
    description: "Data Provider"
    type: string
    sql: ${TABLE}."data_column":"dataProvider"::string ;;
  }
    
  dimension: payload_primary_key_value {
    description: "Payload Primary Key Value"
    type: string
    sql: ${TABLE}."data_column":"payloadPrimaryKeyValue"::string ;;
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

  dimension: capacity {
    description: "Capacity"
    type: number
    sql: ${TABLE}.VALUE:"capacity"::number ;;
  }
    
  dimension: cars_now {
    description: "Status Cars Now"
    type: number
    sql: ${TABLE}.VALUE:"status":"carsNow"::number ;;
    group_label:"status"
  }
    
  dimension: id {
    description: "Id"
    type: number
    sql: ${TABLE}.VALUE:"id"::number ;;
  }
    
  dimension: is_broken {
    description: "Status Is Broken"
    type: yesno
    sql: ${TABLE}.VALUE:"status":"isBroken"::boolean ;;
    group_label:"status"
  }
    
  dimension: is_opened {
    description: "Status Is Opened"
    type: yesno
    sql: ${TABLE}.VALUE:"status":"isOpened"::boolean ;;
    group_label:"status"
  }
    
  dimension: name {
    description: "Name"
    type: string
    sql: ${TABLE}.VALUE:"name"::string ;;
  }
    
  dimension: owner {
    description: "Owner"
    type: string
    sql: ${TABLE}.VALUE:"owner"::string ;;
  }
    
  dimension: price {
    description: "Price"
    type: number
    sql: ${TABLE}.VALUE:"price"::number ;;
  }
    
  dimension: price_currency {
    description: "Price Currency"
    type: string
    sql: ${TABLE}.VALUE:"priceCurrency"::string ;;
  }
    
  dimension: price_unit {
    description: "Price Unit"
    type: string
    sql: ${TABLE}.VALUE:"priceUnit"::string ;;
  }
    
}

view: parkings_cars { 

  dimension: plate {
    description: "Cars Plate"
    type: string
    sql: ${TABLE}.VALUE:"plate"::string ;;
  }
    
  dimension: spot {
    description: "Cars Spot"
    type: number
    sql: ${TABLE}.VALUE:"spot"::number ;;
  }
    
  dimension_group: start_time {
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
    
}

view: parkings_cars_damages { 

  dimension: side {
    description: "Cars Damages Side"
    type: string
    sql: ${TABLE}.VALUE:"side"::string ;;
  }
    
  dimension: state {
    description: "Cars Damages State"
    type: string
    sql: ${TABLE}.VALUE:"state"::string ;;
  }
    
}
