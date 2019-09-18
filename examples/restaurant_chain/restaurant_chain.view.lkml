
view: JSON_TABLE { 
  sql_table_name: RESTAURANT_DETAILS ;;

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
    sql: ${TABLE}."DATA":"dataGenerationTimestamp"::timestamp ;;
  }
    
  dimension: api_version {
    description: "Api Version"
    type: string
    sql: ${TABLE}."DATA":"apiVersion"::string ;;
  }
    
  dimension: payload_primary_key_value {
    description: "Payload Primary Key Value"
    type: string
    sql: ${TABLE}."DATA":"payloadPrimaryKeyValue"::string ;;
  }
    
  dimension: version {
    description: "Version"
    type: string
    sql: ${TABLE}."DATA":"version"::string ;;
  }
    
  dimension:  {
    description: ""
    type: number
    sql: ${TABLE}."DATA":"headquater":"employees"::number ;;group_label:"headquater"
  }
    
  dimension:  {
    description: ""
    type: string
    sql: ${TABLE}."DATA":"headquater":"country"::string ;;group_label:"headquater"
  }
    
  dimension: address {
    description: "Address"
    type: string
    sql: ${TABLE}."DATA":"headquater":"building":"address"::string ;;group_label:"building"
  }
    
  dimension:  {
    description: ""
    type: string
    sql: ${TABLE}."DATA":"data Provider"::string ;;
  }
    
  dimension:  {
    description: ""
    type: string
    sql: ${TABLE}."DATA":"headquater":"city"::string ;;group_label:"headquater"
  }
    
}

view: restaurants { 

  dimension:  {
    description: ""
    type: string
    sql: ${TABLE}.VALUE:"city"::string ;;
  }
    
  dimension:  {
    description: ""
    type: string
    sql: ${TABLE}.VALUE:"name"::string ;;
  }
    
  dimension:  {
    description: ""
    type: string
    sql: ${TABLE}.VALUE:"country"::string ;;
  }
    
  dimension:  {
    description: ""
    type: string
    sql: ${TABLE}.VALUE:"currency"::string ;;
  }
    
  dimension:  {
    description: ""
    type: string
    sql: ${TABLE}.VALUE:"address"::string ;;
  }
    
}

view: restaurants_menu { 

  dimension: price {
    description: "Price"
    type: number
    sql: ${TABLE}.VALUE:"price"::number ;;
  }
    
  dimension: dish_name {
    description: "Dish Name"
    type: string
    sql: ${TABLE}.VALUE:"dishName"::string ;;
  }
    
}

view: restaurants_menu_indegrients { 

  dimension: indegrients_value {
    description: "Indegrients Value"
    type: string
    sql: ${TABLE}.VALUE::string ;;
  }
    
}

view: headquater_building_floors { 

  dimension: floors_value {
    description: "Floors Value"
    type: number
    sql: ${TABLE}.VALUE::number ;;
  }
    
}
