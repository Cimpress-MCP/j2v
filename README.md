[![PyPI version](https://badge.fury.io/py/j2v.svg)](https://badge.fury.io/py/j2v)
# JSONs to Looker views (J2V)

J2V is a simple command-line tool to convert JSON to [Looker](https://looker.com/) readable files in forms of [Looker Views](https://docs.looker.com/reference/view-params/view) and [Looker Explores](https://docs.looker.com/reference/explore-params/explore).

Also it outputs an SQL with proper paths and explosion expressions.

This is useful to be used in combination with databases that are focusing on schema-on-read, and data is stored in raw JSON instead of exploded into columns of a table or view.

## Example use case

You have a table in your database. This table contains a column containing JSONs (one JSON per row). You are very curious how these data look like exploded, but you do not want to spend 2h going through the JSON structure and specifying all the fields just to surface them in Looker.

With J2V all the structures are discovered automatically and two files are generated - a Looker View and Looker Explore. All you need to do is copy/paste the output of this command line tool into your Looker project and you can start exploring.

# Usage

## Requirements

[Python 3](https://www.python.org/downloads/) must be installed.

## How to run
* use code from github or
* `pip install j2v`

## Parameters

* `json_files`: Files in JSON format, representing the data stored in a table
* `output_view`: Name of Looker View output file to be created
* `output_explore`: Name of Looker model output file to be created
* `sql_table_name`: Name of the DB table to be used (this is only used in the LookML files; no actual connection to a database will be done as part of this tool)
* `column_name`: Name of the column in the DB table as specified in `sql_table_name`. (this is only used in the LookML files; no actual connection to a database will be done as part of this tool)

## Output

* `output_view`: File containing definitions of Looker views (see [examples](./examples/) directory in this repository)
* `output_explore`: File containing definition of looker explore exploding the structures (see [examples](./examples/) directory in this repository)

## Example usage

### Using all parameters

`python3 main.py --json_files data1.json data2.json --output_view restaurant_chain.view --output_explore restaurant_chain.lkml --column_name raw_data --sql_table_name chains`

### Using only mandatory parameters

`python3 main.py --json_files order_example.json order_example2.json order_example3.json`<br />

# Contribution

## Project structure:

* `j2v` - source code of a package
* `examples` - working examples
* `tests` - tests

## Contribute

1. If unsure, open an issue for a discussion
1. Create a fork
1. Make your change
1. Make a pull request
1. Happy contribution!

## EXAMPLE

### Input: 
```json
{
  "apiVersion": "v3.4",
  "data Provider": "Eat me",
  "restaurants": [
    {
      "name": "Super Burger",
      "city": "Sydney",
      "country": "Australia",
      "address": "Big Street 3",
      "currency": "AUD",
      "menu": [
        {
          "dishName": "BurgerPlus",
          "price": 10,
          "ingredients": ["Meat", "Cheese", "Bun"]
        }
      ]
    }
  ],
  "headquarter": {
    "employees": 36,
    "city": "Olsztyn",
    "country": "Poland",
    "building": {
      "address": "3 Maja 10",
      "floors": [1, 2, 7]
    }
  },
  "dataGenerationTimestamp": "2019-03-30T11:30:00.812Z",
  "payloadPrimaryKeyValue": "3ab21b54-22d6-473c-b055-4430f8927d4c",
  "version": null
}
```

### Ouput:

#### SQL output (now only Snowflake dialect supported):

```SQL

SELECT

---JSON_TABLE Information
IFNULL(JSON_TABLE."DATA":"apiVersion"::string,'N/A') AS APIVERSION
,IFNULL(JSON_TABLE."DATA":"data Provider"::string,'N/A') AS DATA_PROVIDER
,IFNULL(JSON_TABLE."DATA":"headquarter":"building":"address"::string,'N/A') AS HEADQUARTER_BUILDING_ADDRESS
,IFNULL(JSON_TABLE."DATA":"headquarter":"city"::string,'N/A') AS HEADQUARTER_CITY
,IFNULL(JSON_TABLE."DATA":"headquarter":"country"::string,'N/A') AS HEADQUARTER_COUNTRY
,IFNULL(JSON_TABLE."DATA":"headquarter":"employees"::number,0) AS HEADQUARTER_EMPLOYEES
,IFNULL(JSON_TABLE."DATA":"payloadPrimaryKeyValue"::string,'N/A') AS PAYLOADPRIMARYKEYVALUE
,IFNULL(JSON_TABLE."DATA":"version"::string,'N/A') AS VERSION
,JSON_TABLE."DATA":"dataGenerationTimestamp"::timestamp AS DATAGENERATIONTIMESTAMP
,
---restaurants Information
IFNULL(restaurants.VALUE:"address"::string,'N/A') AS RESTAURANTS_ADDRESS
,IFNULL(restaurants.VALUE:"city"::string,'N/A') AS RESTAURANTS_CITY
,IFNULL(restaurants.VALUE:"country"::string,'N/A') AS RESTAURANTS_COUNTRY
,IFNULL(restaurants.VALUE:"currency"::string,'N/A') AS RESTAURANTS_CURRENCY
,IFNULL(restaurants.VALUE:"name"::string,'N/A') AS RESTAURANTS_NAME
,
---restaurants_menu Information
IFNULL(restaurants_menu.VALUE:"dishName"::string,'N/A') AS RESTAURANTS_MENU_DISHNAME
,IFNULL(restaurants_menu.VALUE:"price"::number,0) AS RESTAURANTS_MENU_PRICE
,
---restaurants_menu_ingredients Information
IFNULL(restaurants_menu_ingredients.VALUE::string,'N/A') AS RESTAURANTS_MENU_INGREDIENTS_VALUE
,
---headquarter_building_floors Information
IFNULL(headquarter_building_floors.VALUE::number,0) AS HEADQUARTER_BUILDING_FLOORS_VALUE
FROM RESTAURANT_DETAILS AS JSON_TABLE,
LATERAL FLATTEN(OUTER => TRUE, INPUT => JSON_TABLE."DATA":"restaurants") restaurants
,LATERAL FLATTEN(OUTER => TRUE, INPUT => restaurants.VALUE:"menu") restaurants_menu
,LATERAL FLATTEN(OUTER => TRUE, INPUT => restaurants_menu.VALUE:"ingredients") restaurants_menu_ingredients
,LATERAL FLATTEN(OUTER => TRUE, INPUT => JSON_TABLE."DATA":"headquarter":"building":"floors") headquarter_building_floors

```

#### Ouput files:

##### View file:

```LookML

view: JSON_TABLE { 
  sql_table_name: RESTAURANT_DETAILS ;;

  dimension: country {
    description: "Country"
    type: string
    sql: ${TABLE}."DATA":"headquarter":"country"::string ;;
	group_label:"headquarter"
  }
    
  dimension: employees {
    description: "Employees"
    type: number
    sql: ${TABLE}."DATA":"headquarter":"employees"::number ;;
	group_label:"headquarter"
  }
    
  dimension: building_address {
    description: "Building Address"
    type: string
    sql: ${TABLE}."DATA":"headquarter":"building":"address"::string ;;
	group_label:"building"
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
    
  dimension: version {
    description: "Version"
    type: string
    sql: ${TABLE}."DATA":"version"::string ;;
  }
    
  dimension: payload_primary_key_value {
    description: "Payload Primary Key Value"
    type: string
    sql: ${TABLE}."DATA":"payloadPrimaryKeyValue"::string ;;
  }
    
  dimension: api_version {
    description: "Api Version"
    type: string
    sql: ${TABLE}."DATA":"apiVersion"::string ;;
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

```

##### Explore file:

```LookML
include: "restaurant_chain.view.lkml"
   
explore: JSON_TABLE {
  view_name: JSON_TABLE
  from: JSON_TABLE
  label: "JSON_TABLE explore"
  description: "JSON_TABLE explore"

  join: restaurants {
     from: restaurants
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => JSON_TABLE."DATA":"restaurants") restaurants;;
     relationship: one_to_many 
  }
  
  join: restaurants_menu {
     from: restaurants_menu
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => restaurants.VALUE:"menu") restaurants_menu;;
     relationship: one_to_many 
     required_joins: [restaurants]
  }
  
  join: restaurants_menu_ingredients {
     from: restaurants_menu_ingredients
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => restaurants_menu.VALUE:"ingredients") restaurants_menu_ingredients;;
     relationship: one_to_many 
     required_joins: [restaurants_menu]
  }
  
  join: headquarter_building_floors {
     from: headquarter_building_floors
     sql:,LATERAL FLATTEN(OUTER => TRUE, INPUT => JSON_TABLE."DATA":"headquarter":"building":"floors") headquarter_building_floors;;
     relationship: one_to_many 
  } 
}

```


