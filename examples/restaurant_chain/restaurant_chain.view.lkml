
view: JSON_TABLE { 
  sql_table_name: RESTAURANT_DETAILS ;;

  dimension: employees {
    description: "Employees"
    type: number
    sql: ${TABLE}."DATA":"headquater":"employees"::number ;;
  }
    
  dimension: city {
    description: "City"
    type: string
    sql: ${TABLE}."DATA":"headquater":"city"::string ;;
  }
    
  dimension: building_address {
    description: "Building Address"
    type: string
    sql: ${TABLE}."DATA":"headquater":"building":"address"::string ;;
  }
    
  dimension: payload_primary_key_value {
    description: "Payload Primary Key Value"
    type: string
    sql: ${TABLE}."DATA":"payloadPrimaryKeyValue"::string ;;
  }
    
  dimension: country {
    description: "Country"
    type: string
    sql: ${TABLE}."DATA":"headquater":"country"::string ;;
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
    sql: ${TABLE}."DATA":"dataGenerationTimestamp"::timestamp ;;
  }
    
  dimension: version {
    description: "Version"
    type: string
    sql: ${TABLE}."DATA":"version"::string ;;
  }
    
  dimension: provider {
    description: "Provider"
    type: string
    sql: ${TABLE}."DATA":"data Provider"::string ;;
  }
    
  dimension: api_version {
    description: "Api Version"
    type: string
    sql: ${TABLE}."DATA":"apiVersion"::string ;;
  }
    
}

view: restaurants { 

  dimension: country {
    description: "Country"
    type: string
    sql: ${TABLE}.VALUE:"country"::string ;;
  }
    
  dimension: address {
    description: "Address"
    type: string
    sql: ${TABLE}.VALUE:"address"::string ;;
  }
    
  dimension: name {
    description: "Name"
    type: string
    sql: ${TABLE}.VALUE:"name"::string ;;
  }
    
  dimension: currency {
    description: "Currency"
    type: string
    sql: ${TABLE}.VALUE:"currency"::string ;;
  }
    
  dimension: city {
    description: "City"
    type: string
    sql: ${TABLE}.VALUE:"city"::string ;;
  }
    
}

view: restaurants_menu { 

  dimension: menu_price {
    description: "Menu Price"
    type: number
    sql: ${TABLE}.VALUE:"price"::number ;;
  }
    
  dimension: menu_dish_name {
    description: "Menu Dish Name"
    type: string
    sql: ${TABLE}.VALUE:"dishName"::string ;;
  }
    
}

view: restaurants_menu_indegrients { 

  dimension: menu_indegrients_value {
    description: "Menu Indegrients Value"
    type: string
    sql: ${TABLE}.VALUE::string ;;
  }
    
}

view: headquater_building_floors { 

  dimension: building_floors_value {
    description: "Building Floors Value"
    type: number
    sql: ${TABLE}.VALUE::number ;;
  }
    
}
