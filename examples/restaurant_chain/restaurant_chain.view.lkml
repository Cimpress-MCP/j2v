
view: chains_table { 
  sql_table_name: RESTAURANT_DETAILS ;;

  dimension: address {
    description: "Address"
    type: string
    sql: ${TABLE}."DATA":"headquarter":"building":"address"::string ;;
    group_label: "Building"
  }
    
  dimension: api_version {
    description: "Api version"
    primary_key: yes
    type: string
    sql: ${TABLE}."DATA":"apiVersion"::string ;;
  }
    
  dimension: city {
    description: "City"
    type: string
    sql: ${TABLE}."DATA":"headquarter":"city"::string ;;
    group_label: "Headquarter"
  }
    
  dimension: country {
    description: "Country"
    type: string
    sql: ${TABLE}."DATA":"headquarter":"country"::string ;;
    group_label: "Headquarter"
  }
    
  dimension: data_provider {
    description: "Data provider"
    type: string
    sql: ${TABLE}."DATA":"data Provider"::string ;;
  }
    
  dimension: employees {
    description: "Employees"
    type: number
    sql: ${TABLE}."DATA":"headquarter":"employees"::number ;;
    group_label: "Headquarter"
  }
    
  dimension: payload_primary_key_value {
    description: "Payload primary key value"
    type: string
    sql: ${TABLE}."DATA":"payloadPrimaryKeyValue"::string ;;
  }
    
  dimension: version {
    description: "Version"
    type: string
    sql: ${TABLE}."DATA":"version"::string ;;
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
    sql: ${TABLE}."DATA":"dataGenerationTimestamp"::timestamp ;;
  }
    
}

view: restaurants { 

  dimension: address {
    description: "Address"
    type: string
    sql: ${TABLE}.VALUE:"address"::string ;;
  }
    
  dimension: city {
    description: "City"
    type: string
    sql: ${TABLE}.VALUE:"city"::string ;;
  }
    
  dimension: country {
    description: "Country"
    type: string
    sql: ${TABLE}.VALUE:"country"::string ;;
  }
    
  dimension: currency {
    description: "Currency"
    type: string
    sql: ${TABLE}.VALUE:"currency"::string ;;
  }
    
  dimension: name {
    description: "Name"
    type: string
    sql: ${TABLE}.VALUE:"name"::string ;;
  }
    
  dimension_group: open_time {
    description: "Open time"
    datatype: epoch
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
    sql: ${TABLE}.VALUE:"openTime"::number ;;
  }
    
}

view: restaurants_menu { 

  dimension: dish_name {
    description: "Dish name"
    type: string
    sql: ${TABLE}.VALUE:"dishName"::string ;;
  }
    
  dimension: price {
    description: "Price"
    type: number
    sql: ${TABLE}.VALUE:"price"::number ;;
  }
    
}

view: restaurants_menu_ingredients { 

  dimension: value {
    description: "Value"
    type: string
    sql: ${TABLE}.VALUE::string ;;
  }
    
}

view: headquarter_building_floors { 

  dimension: value {
    description: "Value"
    type: number
    sql: ${TABLE}.VALUE::number ;;
  }
    
}
