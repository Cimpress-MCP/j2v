
view: json_table { 
  sql_table_name: parking_table ;;

  dimension: api_version {
    label: "Api version"
    description: "Api version"
    type: string
    sql: ${TABLE}."data_column":"apiVersion"::string ;;
  }
    
  dimension: client {
    label: "Client"
    description: "Client"
    type: string
    sql: ${TABLE}."data_column":"client"::string ;;
  }
    
  dimension: data_provider {
    label: "Data provider"
    description: "Data provider"
    type: string
    sql: ${TABLE}."data_column":"dataProvider"::string ;;
  }
    
  dimension: payload_primary_key_value {
    label: "Payload primary key value"
    description: "Payload primary key value"
    primary_key: yes
    type: string
    sql: ${TABLE}."data_column":"payloadPrimaryKeyValue"::string ;;
  }
    
  dimension_group: data_generation_timestamp {
    description: "Data generation timestamp"
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
    label: "Capacity"
    description: "Capacity"
    type: number
    sql: ${TABLE}.VALUE:"capacity"::number ;;
  }
    
  dimension: cars_now {
    label: "Cars now"
    description: "Cars now"
    type: number
    sql: ${TABLE}.VALUE:"status":"carsNow"::number ;;
    group_label: "Status"
  }
    
  dimension: id {
    label: "Id"
    description: "Id"
    type: number
    sql: ${TABLE}.VALUE:"id"::number ;;
  }
    
  dimension: is_broken {
    label: "Is broken"
    description: "Is broken"
    type: yesno
    sql: ${TABLE}.VALUE:"status":"isBroken"::boolean ;;
    group_label: "Status"
  }
    
  dimension: is_opened {
    label: "Is opened"
    description: "Is opened"
    type: yesno
    sql: ${TABLE}.VALUE:"status":"isOpened"::boolean ;;
    group_label: "Status"
  }
    
  dimension: name {
    label: "Name"
    description: "Name"
    type: string
    sql: ${TABLE}.VALUE:"name"::string ;;
  }
    
  dimension: owner {
    label: "Owner"
    description: "Owner"
    type: string
    sql: ${TABLE}.VALUE:"owner"::string ;;
  }
    
  dimension: price {
    label: "Price"
    description: "Price"
    type: number
    sql: ${TABLE}.VALUE:"price"::number ;;
  }
    
  dimension: price_currency {
    label: "Price currency"
    description: "Price currency"
    type: string
    sql: ${TABLE}.VALUE:"priceCurrency"::string ;;
  }
    
  dimension: price_unit {
    label: "Price unit"
    description: "Price unit"
    type: string
    sql: ${TABLE}.VALUE:"priceUnit"::string ;;
  }
    
}

view: parkings_cars { 

  dimension: plate {
    label: "Plate"
    description: "Plate"
    type: string
    sql: ${TABLE}.VALUE:"plate"::string ;;
  }
    
  dimension: spot {
    label: "Spot"
    description: "Spot"
    type: number
    sql: ${TABLE}.VALUE:"spot"::number ;;
  }
    
  dimension_group: start_time {
    description: "Start time"
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
    label: "Side"
    description: "Side"
    type: string
    sql: ${TABLE}.VALUE:"side"::string ;;
  }
    
  dimension: state {
    label: "State"
    description: "State"
    type: string
    sql: ${TABLE}.VALUE:"state"::string ;;
  }
    
}
