
view: JSON_TABLE { 
  sql_table_name: RESTAURANT_DETAILS ;;

  dimension: employees {
    description: "Employees"
    type: number
    sql: ${TABLE}."DATA":"headquater":"employees"::number ;;
    group_label:"headquater"
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
    
  dimension: payload_primary_key_value {
    description: "Payload Primary Key Value"
    type: string
    sql: ${TABLE}."DATA":"payloadPrimaryKeyValue"::string ;;
    
  }
    
  dimension: country {
    description: "Country"
    type: string
    sql: ${TABLE}."DATA":"headquater":"country"::string ;;
    group_label:"headquater"
  }
    
  dimension: city {
    description: "City"
    type: string
    sql: ${TABLE}."DATA":"headquater":"city"::string ;;
    group_label:"headquater"
  }
    
  dimension: version {
    description: "Version"
    type: string
    sql: ${TABLE}."DATA":"version"::string ;;
    
  }
    
  dimension: api_version {
    description: "Api Version"
    type: string
    sql: ${TABLE}."DATA":"apiVersion"::string ;;
    
  }
    
  dimension: provider {
    description: "Provider"
    type: string
    sql: ${TABLE}."DATA":"data Provider"::string ;;
    
  }
    
  dimension: building_address {
    description: "Building Address"
    type: string
    sql: ${TABLE}."DATA":"headquater":"building":"address"::string ;;
    group_label:"building"
  }
    
}

view: restaurants { 

  dimension: city {
    description: "City"
    type: string
    sql: ${TABLE}.VALUE:"city"::string ;;
    
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
