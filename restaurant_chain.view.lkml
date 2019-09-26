
view: JSON_TABLE { 
  sql_table_name: RESTAURANT_DETAILS ;;

  dimension: building_address {
    description: "Building Address"
    type: string
    sql: ${TABLE}."DATA":"headquarter":"building":"address"::string ;;
	group_label:"building"
  }
    
  dimension: employees {
    description: "Employees"
    type: number
    sql: ${TABLE}."DATA":"headquarter":"employees"::number ;;
	group_label:"headquarter"
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
    
  dimension: city {
    description: "City"
    type: string
    sql: ${TABLE}."DATA":"headquarter":"city"::string ;;
	group_label:"headquarter"
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
    
  dimension: version {
    description: "Version"
    type: string
    sql: ${TABLE}."DATA":"version"::string ;;
  }
    
  dimension: country {
    description: "Country"
    type: string
    sql: ${TABLE}."DATA":"headquarter":"country"::string ;;
	group_label:"headquarter"
  }
    
}

view: restaurants { 

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
    
  dimension: country {
    description: "Country"
    type: string
    sql: ${TABLE}.VALUE:"country"::string ;;
  }
    
  dimension: name {
    description: "Name"
    type: string
    sql: ${TABLE}.VALUE:"name"::string ;;
  }
    
  dimension: address {
    description: "Address"
    type: string
    sql: ${TABLE}.VALUE:"address"::string ;;
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

view: restaurants_menu_ingredients { 

  dimension: menu_ingredients_value {
    description: "Menu Ingredients Value"
    type: string
    sql: ${TABLE}.VALUE::string ;;
  }
    
}

view: headquarter_building_floors { 

  dimension: building_floors_value {
    description: "Building Floors Value"
    type: number
    sql: ${TABLE}.VALUE::number ;;
  }
    
}
